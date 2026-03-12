+++
title = 'Shell 特殊变量完全指南：$$、$?、$@、$# 等用法详解'
date = '2026-01-22T15:47:58+08:00'
description = 'Bash Shell 特殊变量完全指南，详解 $$、$!、$?、$-、$*、$@、$#、$0 等变量的含义和实际用法。包含 $* 与 $@ 的区别对比、退出状态码说明、完整示例代码和最佳实践。'
toc = true
tags = ['Shell', 'Bash', 'Linux', 'Scripting']
categories = ['Linux']
keywords = ['Shell 特殊变量', 'Bash 变量', '$@ $* 区别', 'Shell 脚本', 'Linux 变量']
+++
![Shell 特殊变量完全指南，掌握 Bash 脚本的核心知识](cover.webp)

编写 Shell 脚本时，你一定见过 `$?`、`$@`、`$$` 这些以美元符号开头的特殊变量。它们是 Bash 内置的**特殊参数**，用于获取脚本运行状态、命令行参数等关键信息。掌握这些变量，是写出健壮 Shell 脚本的基础。

本文将系统讲解每个特殊变量的含义、使用场景，并通过实际示例帮助你深入理解。

<!--more-->

## 一、特殊变量速查表

先来看一个快速参考表，方便日后查阅：

| 变量 | 含义 | 示例值 |
|------|------|--------|
| `$0` | 当前脚本的文件名 | `./test.sh` |
| `$1`~`$9` | 第 1~9 个位置参数 | `arg1` |
| `${10}` | 第 10 个及以后的参数（需要大括号） | `arg10` |
| `$#` | 传入参数的个数（不含 `$0`） | `3` |
| `$*` | 所有参数，作为**一个字符串** | `"arg1 arg2 arg3"` |
| `$@` | 所有参数，作为**独立字符串数组** | `"arg1" "arg2" "arg3"` |
| `$?` | 上一条命令的退出状态码 | `0`（成功） |
| `$$` | 当前 Shell 进程的 PID | `12345` |
| `$!` | 最近一个后台进程的 PID | `12346` |
| `$-` | 当前 Shell 的选项标志 | `himBHs` |
| `$_` | 上一条命令的最后一个参数 | `/path/to/file` |

> 记忆技巧：`$#` 的 `#` 像是在数数（count），`$?` 的 `?` 像是在问"结果如何"，`$$` 两个 `$` 表示"我自己的身份"。

---

## 二、位置参数详解

### 1. $0 - 脚本名称

`$0` 保存当前执行脚本的名称（包含路径）。

```bash
#!/bin/bash
echo "脚本名称: $0"
```

**运行结果：**

```bash
$ ./scripts/deploy.sh
脚本名称: ./scripts/deploy.sh

$ bash /home/user/scripts/deploy.sh
脚本名称: /home/user/scripts/deploy.sh
```

**应用场景**：打印帮助信息时显示正确的脚本名。

```bash
usage() {
    echo "用法: $0 [选项] <参数>"
    echo "示例: $0 -f config.yml"
}
```

### 2. $1~$9 和 ${n} - 位置参数

`$1` 到 `$9` 分别表示传入脚本的第 1 到第 9 个参数。超过 9 个时，必须用 `${10}`、`${11}` 这种大括号形式。

```bash
#!/bin/bash
echo "第一个参数: $1"
echo "第二个参数: $2"
echo "第十个参数: ${10}"
```

**注意**：如果写成 `$10`，Shell 会解析为 `$1` 加上字符 `0`，而不是第 10 个参数。

### 3. $# - 参数个数

`$#` 返回传入参数的数量，**不包括 `$0`**。

```bash
#!/bin/bash
echo "参数个数: $#"

if [ $# -lt 2 ]; then
    echo "错误: 至少需要 2 个参数"
    exit 1
fi
```

**运行结果：**

```bash
$ ./test.sh a b c
参数个数: 3

$ ./test.sh
参数个数: 0
```

---

## 三、$* 与 $@ 的区别（重点）

![终端中运行 Shell 脚本的示例](terminal.webp)

这两个变量都表示"所有参数"，但在加引号时行为不同。这是 Shell 脚本面试中的经典问题。

### 不加引号时：行为相同

