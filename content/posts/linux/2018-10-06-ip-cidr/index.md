+++
title = 'IP Addresses and CIDR Explained: A Complete Networking Guide'
date = '2018-10-06'
draft = false
description = 'Learn IPv4 address structure, classful addressing (A/B/C/D/E), subnet masks, and CIDR notation. Includes a subnet cheat sheet and practical Linux commands for network engineers and developers.'
tags = ['IP', 'CIDR', 'Networking', 'Subnet Mask', 'Linux']
categories = ['Linux']
toc = true
keywords = ['IP address', 'CIDR notation', 'subnet mask', 'IPv4', 'subnetting', 'network fundamentals']
+++

Every device on the internet needs an **IP address** to communicate. Whether you are configuring cloud infrastructure, debugging connectivity issues, or setting up container networks, a solid grasp of IP addressing and CIDR is essential. This guide walks through IPv4 address structure, the legacy class system, subnet masks, and modern CIDR notation from the ground up.

<!--more-->

## Why IP Addressing Matters

| Scenario | What You Need to Know |
|----------|----------------------|
| Server setup | Static IPs, firewall rules |
| Troubleshooting | Connectivity analysis, fault isolation |
| Cloud services | VPC design, security group configuration |
| Container orchestration | Kubernetes networking, Docker network modes |

> Understanding IP fundamentals is a prerequisite for every other networking topic.

## IPv4 Address Basics

### Address Structure

An IPv4 address is a **32-bit binary number**. For readability, it is written as four decimal numbers separated by dots — a format called **dotted decimal notation**.

![Diagram showing the IPv4 address structure and the relationship between binary and decimal representations](ip-classes.svg)

```
Binary:  11000000.10101000.00000001.00000001
Decimal: 192.168.1.1
```

Each decimal number is called an **octet** (8 bits). Its range is 0 to 255 because the maximum value of 8 binary digits is 2^8 - 1 = 255.

### Network ID vs. Host ID

Every IP address consists of two logical parts:

| Part | Purpose | Used For |
|------|---------|----------|
| **Network ID** | Identifies the network the device belongs to | Routing decisions |
| **Host ID** | Identifies a specific device within that network | Local addressing |

This split is what makes routing scalable: **routers only need to store network-level entries**, not an entry for every single host on the internet.

### Reserved Addresses

Certain IP addresses serve special purposes and cannot be assigned to regular hosts:

| Type | Description | Example |
|------|-------------|---------|
| Network address | Host bits all set to 0 | 192.168.1.0 |
| Broadcast address | Host bits all set to 1 | 192.168.1.255 |
| Loopback address | Used for local testing | 127.0.0.1 |
| Private addresses | Internal use only, non-routable | 10.x.x.x, 192.168.x.x |

## Classful Addressing (Legacy)

In the early days of the internet, IP addresses were divided into five **classes** — A through E. Although CIDR replaced this system in 1993, understanding classful addressing helps explain why modern notation exists.

### Class A

- **Network ID**: First 8 bits (1st octet)
- **Host ID**: Remaining 24 bits (octets 2-4)
- **Leading bit**: `0`

```
Format: 0NNNNNNN.HHHHHHHH.HHHHHHHH.HHHHHHHH
        └─Net ID─┘└──────── Host ID ────────┘
```

| Property | Value |
|----------|-------|
| Range | 1.0.0.0 – 126.255.255.255 |
| Number of networks | 126 (0 and 127 are reserved) |
| Hosts per network | 2^24 - 2 = 16,777,214 |
| Default subnet mask | 255.0.0.0 (/8) |

> **Note:** The entire 127.x.x.x block is reserved for loopback (e.g., 127.0.0.1).

### Class B

- **Network ID**: First 16 bits (octets 1-2)
- **Host ID**: Remaining 16 bits (octets 3-4)
- **Leading bits**: `10`

```
Format: 10NNNNNN.NNNNNNNN.HHHHHHHH.HHHHHHHH
        └──── Net ID ────┘└── Host ID ──┘
```

| Property | Value |
|----------|-------|
| Range | 128.0.0.0 – 191.255.255.255 |
| Number of networks | 2^14 = 16,384 |
| Hosts per network | 2^16 - 2 = 65,534 |
| Default subnet mask | 255.255.0.0 (/16) |

### Class C

- **Network ID**: First 24 bits (octets 1-3)
- **Host ID**: Remaining 8 bits (4th octet)
- **Leading bits**: `110`

```
Format: 110NNNNN.NNNNNNNN.NNNNNNNN.HHHHHHHH
        └────────── Net ID ──────────┘└Host┘
```

