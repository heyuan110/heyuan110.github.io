+++
title = 'Bash Special Variables Explained: $$, $?, $@, $# and More'
date = '2026-01-22T15:47:58+08:00'
description = 'A complete guide to Bash special variables including $$, $!, $?, $-, $*, $@, $#, and $0. Learn the difference between $* and $@, exit status codes, and best practices with practical examples.'
toc = true
tags = ['Shell', 'Bash', 'Linux', 'Scripting']
categories = ['Linux']
keywords = ['Bash special variables', 'Shell variables', '$@ vs $* difference', 'Shell scripting', 'Linux variables', 'exit status code']
+++
![A complete guide to Bash special variables for Shell scripting](cover.webp)

If you have written any Bash scripts, you have almost certainly encountered cryptic-looking variables like `$?`, `$@`, and `$$`. These are **special parameters** built into Bash that give you access to script metadata, command-line arguments, and process information. Understanding them is essential for writing robust Shell scripts.

This guide walks through every special variable with clear explanations, real-world use cases, and runnable examples.

<!--more-->

## Quick Reference Table

Here is a cheat sheet you can bookmark for later:

| Variable | Meaning | Example Value |
|----------|---------|---------------|
| `$0` | Name of the current script | `./test.sh` |
| `$1`–`$9` | Positional parameters 1 through 9 | `arg1` |
| `${10}` | 10th parameter and beyond (braces required) | `arg10` |
| `$#` | Number of arguments (excluding `$0`) | `3` |
| `$*` | All arguments as a **single string** | `"arg1 arg2 arg3"` |
| `$@` | All arguments as **separate strings** | `"arg1" "arg2" "arg3"` |
| `$?` | Exit status of the last command | `0` (success) |
| `$$` | PID of the current Shell process | `12345` |
| `$!` | PID of the most recent background process | `12346` |
| `$-` | Current Shell option flags | `himBHs` |
| `$_` | Last argument of the previous command | `/path/to/file` |

> **Memory trick:** The `#` in `$#` looks like it is counting, the `?` in `$?` is asking "how did it go?", and the double `$` in `$$` means "my own identity."

---

## Positional Parameters

### $0 — Script Name

`$0` holds the name (including path) of the currently running script.

```bash
#!/bin/bash
echo "Script name: $0"
```

**Output:**

```bash
$ ./scripts/deploy.sh
Script name: ./scripts/deploy.sh

$ bash /home/user/scripts/deploy.sh
Script name: /home/user/scripts/deploy.sh
```

**Common use case:** displaying the correct script name in help messages.

```bash
usage() {
    echo "Usage: $0 [options] <argument>"
    echo "Example: $0 -f config.yml"
}
```

### $1–$9 and ${n} — Positional Parameters

`$1` through `$9` represent the first through ninth arguments passed to the script. For the 10th argument and beyond, you must use braces: `${10}`, `${11}`, etc.

```bash
#!/bin/bash
echo "First argument: $1"
echo "Second argument: $2"
echo "Tenth argument: ${10}"
```

**Watch out:** Writing `$10` without braces is interpreted as `$1` followed by the literal character `0`, not as the tenth parameter.

### $# — Argument Count

`$#` returns the number of arguments passed to the script, **excluding `$0`**.

```bash
#!/bin/bash
echo "Number of arguments: $#"

if [ $# -lt 2 ]; then
    echo "Error: at least 2 arguments required"
    exit 1
fi
```

**Output:**

```bash
$ ./test.sh a b c
Number of arguments: 3

$ ./test.sh
Number of arguments: 0
```

---

## $* vs $@ — The Critical Difference

![Example of running a Shell script in the terminal](terminal.webp)

Both variables represent "all arguments," but they behave very differently when quoted. This is a classic Shell scripting interview question.

### Without Quotes: Identical Behavior