```bash
#!/bin/bash
echo "使用 \$*:"
for arg in $*; do
    echo "  - $arg"
done

echo "使用 \$@:"
for arg in $@; do
    echo "  - $arg"
done
```

**运行 `./test.sh "hello world" foo bar`：**

```
使用 $*:
  - hello
  - world
  - foo
  - bar
使用 $@:
  - hello
  - world
  - foo
  - bar
```

不加引号时，包含空格的参数 `"hello world"` 被拆分成两个词。

### 加引号时：关键区别

```bash
#!/bin/bash
echo "使用 \"\$*\":"
for arg in "$*"; do
    echo "  [$arg]"
done

echo "使用 \"\$@\":"
for arg in "$@"; do
    echo "  [$arg]"
done
```

**运行 `./test.sh "hello world" foo bar`：**

```
使用 "$*":
  [hello world foo bar]
使用 "$@":
  [hello world]
  [foo]
  [bar]
```

### 区别总结

| 形式 | 结果 | 说明 |
|------|------|------|
| `$*` | `hello world foo bar` | 所有参数拆分为单词 |
| `$@` | `hello world foo bar` | 所有参数拆分为单词 |
| `"$*"` | `"hello world foo bar"` | **一个**字符串 |
| `"$@"` | `"hello world" "foo" "bar"` | **三个**独立字符串 |

> **最佳实践**：几乎所有情况下都应该使用 `"$@"`，它能正确保留参数中的空格和特殊字符。

---

## 四、进程相关变量

### 1. $$ - 当前进程 PID

`$$` 返回当前 Shell 脚本运行时的进程 ID，常用于创建临时文件。

```bash
#!/bin/bash
TEMP_FILE="/tmp/myapp_$$.tmp"
echo "临时文件: $TEMP_FILE"
echo "数据内容" > "$TEMP_FILE"

# 脚本结束时清理
trap "rm -f $TEMP_FILE" EXIT
```

**为什么用 PID？** 保证文件名唯一，避免多个脚本实例冲突。

### 2. $! - 后台进程 PID

`$!` 保存最近一个后台执行命令的进程 ID。

```bash
#!/bin/bash
# 启动后台任务
long_running_task &
TASK_PID=$!

echo "后台任务 PID: $TASK_PID"

# 等待任务完成
wait $TASK_PID
echo "任务已完成"
```

**应用场景**：管理后台进程、实现超时控制。

```bash
#!/bin/bash
# 带超时的命令执行
slow_command &
PID=$!

# 5秒后检查
sleep 5
if kill -0 $PID 2>/dev/null; then
    echo "命令执行超时，终止进程"
    kill $PID
fi
```

---

## 五、退出状态 $?

`$?` 保存上一条命令的退出状态码（Exit Code），是脚本流程控制的核心。

### 状态码含义

| 状态码 | 含义 |
|--------|------|
| `0` | 命令执行成功 |
| `1` | 通用错误 |
| `2` | 命令使用错误（如参数错误） |
| `126` | 命令存在但无执行权限 |
| `127` | 命令不存在 |
| `128+N` | 被信号 N 终止 |
| `130` | 被 Ctrl+C 中断（128+2） |
| `255` | 退出码超出范围 |

### 实际应用

```bash
#!/bin/bash
# 检查命令是否成功
grep "error" /var/log/app.log
if [ $? -eq 0 ]; then
    echo "发现错误日志"
else
    echo "没有错误"
fi

# 更简洁的写法
if grep -q "error" /var/log/app.log; then
    echo "发现错误日志"
fi
```

### 设置脚本退出码

使用 `exit` 命令设置脚本的退出状态码：

```bash
#!/bin/bash
if [ ! -f "$1" ]; then
    echo "错误: 文件不存在" >&2
    exit 1
fi

# 正常执行
process_file "$1"
exit 0
```

---

## 六、Shell 选项 $-

`$-` 显示当前 Shell 启用的选项标志。

```bash
$ echo $-
himBHs
```

常见标志含义：

| 标志 | 含义 |
|------|------|
| `h` | hashall - 记住命令位置 |
| `i` | interactive - 交互式 Shell |
| `m` | monitor - 作业控制 |
| `B` | braceexpand - 启用花括号展开 |
| `H` | histexpand - 启用历史展开 |
| `s` | stdin - 从标准输入读取命令 |

