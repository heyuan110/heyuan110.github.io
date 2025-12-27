/**
 * 简单的 WebSocket 测试服务器
 * 运行: node ws-server.js
 * 连接: ws://127.0.0.1:8080
 */

const http = require('http');
const crypto = require('crypto');

const PORT = 8080;

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('WebSocket Server is running. Connect via ws://127.0.0.1:8080');
});

server.on('upgrade', (req, socket) => {
    // 获取 WebSocket 密钥
    const key = req.headers['sec-websocket-key'];
    const acceptKey = crypto
        .createHash('sha1')
        .update(key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
        .digest('base64');

    // 发送握手响应
    const responseHeaders = [
        'HTTP/1.1 101 Switching Protocols',
        'Upgrade: websocket',
        'Connection: Upgrade',
        `Sec-WebSocket-Accept: ${acceptKey}`,
        '',
        ''
    ].join('\r\n');

    socket.write(responseHeaders);

    const clientAddr = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log(`[${timestamp()}] ✅ 客户端已连接: ${clientAddr}`);

    // 发送欢迎消息
    sendMessage(socket, JSON.stringify({
        type: 'welcome',
        message: '欢迎连接到 WebSocket 测试服务器！',
        time: new Date().toISOString()
    }));

    // 处理接收的数据
    socket.on('data', (buffer) => {
        const message = parseFrame(buffer);
        if (message !== null) {
            console.log(`[${timestamp()}] 📥 收到消息: ${message}`);

            // 根据消息类型响应
            let response;
            try {
                const data = JSON.parse(message);
                response = handleJsonMessage(data);
            } catch (e) {
                response = handleTextMessage(message);
            }

            console.log(`[${timestamp()}] 📤 发送响应: ${response}`);
            sendMessage(socket, response);
        }
    });

    socket.on('close', () => {
        console.log(`[${timestamp()}] ❌ 客户端断开: ${clientAddr}`);
    });

    socket.on('error', (err) => {
        console.log(`[${timestamp()}] ⚠️ 错误: ${err.message}`);
    });
});

// 处理 JSON 消息
function handleJsonMessage(data) {
    const response = {
        type: 'response',
        originalType: data.type || 'unknown',
        time: new Date().toISOString()
    };

    switch (data.type) {
        case 'ping':
            response.message = 'pong';
            break;
        case 'echo':
            response.message = data.message || data;
            break;
        case 'time':
            response.message = `当前服务器时间: ${new Date().toLocaleString('zh-CN')}`;
            break;
        case 'subscribe':
            response.message = `已订阅频道: ${data.channel || 'default'}`;
            break;
        default:
            response.message = `收到 JSON 消息`;
            response.echo = data;
    }

    return JSON.stringify(response);
}

// 处理文本消息
function handleTextMessage(message) {
    const lower = message.toLowerCase().trim();

    switch (lower) {
        case 'ping':
            return 'pong';
        case 'pong':
            return 'ping';
        case 'hello':
            return '你好！这是 WebSocket 测试服务器的回复。';
        case 'time':
            return `服务器时间: ${new Date().toLocaleString('zh-CN')}`;
        case 'help':
            return '可用命令: ping, pong, hello, time, help, echo <消息>';
        default:
            if (lower.startsWith('echo ')) {
                return message.substring(5);
            }
            return `服务器回显: ${message}`;
    }
}

// 解析 WebSocket 帧
function parseFrame(buffer) {
    if (buffer.length < 2) return null;

    const secondByte = buffer[1];
    const isMasked = (secondByte & 0x80) !== 0;
    let payloadLength = secondByte & 0x7f;
    let offset = 2;

    if (payloadLength === 126) {
        payloadLength = buffer.readUInt16BE(2);
        offset = 4;
    } else if (payloadLength === 127) {
        payloadLength = Number(buffer.readBigUInt64BE(2));
        offset = 10;
    }

    let mask;
    if (isMasked) {
        mask = buffer.slice(offset, offset + 4);
        offset += 4;
    }

    const payload = buffer.slice(offset, offset + payloadLength);

    if (isMasked) {
        for (let i = 0; i < payload.length; i++) {
            payload[i] ^= mask[i % 4];
        }
    }

    return payload.toString('utf8');
}

// 发送 WebSocket 消息
function sendMessage(socket, message) {
    const payload = Buffer.from(message);
    const length = payload.length;

    let frame;
    if (length < 126) {
        frame = Buffer.alloc(2 + length);
        frame[0] = 0x81; // 文本帧
        frame[1] = length;
        payload.copy(frame, 2);
    } else if (length < 65536) {
        frame = Buffer.alloc(4 + length);
        frame[0] = 0x81;
        frame[1] = 126;
        frame.writeUInt16BE(length, 2);
        payload.copy(frame, 4);
    } else {
        frame = Buffer.alloc(10 + length);
        frame[0] = 0x81;
        frame[1] = 127;
        frame.writeBigUInt64BE(BigInt(length), 2);
        payload.copy(frame, 10);
    }

    socket.write(frame);
}

// 时间戳
function timestamp() {
    return new Date().toLocaleTimeString('zh-CN');
}

server.listen(PORT, () => {
    console.log('');
    console.log('╔════════════════════════════════════════════╗');
    console.log('║     🔌 WebSocket 测试服务器已启动          ║');
    console.log('╠════════════════════════════════════════════╣');
    console.log(`║  地址: ws://127.0.0.1:${PORT}                  ║`);
    console.log('║  按 Ctrl+C 停止服务器                      ║');
    console.log('╠════════════════════════════════════════════╣');
    console.log('║  支持的命令:                               ║');
    console.log('║  • ping / pong - 心跳测试                  ║');
    console.log('║  • hello - 问候消息                        ║');
    console.log('║  • time - 获取服务器时间                   ║');
    console.log('║  • echo <消息> - 回显消息                  ║');
    console.log('║  • 任意文本 - 服务器会回显                 ║');
    console.log('║  • JSON 格式消息也支持                     ║');
    console.log('╚════════════════════════════════════════════╝');
    console.log('');
});