| Property | Value |
|----------|-------|
| Range | 192.0.0.0 – 223.255.255.255 |
| Number of networks | 2^21 = 2,097,152 |
| Hosts per network | 2^8 - 2 = 254 |
| Default subnet mask | 255.255.255.0 (/24) |

### Class D (Multicast)

- **Leading bits**: `1110`
- **Range**: 224.0.0.0 – 239.255.255.255
- **Purpose**: Multicast — one-to-many communication

Class D addresses have no network/host split. They are used to send data to a group of receivers simultaneously.

### Class E (Reserved)

- **Leading bits**: `1111`
- **Range**: 240.0.0.0 – 255.255.255.255
- **Purpose**: Reserved for experimental use

> **Note:** 255.255.255.255 is the limited broadcast address, used to reach all devices on the local network.

### Class Summary

| Class | Leading Bits | 1st Octet Range | Default Mask | Use Case |
|-------|-------------|-----------------|--------------|----------|
| A | 0 | 1-126 | /8 | Large networks |
| B | 10 | 128-191 | /16 | Medium networks |
| C | 110 | 192-223 | /24 | Small networks |
| D | 1110 | 224-239 | — | Multicast |
| E | 1111 | 240-255 | — | Reserved |

## Subnet Masks

### What Is a Subnet Mask?

A **subnet mask** is a 32-bit value that tells you which bits of an IP address belong to the network and which belong to the host.

- **1-bits** mark the network portion
- **0-bits** mark the host portion

```
IP address:  192.168.1.100
             11000000.10101000.00000001.01100100

Subnet mask: 255.255.255.0
             11111111.11111111.11111111.00000000
             └────────── Network ──────────┘└Host┘

Network address: 192.168.1.0 (IP AND mask)
```

### How Subnet Masks Work

Performing a **bitwise AND** between an IP address and its subnet mask yields the network address:

```bash
# Are these two hosts on the same network?
192.168.1.100 AND 255.255.255.0 = 192.168.1.0
192.168.1.200 AND 255.255.255.0 = 192.168.1.0
# Same result — they can communicate directly.

192.168.1.100 AND 255.255.255.0 = 192.168.1.0
192.168.2.100 AND 255.255.255.0 = 192.168.2.0
# Different result — traffic must go through a router.
```

### Calculating Usable Hosts

The formula for usable host addresses in a subnet:

```
Usable hosts = 2^(host bits) - 2
```

**Why subtract 2?** Because two addresses in every subnet are reserved:
- **Network address**: all host bits set to 0 (e.g., 192.168.1.0)
- **Broadcast address**: all host bits set to 1 (e.g., 192.168.1.255)

## CIDR (Classless Inter-Domain Routing)

### Why CIDR Was Needed

Classful addressing led to massive **address waste**:

| Scenario | Need | Classful Allocation | Wasted |
|----------|------|---------------------|--------|
| 300 hosts | 300 IPs | Class C (254) too small, Class B (65,534) | 65,234 |
| 2,000 hosts | 2,000 IPs | Class B (65,534) | 63,534 |

In 1993, the IETF published RFC 1518 and RFC 1519, introducing **CIDR** (Classless Inter-Domain Routing) to solve this problem once and for all.

### CIDR Notation

CIDR uses **slash notation** to express the network prefix length:

```
Format:  IP_address/prefix_length
Example: 192.168.1.0/24
```

`/24` means the first 24 bits are the network ID and the remaining 8 bits are for hosts — equivalent to the subnet mask 255.255.255.0.

### CIDR Calculation Example

Suppose you need a subnet that supports 2,000 hosts:

```
Required host bits: 2^11 = 2048 > 2000, so 11 host bits
Network bits:       32 - 11 = 21
CIDR notation:      xxx.xxx.xxx.xxx/21
Subnet mask:        11111111.11111111.11100000.00000000 = 255.255.224.0
Usable hosts:       2^11 - 2 = 2,046
```

### Advantages of CIDR

| Advantage | Description |
|-----------|-------------|
| Flexible allocation | Assign exactly the number of IPs you need |
| Route aggregation | Combine multiple networks into a single route (supernetting) |
| Slower exhaustion | More efficient use of the IPv4 address space |

## Subnetting in Practice

### Steps to Subnet a Network

1. Determine how many subnets you need (or how many hosts per subnet)
2. Calculate how many host bits to borrow
3. Derive the new subnet mask
4. List the address range for each subnet

### Example: Split 192.168.1.0/24 into 4 Subnets

