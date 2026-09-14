+++
date = '2013-06-18T17:44:50+08:00'
draft = true
title = 'macOS 显示和隐藏隐藏文件：终端命令与图形工具'
description = 'macOS 系统中显示和隐藏隐藏文件的多种方法，提供 Shell 脚本命令和图形界面小工具下载，轻松管理以点号开头的隐藏文件'
toc = true
tags = ['macOS', '终端', '隐藏文件', '技巧']
categories = ['macOS']

[[params.faqItems]]
question = "macOS 上为什么有些文件看不到？"
answer = "因为在 OS X / macOS 里，以点号 `.` 开头的文件会被系统自动隐藏，Finder 默认不显示它们。常见的 `.zshrc`、`.gitignore`、`.env` 都属于这一类，文件其实一直都在，只是默认不展示给你看。"

[[params.faqItems]]
question = "macOS 怎么用命令显示和隐藏隐藏文件？"
answer = "把文中提供的两个脚本下载下来，在终端里执行 `sh showallfiles.sh` 就能显示全部隐藏文件，想恢复默认状态执行 `sh hideallfiles.sh`。脚本已经打包成 sh.zip，文中可直接下载，执行完按提示查看 Finder 效果即可。"

[[params.faqItems]]
question = "不想每次都敲终端命令，有图形化的办法吗？"
answer = "有，文中附了一个自己写的小工具 ShowFiles，带图形界面，点一下就能切换显示或隐藏，不用记 `showallfiles.sh` 和 `hideallfiles.sh` 这两条命令。工具打包成 zip 可以直接在文中下载，适合不习惯用终端的人。"
+++
在osx里，.开头的文件会被自动隐藏的，但是如果想要显示所有隐藏文件怎么办呢？<!--more-->

**打开终端输入下面的命令**

隐藏：`sh hideallfiles.sh`

显示：`sh showallfiles.sh`

![xgt](/images/showorhidefiles/2.webp)


下载sh文件：[sh.zip](/download/showorhidefiles-sh.zip)

**每次敲命令也是比较繁琐的**

所以写了个小工具有界面哦，截图

![xgt](/images/showorhidefiles/1.webp)

下载工具：[ShowFiles](/download/showorhidefiles-app.zip)