```bash
#!/bin/bash
echo "Using \$*:"
for arg in $*; do
    echo "  - $arg"
done

echo "Using \$@:"
for arg in $@; do
    echo "  - $arg"
done
```

**Running `./test.sh "hello world" foo bar`:**

```
Using $*:
  - hello
  - world
  - foo
  - bar
Using $@:
  - hello
  - world
  - foo
  - bar
```

Without quotes, the argument `"hello world"` gets split into two separate words by word splitting.

### With Quotes: The Key Difference

```bash
#!/bin/bash
echo "Using \"\$*\":"
for arg in "$*"; do
    echo "  [$arg]"
done

echo "Using \"\$@\":"
for arg in "$@"; do
    echo "  [$arg]"
done
```

**Running `./test.sh "hello world" foo bar`:**

```
Using "$*":
  [hello world foo bar]
Using "$@":
  [hello world]
  [foo]
  [bar]
```

### Summary

| Form | Result | Explanation |
|------|--------|-------------|
| `$*` | `hello world foo bar` | All arguments subject to word splitting |
| `$@` | `hello world foo bar` | All arguments subject to word splitting |
| `"$*"` | `"hello world foo bar"` | Everything joined into **one** string |
| `"$@"` | `"hello world" "foo" "bar"` | Each argument preserved as a **separate** string |

> **Best practice:** Almost always use `"$@"`. It correctly preserves spaces and special characters within arguments.

---

## Process-Related Variables

### $$ — Current Process PID

`$$` returns the process ID of the running Shell script. It is commonly used to create unique temporary files.

```bash
#!/bin/bash
TEMP_FILE="/tmp/myapp_$$.tmp"
echo "Temp file: $TEMP_FILE"
echo "some data" > "$TEMP_FILE"

# Clean up on exit
trap "rm -f $TEMP_FILE" EXIT
```

**Why use the PID?** It guarantees a unique filename, preventing collisions when multiple instances of the script run simultaneously.

### $! — Background Process PID

`$!` stores the process ID of the most recently backgrounded command.

```bash
#!/bin/bash
# Start a background task
long_running_task &
TASK_PID=$!

echo "Background task PID: $TASK_PID"

# Wait for it to finish
wait $TASK_PID
echo "Task completed"
```

**Use case:** managing background processes and implementing timeouts.

```bash
#!/bin/bash
# Run a command with a timeout
slow_command &
PID=$!

# Check after 5 seconds
sleep 5
if kill -0 $PID 2>/dev/null; then
    echo "Command timed out, killing process"
    kill $PID
fi
```

---

## Exit Status — $?

`$?` holds the exit status code of the last executed command. It is the backbone of flow control in Shell scripts.

### Exit Code Reference

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `2` | Misuse of command (e.g., invalid arguments) |
| `126` | Command found but not executable |
| `127` | Command not found |
| `128+N` | Terminated by signal N |
| `130` | Interrupted by Ctrl+C (128+2) |
| `255` | Exit code out of range |

### Practical Usage

```bash
#!/bin/bash
# Check whether a command succeeded
grep "error" /var/log/app.log
if [ $? -eq 0 ]; then
    echo "Errors found in log"
else
    echo "No errors"
fi

# A cleaner approach
if grep -q "error" /var/log/app.log; then
    echo "Errors found in log"
fi
```

### Setting Your Own Exit Codes

Use the `exit` command to return a specific status from your script:

```bash
#!/bin/bash
if [ ! -f "$1" ]; then
    echo "Error: file not found" >&2
    exit 1
fi

# Normal execution
process_file "$1"
exit 0
```

---

## Shell Option Flags — $-

`$-` shows the option flags currently enabled in the Shell.

```bash
$ echo $-
himBHs
```

Common flags:

| Flag | Meaning |
|------|---------|
| `h` | hashall — remember command locations |
| `i` | interactive — this is an interactive Shell |
| `m` | monitor — job control enabled |
| `B` | braceexpand — brace expansion enabled |
| `H` | histexpand — history expansion enabled |
| `s` | stdin — reading commands from standard input |