**应用场景**：判断脚本是否在交互式 Shell 中运行。

```bash
#!/bin/bash
case $- in
    *i*) echo "交互式 Shell" ;;
    *)   echo "非交互式 Shell" ;;
esac
```

---

## 七、完整示例脚本

下面是一个综合运用特殊变量的实用脚本：

```bash
#!/bin/bash
# 文件: show_vars.sh
# 说明: 演示 Shell 特殊变量的用法

echo "===== 基本信息 ====="
echo "脚本名称: $0"
echo "进程 PID: $$"
echo "参数个数: $#"
echo "Shell 选项: $-"

echo ""
echo "===== 位置参数 ====="
echo "第一个参数: ${1:-'(空)'}"
echo "第二个参数: ${2:-'(空)'}"
echo "第三个参数: ${3:-'(空)'}"

echo ""
echo '===== $* vs $@ ====='
echo "使用 \"\$*\":"
for arg in "$*"; do
    echo "  -> [$arg]"
done

echo "使用 \"\$@\":"
for arg in "$@"; do
    echo "  -> [$arg]"
done

echo ""
echo "===== 退出状态演示 ====="
ls /nonexistent 2>/dev/null
echo "ls 不存在目录的退出码: $?"

ls / >/dev/null
echo "ls 存在目录的退出码: $?"

echo ""
echo "===== 后台进程 ====="
sleep 1 &
echo "后台进程 PID: $!"
wait
echo "后台进程已结束"
```

**运行结果：**

```bash
$ ./show_vars.sh "hello world" foo bar

===== 基本信息 =====
脚本名称: ./show_vars.sh
进程 PID: 28547
参数个数: 3
Shell 选项: hB

===== 位置参数 =====
第一个参数: hello world
第二个参数: foo
第三个参数: bar

===== $* vs $@ =====
使用 "$*":
  -> [hello world foo bar]
使用 "$@":
  -> [hello world]
  -> [foo]
  -> [bar]

===== 退出状态演示 =====
ls 不存在目录的退出码: 2
ls 存在目录的退出码: 0

===== 后台进程 =====
后台进程 PID: 28548
后台进程已结束
```

---

## 八、最佳实践

### 1. 始终用 "$@" 而不是 $*

```bash
# 推荐
for arg in "$@"; do
    process "$arg"
done

# 不推荐
for arg in $*; do
    process "$arg"
done
```

### 2. 检查参数数量

```bash
if [ $# -eq 0 ]; then
    echo "用法: $0 <文件名>" >&2
    exit 1
fi
```

### 3. 使用有意义的退出码

```bash
readonly E_SUCCESS=0
readonly E_NO_ARGS=1
readonly E_FILE_NOT_FOUND=2

if [ $# -eq 0 ]; then
    exit $E_NO_ARGS
fi
```

### 4. 临时文件使用 $$ 确保唯一

```bash
TMPFILE="/tmp/${0##*/}.$$"
trap "rm -f $TMPFILE" EXIT
```

---

## 总结

Shell 特殊变量是脚本编程的基础工具：

- **位置参数**（`$0`~`$9`、`$#`、`$@`）用于处理命令行输入
- **进程变量**（`$$`、`$!`）用于进程管理和临时文件
- **状态变量**（`$?`）用于流程控制和错误处理
- **`"$@"`** 几乎总是比 `$*` 更安全的选择

掌握这些变量，你就能写出更健壮、更专业的 Shell 脚本。

---

## 相关阅读

- [Oh My Zsh 安装配置指南：打造高效终端环境](/posts/linux/2015-06-17-shell-zsh/) - 强大的 Zsh 配置框架
- [Linux/macOS 常用命令速查手册](/posts/linux/2020-03-19-linux-mac-commands/) - 运维开发常用命令参考

## 参考资料

- [Bash Reference Manual - Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)
- [Shell 传递参数 - 菜鸟教程](https://www.runoob.com/linux/linux-shell-passing-arguments.html)
- [Bash Special Variables - Linux Handbook](https://linuxhandbook.com/bash-special-variables/)
- [Devhints - Bash Scripting Cheatsheet](https://devhints.io/bash)