```
Original network: 192.168.1.0/24
Subnets needed:   4
Bits borrowed:    2 (2^2 = 4)
New mask:         /26 (255.255.255.192)
```

Results:

| Subnet | Network Address | Usable Range | Broadcast | Usable Hosts |
|--------|----------------|--------------|-----------|--------------|
| 1 | 192.168.1.0/26 | .1 – .62 | .63 | 62 |
| 2 | 192.168.1.64/26 | .65 – .126 | .127 | 62 |
| 3 | 192.168.1.128/26 | .129 – .190 | .191 | 62 |
| 4 | 192.168.1.192/26 | .193 – .254 | .255 | 62 |

## Subnet Cheat Sheet

A quick reference for common CIDR prefixes:

| CIDR | Subnet Mask | Usable Hosts | Typical Use |
|------|------------|--------------|-------------|
| /30 | 255.255.255.252 | 2 | Point-to-point links |
| /29 | 255.255.255.248 | 6 | Tiny subnets |
| /28 | 255.255.255.240 | 14 | Small offices |
| /27 | 255.255.255.224 | 30 | Small departments |
| /26 | 255.255.255.192 | 62 | Medium departments |
| /25 | 255.255.255.128 | 126 | Large departments |
| /24 | 255.255.255.0 | 254 | Standard Class C equivalent |
| /23 | 255.255.254.0 | 510 | Medium networks |
| /22 | 255.255.252.0 | 1,022 | Large networks |
| /21 | 255.255.248.0 | 2,046 | Large networks |
| /20 | 255.255.240.0 | 4,094 | Data centers |
| /16 | 255.255.0.0 | 65,534 | Standard Class B equivalent |
| /8 | 255.0.0.0 | 16,777,214 | Standard Class A equivalent |

## Private IP Addresses

RFC 1918 defines three private address ranges for internal networks. These addresses are not routed on the public internet:

| Range | CIDR | Available IPs | Legacy Class |
|-------|------|---------------|-------------|
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | 16,777,216 | A |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | 1,048,576 | B |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | 65,536 | C |

Home routers and corporate LANs use these private ranges and reach the public internet through NAT (Network Address Translation).

## Useful Commands

### Viewing IP Configuration on Linux

```bash
# Show all network interfaces
ip addr show

# Show the routing table
ip route show

# Show a specific interface
ip addr show eth0
```

### Calculating Network Addresses

```bash
# Use the ipcalc utility
ipcalc 192.168.1.100/24

# Sample output:
# Network:   192.168.1.0/24
# Netmask:   255.255.255.0
# Broadcast: 192.168.1.255
# HostMin:   192.168.1.1
# HostMax:   192.168.1.254
# Hosts/Net: 254
```

### Testing Connectivity

```bash
# Ping test
ping 192.168.1.1

# Trace the route
traceroute 8.8.8.8
```

For more Linux networking commands, see [Linux/macOS Command Cheat Sheet](/posts/linux/2020-03-19-linux-mac-commands/).

## Summary

Here are the key takeaways:

1. **IPv4 addresses** are 32-bit numbers split into a network ID and a host ID
2. **Classful addressing** divided addresses into five classes (A–E) but wasted large blocks of address space
3. **Subnet masks** separate the network portion from the host portion using a bitwise AND operation
4. **CIDR** replaced classful addressing with flexible prefix-length notation, enabling right-sized allocations
5. **Subnetting** lets you carve a large network into smaller, more manageable segments

These fundamentals underpin everything from cloud VPC design and Kubernetes pod networking to firewall rules and DNS configuration.

## Further Reading

- [Linux/macOS Command Cheat Sheet](/posts/linux/2020-03-19-linux-mac-commands/) — Network diagnostic commands
- [Traceroute Explained](/posts/linux/2020-06-28-traceroute/) — Tracing network routes
- [The Complete curl Guide](/posts/linux/2020-06-29-curl/) — HTTP requests and API debugging

## References

- [Understanding IP Addresses, Subnets, and CIDR — DigitalOcean](https://www.digitalocean.com/community/tutorials/understanding-ip-addresses-subnets-and-cidr-notation-for-networking)
- [What is CIDR? — AWS](https://aws.amazon.com/what-is/cidr/)
- [Subnet Cheat Sheet — freeCodeCamp](https://www.freecodecamp.org/news/subnet-cheat-sheet-24-subnet-mask-30-26-27-29-and-other-ip-address-cidr-network-references/)
- [CIDR — Wikipedia](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
- [RFC 1918 — Private Address Space](https://tools.ietf.org/html/rfc1918)