**Use case:** detecting whether a script is running in an interactive Shell.

```bash
#!/bin/bash
case $- in
    *i*) echo "Interactive Shell" ;;
    *)   echo "Non-interactive Shell" ;;
esac
```

---

## Putting It All Together

Here is a comprehensive script that demonstrates every special variable in action:

```bash
#!/bin/bash
# File: show_vars.sh
# Demonstrates Bash special variables

echo "===== Basic Info ====="
echo "Script name: $0"
echo "Process PID: $$"
echo "Argument count: $#"
echo "Shell options: $-"

echo ""
echo "===== Positional Parameters ====="
echo "First argument: ${1:-'(empty)'}"
echo "Second argument: ${2:-'(empty)'}"
echo "Third argument: ${3:-'(empty)'}"

echo ""
echo '===== $* vs $@ ====='
echo "Using \"\$*\":"
for arg in "$*"; do
    echo "  -> [$arg]"
done

echo "Using \"\$@\":"
for arg in "$@"; do
    echo "  -> [$arg]"
done

echo ""
echo "===== Exit Status Demo ====="
ls /nonexistent 2>/dev/null
echo "Exit code for missing directory: $?"

ls / >/dev/null
echo "Exit code for existing directory: $?"

echo ""
echo "===== Background Process ====="
sleep 1 &
echo "Background PID: $!"
wait
echo "Background process finished"
```

**Output:**

```bash
$ ./show_vars.sh "hello world" foo bar

===== Basic Info =====
Script name: ./show_vars.sh
Process PID: 28547
Argument count: 3
Shell options: hB

===== Positional Parameters =====
First argument: hello world
Second argument: foo
Third argument: bar

===== $* vs $@ =====
Using "$*":
  -> [hello world foo bar]
Using "$@":
  -> [hello world]
  -> [foo]
  -> [bar]

===== Exit Status Demo =====
Exit code for missing directory: 2
Exit code for existing directory: 0

===== Background Process =====
Background PID: 28548
Background process finished
```

---

## Best Practices

### 1. Always Use "$@" Instead of $*

```bash
# Recommended
for arg in "$@"; do
    process "$arg"
done

# Avoid — breaks on arguments with spaces
for arg in $*; do
    process "$arg"
done
```

### 2. Validate Argument Count Early

```bash
if [ $# -eq 0 ]; then
    echo "Usage: $0 <filename>" >&2
    exit 1
fi
```

### 3. Use Meaningful Exit Codes

```bash
readonly E_SUCCESS=0
readonly E_NO_ARGS=1
readonly E_FILE_NOT_FOUND=2

if [ $# -eq 0 ]; then
    exit $E_NO_ARGS
fi
```

### 4. Use $$ for Unique Temp Files

```bash
TMPFILE="/tmp/${0##*/}.$$"
trap "rm -f $TMPFILE" EXIT
```

---

## Summary

Bash special variables are fundamental tools for scripting:

- **Positional parameters** (`$0`–`$9`, `$#`, `$@`) handle command-line input
- **Process variables** (`$$`, `$!`) manage processes and temp files
- **Exit status** (`$?`) drives flow control and error handling
- **`"$@"`** is almost always the safer choice over `$*`

Master these variables and you will write cleaner, more reliable Shell scripts.

---

## Further Reading

- [Oh My Zsh Setup Guide: Build a Productive Terminal](/posts/linux/2015-06-17-shell-zsh/) — A powerful Zsh configuration framework
- [Linux/macOS Command Cheat Sheet](/posts/linux/2020-03-19-linux-mac-commands/) — Common commands for daily use

## References

- [Bash Reference Manual - Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)
- [Bash Special Variables - Linux Handbook](https://linuxhandbook.com/bash-special-variables/)
- [Devhints - Bash Scripting Cheatsheet](https://devhints.io/bash)
