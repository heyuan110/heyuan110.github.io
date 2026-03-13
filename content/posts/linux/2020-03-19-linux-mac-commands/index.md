+++
date = '2020-03-19T10:55:52+08:00'
title = 'Linux and macOS Command Cheat Sheet for Developers'
description = 'Essential Linux and macOS command reference covering networking, process management, file operations, text processing, disk management, and macOS-specific tips — with practical examples for each command.'
toc = true
tags = ['Linux', 'macOS', 'Shell', '命令行', '运维']
categories = ['Linux']
keywords = ['Linux commands cheat sheet', 'macOS terminal commands', 'shell command reference', 'Linux networking commands', 'developer command line tools']
+++

The command line is an essential skill for every developer. This reference organizes the most frequently used Linux and macOS commands by category for quick lookup.

## Networking

### netstat — View Network Connections

**Linux:**
```bash
# Check which process is using a specific port
netstat -ntlp | grep 3000

# Find network connections for a specific process
netstat -ntlp | grep nginx

# List all listening ports
netstat -tuln
```

**macOS:**
```bash
# Check a specific port
netstat -an | grep 3306

# List all listening ports
netstat -an | grep LISTEN
```

> On Linux, you need `sudo` to see process names in netstat output.

### lsof — List Open Files and Ports

```bash
# Check what is using a port (most common use)
lsof -i:80
lsof -i:3000

# List all listening ports
sudo lsof -i -P | grep LISTEN

# List files opened by a specific process
lsof -p <PID>

# List files opened by a specific user
lsof -u username
```

### ss — A Faster netstat Alternative

```bash
# Show all TCP connections
ss -t

# List all listening ports
ss -tuln

# Filter by port
ss -tuln | grep :80

# Show socket statistics summary
ss -s
```

### ping and telnet — Connectivity Testing

```bash
# Test network connectivity
ping google.com

# Limit to a specific number of packets
ping -c 4 google.com

# Test TCP port connectivity
telnet 192.168.1.1 3306

# On macOS, use nc instead of telnet
nc -zv 192.168.1.1 3306
```

### dig and nslookup — DNS Queries

```bash
# Query A records
dig example.com

# Query specific record types
dig example.com MX
dig example.com TXT

# Use a specific DNS server
dig @8.8.8.8 example.com

# Get a concise answer
dig +short example.com

# Alternative: nslookup
nslookup example.com
```

### ifconfig and ip — Network Interface Information

```bash
# View network interfaces
ifconfig
ifconfig en0    # macOS: view a specific interface

# Linux: prefer the ip command
ip addr
ip addr show eth0
ip route        # View routing table
```

---

## Process Management

### ps — View Running Processes

```bash
# List all processes (most common)
ps aux
ps -ef

# Search for a specific process
ps aux | grep nginx
ps -ef | grep java

# Sort by CPU or memory usage
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10

# Show process tree (Linux)
ps auxf
pstree
```

### kill — Terminate Processes

```bash
# Graceful termination
kill <PID>

# Force kill
kill -9 <PID>

# Kill by name
pkill nginx
killall nginx

# Common signals:
# -1  (HUP)   Reload configuration
# -9  (KILL)  Force terminate
# -15 (TERM)  Graceful terminate (default)
```

### top and htop — Real-Time Monitoring

```bash
# Real-time system resource monitor
top

# Useful top shortcuts:
# P — Sort by CPU
# M — Sort by memory
# k — Kill a process
# q — Quit

# htop (friendlier interface, requires installation)
htop
```

### nohup — Background Execution

```bash
# Run in background, immune to hangup signals
nohup ./script.sh &

# Redirect all output to a file
nohup ./script.sh > output.log 2>&1 &

# View background jobs
jobs

# Switch between foreground and background
bg %1    # Send to background
fg %1    # Bring to foreground
```

### systemctl — Service Management (Linux)

```bash
# Start, stop, restart a service
systemctl start nginx
systemctl stop nginx
systemctl restart nginx

# Check service status
systemctl status nginx

# Enable or disable auto-start on boot
systemctl enable nginx
systemctl disable nginx

# List all running services
systemctl list-units --type=service --state=running
```

---

## File Operations

### find — Search for Files

```bash
# Search by name
find /path -name "*.log"
find . -name "config.yml"

# Case-insensitive search
find . -iname "readme*"

# Search by type
find . -type f    # Files only
find . -type d    # Directories only

# Search by modification time
find . -mtime -7     # Modified within the last 7 days
find . -mtime +30    # Modified more than 30 days ago

# Search by size
find . -size +100M   # Larger than 100 MB
find . -size -1k     # Smaller than 1 KB

# Execute a command on results
find . -name "*.tmp" -delete
find . -name "*.log" -exec rm {} \;
find . -type f -name "*.txt" -exec grep "keyword" {} \;
```

