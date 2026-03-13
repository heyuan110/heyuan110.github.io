+++
date = '2018-10-07T00:35:04+08:00'
title = 'Supervisor Guide: Installation, Configuration, Troubleshooting & Comparison with systemd'
description = 'A practical guide to Supervisor for Linux process management — covering installation, configuration, common issues, and how it compares to systemd and PM2.'
toc = true
tags = ['supervisor', 'linux', '进程管理', 'systemd', '运维']
categories = ['Linux']
keywords = ['Supervisor tutorial', 'Supervisor vs systemd', 'Linux process management', 'supervisord configuration', 'supervisorctl commands']
+++

Supervisor ([supervisord.org](http://supervisord.org)) is a Python-based process management tool that makes it easy to start, stop, and restart long-running processes — not just Python programs, but any executable. It can manage individual processes or bring up entire groups of services at once, which is especially useful for recovering from server failures quickly.

Here is the quick summary if you are short on time:

- If you need to manage **multiple application processes** (queue workers, cron-like tasks, scrapers, utility scripts), Supervisor remains an excellent choice.
- If you want native OS-level service management with deep Linux integration, go with **systemd**.
- For Node.js-only deployments, **PM2** works well, but Supervisor is better suited for managing processes across different languages.

## Supervisor vs systemd vs PM2 — Choosing the Right Tool

| Criteria | Supervisor | systemd | PM2 |
|---|---|---|---|
| Best for | Multi-process management (polyglot) | System-level service management | Node.js application management |
| Learning curve | Moderate | Steep | Low |
| Boot startup | Supported | Native (strongest) | Supported |
| Log management | Basic | Strong | User-friendly |
| Target audience | Ops / backend / multi-script setups | Linux ops teams | Node.js developers |

> Practical advice: If your production environment already uses systemd extensively, stick with systemd. When you need to quickly unify process management across multiple languages and services, Supervisor is still a cost-effective solution.

## Installation

This guide installs Supervisor from source into `/usr/local/programs/` for consistency across all applications on the server.

Make sure Python 2.7 is available, then download the required files:

```bash
wget https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg --no-check-certificate
wget https://pypi.python.org/packages/80/37/964c0d53cbd328796b1aeb7abea4c0f7b0e8c7197ea9b0b9967b7d004def/supervisor-3.3.1.tar.gz
```

Follow these steps:

```bash
sh setuptools-0.6c11-py2.7.egg
tar -axvf supervisor-3.3.1.tar.gz
cd supervisor-3.3.1
python setup.py install
echo_supervisord_conf > /usr/local/programs/supervisoretc/supervisord.conf
supervisord -c /usr/local/programs/supervisoretc/supervisord.conf
supervisorctl
```

The generated `supervisord.conf` contains extensive comments explaining every option. The most important section to note is the `[include]` block at the bottom:

```ini
[include]
files = conf.d/*.conf
```

This tells Supervisor to load additional program configurations from the `conf.d/` directory, which is the recommended way to organize managed processes.

## Configuring a Managed Program

Using Nginx as an example, create a configuration file at `/usr/local/programs/supervisor/conf.d/nginx.conf`:

```ini
[program:nginx]
command=/usr/local/programs/nginx/nginx
user=root
autostart=true
autorestart=true
startsecs=3
stderr_logfile=/usr/local/programs/supervisor/logs/nginx_stderr_err.log
stdout_logfile=/usr/local/programs/supervisor/logs/nginx_stdout.log
```

Save the file, then start Supervisor:

```bash
supervisord -c /etc/supervisord.conf
```

## Using supervisorctl

You can enter the interactive shell by running `supervisorctl`:

```
> status              # View program status
> stop usercenter     # Stop the usercenter program
> start usercenter    # Start the usercenter program
> restart usercenter  # Restart the usercenter program
> reread              # Re-read changed config files (does not start new programs)
> update              # Restart programs whose config has changed
```

All of these commands also work directly from the command line without entering the interactive shell:

```bash
supervisorctl status
supervisorctl stop usercenter
supervisorctl start usercenter
supervisorctl restart usercenter
supervisorctl reread
supervisorctl update
```

## Starting Supervisor on Boot

### Legacy method: rc.local (Ubuntu)

On older Ubuntu systems, you can add Supervisor to `/etc/rc.local`:

```bash
#!/bin/sh -e
/bin/bash -c "/usr/local/bin/supervisord -c /usr/local/programs/supervisor/supervisord.conf"
exit 0
```

Then make it executable: `chmod +x /etc/rc.local`

> Note: On modern Ubuntu/Debian systems, `rc.local` is deprecated. Use the systemd method below instead.

### Recommended: systemd unit file

Create `/etc/systemd/system/supervisord.service`:

```ini
[Unit]
Description=Supervisor daemon
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/bin/supervisord -c /usr/local/programs/supervisor/supervisord.conf
ExecStop=/usr/local/bin/supervisorctl shutdown
ExecReload=/usr/local/bin/supervisorctl reload
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable supervisord
sudo systemctl start supervisord
sudo systemctl status supervisord
```

## Common Troubleshooting Scenarios

### 1) `unix:///tmp/supervisor.sock no such file`

**Cause:** The `supervisord` daemon is not running, or the socket path in your config does not match.

**Fix:** Start `supervisord` with the correct config file, and verify that the `serverurl` in the `[supervisorctl]` section matches the `file` path in the `[unix_http_server]` section.

### 2) Program stuck in `BACKOFF` or `FATAL` state

**Cause:** The `command` is incorrect, a dependency is missing, or the process exits immediately after starting.

**Fix:** Check `stdout_logfile` and `stderr_logfile` for error messages. Try running the command manually to confirm it works.

### 3) `autorestart` not working

**Cause:** The process exit code does not match the `exitcodes` setting, or `startsecs` is too short (the process exits before Supervisor considers it "running").

**Fix:** Set `autorestart=unexpected` and adjust `startsecs` and `startretries` as needed.

### 4) `permission denied`

**Cause:** The user running the process lacks execute permissions or write access to required directories.

**Fix:** Verify the `user=` setting, ensure log directories are writable, and confirm the executable has proper permissions.

## Related Reading

- [Linux/macOS Command Cheat Sheet](/posts/linux/2020-03-19-linux-mac-commands/)
- [curl Command Guide (Linux/macOS)](/posts/linux/2020-06-29-curl/)
- [Traceroute Command Explained](/posts/linux/2020-06-28-traceroute/)
- [Docker Compose Complete Guide](/posts/docker/2026-01-19-docker-compose-complete-guide/)
- [docker-compose.yml Explained](/posts/docker/2026-01-24-docker-compose-yml-explained/)
