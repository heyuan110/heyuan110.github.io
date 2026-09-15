+++
title = 'Linux Ops Fundamentals Hub: CLI, Network Troubleshooting &'
description = 'A curated hub for essential Linux operations skills — command-line basics, network diagnostics, Docker containers, and AWS CLI for everyday dev and ops work.'
date = '2026-02-18T21:35:00+08:00'
lastmod = '2026-02-18T21:35:00+08:00'
draft = true
toc = true
tags = ['Linux', 'DevOps', 'Docker', 'Networking']
categories = ['Linux']
keywords = ['Linux operations', 'command line basics', 'network troubleshooting', 'Docker containers', 'AWS CLI']

[[params.faqItems]]
question = "Which Linux skills does a developer actually need for ops work?"
answer = "Four keep recurring, whether you are debugging a production server or building infrastructure: working efficiently on the command line, diagnosing network problems, running containers, and managing cloud resources. This hub maps each to a practical guide — everyday Linux and Mac commands, `curl` for HTTP and API work, `traceroute` for network paths, Docker Compose for multi-container apps, and the AWS CLI for cloud resources."

[[params.faqItems]]
question = "Where should I start if I only have time for one or two of these?"
answer = "Start with the command-line essentials, then `curl`. The everyday commands guide covers what you reach for constantly, and `curl` is the single tool that turns a terminal into an API client — making HTTP requests, testing endpoints and transferring data without leaving the shell. Those two cover the majority of day-to-day debugging before you touch containers or cloud tooling at all."

[[params.faqItems]]
question = "How do I diagnose a network connectivity problem from the terminal?"
answer = "Two articles here cover the ground. `traceroute` traces the path packets take and shows where they stop, which is how you separate a local problem from one several hops away. The IP addressing and CIDR primer covers the fundamentals underneath — subnets, masks and prefix notation — so that a routing or subnet misconfiguration is something you can read rather than guess at."

[[params.faqItems]]
question = "What is the difference between the Docker articles linked here?"
answer = "Three cover different levels. The Docker commands cheat sheet is a quick reference for the most-used CLI commands. The Docker Compose complete guide covers defining and running multi-container applications end to end. The docker-compose.yml explainer breaks down every section of a Compose file field by field, which is the one to open when a specific key is not behaving the way you expected."

[[params.faqItems]]
question = "What else is worth reading beyond the core five?"
answer = "Shell setup and fundamentals. The Shell and Zsh configuration guide gets you a productive terminal environment rather than the default one, and the shell variables article explains environment variables, scope and the patterns that trip people up in scripts and CI. Together with the AWS CLI guide, that covers most of what everyday dev and ops work actually demands."
+++

> This page is a living hub for Linux ops fundamentals — updated regularly as new content is added.

## What This Hub Covers

Whether you're a developer who needs to debug a production server or an ops engineer building infrastructure, certain Linux skills come up again and again: working efficiently on the command line, diagnosing network issues, running containers, and managing cloud resources.

This hub collects the most practical, high-impact articles on these core topics in one place for quick reference.

## Core Articles

1. [Essential Linux & Mac Commands](/posts/linux/2020-03-19-linux-mac-commands/) — The everyday commands you'll reach for most often
2. [curl Command Reference](/posts/linux/2020-06-29-curl/) — Making HTTP requests, testing APIs, and transferring data from the terminal
3. [traceroute Explained](/posts/linux/2020-06-28-traceroute/) — Tracing network paths and diagnosing connectivity issues
4. [Docker Compose Complete Guide](/posts/docker/2026-01-19-docker-compose-complete-guide/) — Defining and running multi-container applications
5. [AWS CLI Complete Guide](/posts/linux/2020-07-04-aws-cli/) — Managing AWS resources from the command line

## Further Reading

These related articles go deeper into specific areas:

- [Shell & Zsh Configuration](/posts/linux/2015-06-17-shell-zsh/) — Setting up a productive shell environment
- [Shell Variables Explained](/posts/linux/2019-05-13-linux-shell-vars/) — Understanding environment variables, scope, and common patterns
- [IP Addressing & CIDR Primer](/posts/linux/2018-10-06-ip-cidr/) — The networking fundamentals behind subnets and routing
- [Docker Commands Cheat Sheet](/posts/docker/2019-11-14-docker-commands/) — Quick reference for the most-used Docker CLI commands
- [docker-compose.yml Explained](/posts/docker/2026-01-24-docker-compose-yml-explained/) — Breaking down every section of a Compose file