### chmod and chown — Permissions

```bash
# Change permissions
chmod 755 script.sh
chmod +x script.sh      # Add execute permission
chmod -R 644 ./dir      # Recursive

# Permission digits:
# 7 = rwx (read, write, execute)
# 6 = rw- (read, write)
# 5 = r-x (read, execute)
# 4 = r-- (read only)

# Change ownership
chown user:group file
chown -R user:group ./dir
```

### tar — Archive and Compress

```bash
# Create compressed archives
tar -czvf archive.tar.gz ./dir
tar -cjvf archive.tar.bz2 ./dir

# Extract
tar -xzvf archive.tar.gz
tar -xzvf archive.tar.gz -C /target/dir

# List archive contents
tar -tzvf archive.tar.gz

# Flag reference:
# c — create
# x — extract
# z — gzip compression
# j — bzip2 compression
# v — verbose output
# f — specify filename
```

### ln — Symbolic and Hard Links

```bash
# Create a symbolic link (most common)
ln -s /path/to/source /path/to/link

# Create a hard link
ln /path/to/source /path/to/link

# Check where a link points
ls -la
readlink /path/to/link
```

### rsync — Efficient File Synchronization

```bash
# Local sync
rsync -av source/ dest/

# Remote sync
rsync -avz source/ user@host:/path/dest/

# Common options:
# -a  Archive mode (preserves permissions, timestamps, etc.)
# -v  Verbose
# -z  Compress during transfer
# --delete  Remove extra files in destination
# --exclude  Exclude files matching a pattern

# Exclude specific files
rsync -av --exclude='*.log' source/ dest/
```

---

## Text Processing

### grep — Search Text

```bash
# Basic search
grep "keyword" file.txt

# Recursive search across a directory
grep -r "keyword" ./dir

# Case-insensitive
grep -i "keyword" file.txt

# Show line numbers
grep -n "keyword" file.txt

# Show context lines
grep -A 3 "keyword" file.txt   # 3 lines after
grep -B 3 "keyword" file.txt   # 3 lines before
grep -C 3 "keyword" file.txt   # 3 lines before and after

# Extended regex (OR matching)
grep -E "pattern1|pattern2" file.txt

# Invert match (exclude)
grep -v "keyword" file.txt

# Show only filenames with matches
grep -l "keyword" *.txt
```

### awk — Column-Based Text Processing

```bash
# Print specific columns
awk '{print $1}' file.txt
awk '{print $1, $3}' file.txt

# Custom field separator
awk -F: '{print $1}' /etc/passwd
awk -F',' '{print $2}' data.csv

# Filter by condition
awk '$3 > 100 {print $1, $3}' file.txt

# Sum a column
awk '{sum += $1} END {print sum}' file.txt

# Count lines
awk 'END {print NR}' file.txt
```

### sed — Stream Editor

```bash
# Replace text (print to stdout)
sed 's/old/new/' file.txt
sed 's/old/new/g' file.txt      # Replace all occurrences

# Edit file in place
sed -i 's/old/new/g' file.txt
sed -i.bak 's/old/new/g' file.txt  # Create backup first

# Delete lines
sed '/pattern/d' file.txt    # Delete matching lines
sed '1d' file.txt            # Delete the first line
sed '1,5d' file.txt          # Delete lines 1 through 5

# Print specific lines
sed -n '5p' file.txt         # Print line 5
sed -n '5,10p' file.txt      # Print lines 5 through 10
```

### sort and uniq — Sort and Deduplicate

```bash
# Sort
sort file.txt
sort -r file.txt       # Reverse order
sort -n file.txt       # Numeric sort
sort -k2 file.txt      # Sort by column 2

# Deduplicate (must sort first)
sort file.txt | uniq
sort file.txt | uniq -c    # Count occurrences
sort file.txt | uniq -d    # Show only duplicate lines
```

### head and tail — View File Beginning or End

```bash
# View first or last N lines
head -n 20 file.txt
tail -n 20 file.txt

# Follow a log file in real time (most common use)
tail -f app.log
tail -f -n 100 app.log     # Start from the last 100 lines

# Follow multiple files
tail -f *.log
```

### wc — Count Lines, Words, Characters

```bash
# Full count (lines, words, characters)
wc file.txt

# Count lines only
wc -l file.txt

# Count files in a directory
ls | wc -l
find . -type f | wc -l
```

---

## Disk Management

### df — Disk Usage Overview

```bash
# Show disk usage in human-readable format
df -h

# Check the partition for a specific directory
df -h /var

# Check inode usage
df -i
```

### du — Directory Size

