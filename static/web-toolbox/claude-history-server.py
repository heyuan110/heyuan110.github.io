#!/usr/bin/env python3
"""
Claude Code 历史记录查看器 - 本地服务器
自动加载 ~/.claude/projects/ 目录的历史记录

使用方法:
  python3 claude-history-server.py

然后浏览器会自动打开查看器
"""

import os
import json
import http.server
import socketserver
import webbrowser
import urllib.parse
from pathlib import Path

PORT = 8765
CLAUDE_DIR = Path.home() / '.claude'
PROJECTS_DIR = CLAUDE_DIR / 'projects'

class ClaudeHistoryHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # 设置工作目录为脚本所在目录
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # API: 获取所有项目和会话列表
        if parsed.path == '/api/sessions':
            self.send_json(self.get_all_sessions())
            return

        # API: 获取指定会话内容
        if parsed.path.startswith('/api/session/'):
            session_path = parsed.path[13:]  # 移除 '/api/session/'
            session_path = urllib.parse.unquote(session_path)
            self.send_json(self.get_session_content(session_path))
            return

        # 其他请求走默认处理
        super().do_GET()

    def send_json(self, data):
        content = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(content))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content)

    def get_all_sessions(self):
        """获取所有项目和会话"""
        sessions = []

        if not PROJECTS_DIR.exists():
            return {'error': f'目录不存在: {PROJECTS_DIR}', 'sessions': []}

        for project_dir in PROJECTS_DIR.iterdir():
            if not project_dir.is_dir():
                continue

            project_name = project_dir.name
            # 将目录名转回路径格式
            project_path = '/' + project_name.replace('-', '/')

            for jsonl_file in project_dir.glob('*.jsonl'):
                # 跳过 agent 文件
                if jsonl_file.name.startswith('agent-'):
                    continue

                try:
                    session_info = self.parse_session_file(jsonl_file, project_path)
                    if session_info:
                        sessions.append(session_info)
                except Exception as e:
                    print(f"解析文件出错 {jsonl_file}: {e}")

        # 按时间排序
        sessions.sort(key=lambda x: x.get('lastTimestamp', 0), reverse=True)

        return {'sessions': sessions}

    def parse_session_file(self, filepath, project_path):
        """解析会话文件的基本信息"""
        summary = ''
        first_user_msg = ''
        first_timestamp = None
        last_timestamp = None
        message_count = 0

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)

                    if item.get('type') == 'summary':
                        summary = item.get('summary', '')

                    if item.get('type') in ('user', 'assistant'):
                        message_count += 1
                        ts = item.get('timestamp')
                        if ts:
                            ts_val = ts if isinstance(ts, (int, float)) else 0
                            if isinstance(ts, str):
                                try:
                                    from datetime import datetime
                                    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                                    ts_val = dt.timestamp() * 1000
                                except:
                                    pass

                            if first_timestamp is None:
                                first_timestamp = ts_val
                            last_timestamp = ts_val

                        # 获取第一条用户消息作为备用标题
                        if not first_user_msg and item.get('type') == 'user':
                            msg = item.get('message', {})
                            content = msg.get('content', '')
                            if isinstance(content, str):
                                first_user_msg = content[:100]
                            elif isinstance(content, list):
                                for c in content:
                                    if c.get('type') == 'text':
                                        first_user_msg = c.get('text', '')[:100]
                                        break

                except json.JSONDecodeError:
                    continue

        if message_count == 0:
            return None

        return {
            'sessionId': filepath.stem,
            'filename': filepath.name,
            'filepath': str(filepath),
            'summary': summary or first_user_msg or '未命名对话',
            'project': project_path,
            'messageCount': message_count,
            'firstTimestamp': first_timestamp,
            'lastTimestamp': last_timestamp
        }

    def get_session_content(self, filepath):
        """获取完整会话内容"""
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                # 尝试在 projects 目录下查找
                for f in PROJECTS_DIR.rglob(filepath.name):
                    filepath = f
                    break

            messages = []
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                        if item.get('type') in ('user', 'assistant'):
                            messages.append({
                                'type': item.get('type'),
                                'role': item.get('message', {}).get('role', item.get('type')),
                                'content': item.get('message', {}).get('content', ''),
                                'timestamp': item.get('timestamp'),
                                'uuid': item.get('uuid')
                            })
                    except json.JSONDecodeError:
                        continue

            return {'messages': messages}

        except Exception as e:
            return {'error': str(e), 'messages': []}

    def log_message(self, format, *args):
        # 简化日志输出
        if '/api/' in args[0]:
            print(f"API: {args[0]}")


def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         Claude Code 历史记录查看器 - 本地服务器              ║
╠══════════════════════════════════════════════════════════════╣
║  历史目录: {str(PROJECTS_DIR):<48} ║
║  服务地址: http://localhost:{PORT:<37} ║
║  按 Ctrl+C 停止服务                                          ║
╚══════════════════════════════════════════════════════════════╝
    """)

    with socketserver.TCPServer(("", PORT), ClaudeHistoryHandler) as httpd:
        # 自动打开浏览器
        url = f"http://localhost:{PORT}/claude-history-viewer.html?auto=1"
        webbrowser.open(url)
        print(f"浏览器已打开: {url}\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务已停止")


if __name__ == '__main__':
    main()