```bash
# Show directory size
du -sh /var/log
du -sh *

# Sort by size
du -sh * | sort -hr

# Show subdirectory sizes (one level deep)
du -h --max-depth=1

# Find the largest files and directories
du -a /var | sort -rn | head -10
```

### ncdu — Interactive Disk Analyzer

```bash
# Install
sudo apt install ncdu    # Ubuntu
brew install ncdu        # macOS

# Run
ncdu /var
```

---

## System Information

### Basic System Info

```bash
# OS version
uname -a
cat /etc/os-release     # Linux
sw_vers                 # macOS

# Hostname
hostname

# Uptime and load average
uptime
```

### Hardware Info

```bash
# CPU information
cat /proc/cpuinfo       # Linux
sysctl -n machdep.cpu.brand_string  # macOS
nproc                   # Number of CPU cores

# Memory information
free -h                 # Linux
vm_stat                 # macOS

# Top 10 memory-consuming processes
ps aux --sort=-%mem | head -10
```

### Environment Variables

```bash
# View all environment variables
env
printenv

# View a specific variable
echo $PATH
echo $HOME

# Set temporarily (current session only)
export MY_VAR="value"

# Set permanently (add to shell config)
echo 'export MY_VAR="value"' >> ~/.zshrc
source ~/.zshrc
```

---

## Users and Permissions

### User Management

```bash
# Current user
whoami
id

# Switch user
su - username
sudo -u username command

# View logged-in users
who
w
last    # Login history
```

### sudo

```bash
# Run as root
sudo command

# Switch to root shell
sudo -i
sudo su -

# Edit sudoers file safely
sudo visudo
```

---

## Practical Tips

### Command History

```bash
# View command history
history
history | grep keyword

# Repeat the last command
!!

# Execute command N from history
!N

# Search history interactively
Ctrl + R
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + C` | Terminate current command |
| `Ctrl + Z` | Suspend current command |
| `Ctrl + D` | Exit terminal |
| `Ctrl + L` | Clear screen |
| `Ctrl + A` | Move cursor to beginning of line |
| `Ctrl + E` | Move cursor to end of line |
| `Ctrl + U` | Delete from cursor to beginning of line |
| `Ctrl + K` | Delete from cursor to end of line |
| `Ctrl + W` | Delete the previous word |
| `Ctrl + R` | Search command history |

### Pipes and Redirection

```bash
# Pipe output to another command
command1 | command2

# Redirect output to a file
command > file.txt      # Overwrite
command >> file.txt     # Append

# Redirect errors
command 2> error.log
command > output.log 2>&1   # Both stdout and stderr

# Redirect input
command < input.txt

# Discard all output
command > /dev/null 2>&1
```

### pv — Show Progress

```bash
# Install
sudo apt install pv     # Ubuntu
brew install pv         # macOS

# Copy with progress bar
pv source.iso > dest.iso

# Rate-limited copy
pv -L 2m source.iso > dest.iso

# MySQL import with progress
pv database.sql | mysql -u root -p dbname
```

---

## macOS-Specific Commands

### Allow Apps from Any Source

```bash
# Disable Gatekeeper
sudo spctl --master-disable

# Remove quarantine attribute from a specific app
sudo xattr -r -d com.apple.quarantine /Applications/xxx.app
```

### Clipboard Operations

```bash
# Copy to clipboard
cat file.txt | pbcopy
echo "hello" | pbcopy

# Paste from clipboard
pbpaste
pbpaste > file.txt
```

### Opening Files and Applications

```bash
# Open with default application
open file.pdf
open .                  # Open current directory in Finder
open -a "Visual Studio Code" file.txt
```

### System Management

```bash
# Check battery status
pmset -g batt

# Prevent sleep (caffeinate mode)
caffeinate -d           # Prevent display sleep
caffeinate -i           # Prevent system sleep

# Flush DNS cache
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

---

## References

- [Linux Command Manual (Runoob)](https://www.runoob.com/linux/linux-command-manual.html)
- [The Linux Command Line](https://linuxcommand.org/)
- [macOS Terminal User Guide](https://support.apple.com/guide/terminal/welcome/mac)

---

## Related Articles

- [Oh My Zsh Setup Guide](/posts/linux/2015-06-17-shell-zsh/)
- [Shell Script Special Variables Explained](/posts/linux/2019-05-13-linux-shell-vars/)
- [Linux curl Command Complete Guide](/posts/linux/2020-06-29-curl/)
- [Traceroute Command Explained](/posts/linux/2020-06-28-traceroute/)
- [Docker Common Commands Cheat Sheet](/posts/docker/2019-11-14-docker-commands/)
- [Docker Compose Complete Guide](/posts/docker/2026-01-19-docker-compose-complete-guide/)
- [docker-compose.yml Explained](/posts/docker/2026-01-24-docker-compose-yml-explained/)
