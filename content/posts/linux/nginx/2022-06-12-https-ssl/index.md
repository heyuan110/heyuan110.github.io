+++
date = '2014-03-18T23:15:02+08:00'
draft = true
title = 'How to Set Up HTTPS on Nginx with a Self-Signed SSL Certificate'
description = 'Step-by-step guide to generating a self-signed SSL certificate with OpenSSL and configuring Nginx for HTTPS, covering private key generation, CSR creation, and Nginx SSL setup'
toc = true
tags = ['Nginx', 'HTTPS', 'SSL', 'OpenSSL', '证书']
categories = ['Linux']
keywords = ['nginx self-signed ssl', 'openssl generate certificate', 'nginx https setup', 'self-signed certificate nginx']
+++

![image](/images/https-ssl/https.webp)

## Install OpenSSL

There are many third-party SSL certificate providers — some paid, some free. For development and testing purposes, you can create a self-signed certificate using OpenSSL.

Check if OpenSSL is already installed:

```bash
openssl version -a
```

If it is not installed, run:

```bash
sudo apt-get install openssl
sudo apt-get install openssl-devel
```

## Generate the Private Key and Certificate

### Step 1: Generate a Private Key

Run the following command to create a 1024-bit RSA private key with DES3 encryption:

```bash
openssl genrsa -des3 -out app.key 1024
```

You will be prompted to set a passphrase. Remember it — you will need it in the next steps.

[![QQ20140318-1](/images/https-ssl/QQ20140318-1.webp)](/images/https-ssl/QQ20140318-1.webp)

### Step 2: Create a Certificate Signing Request (CSR)

```bash
openssl req -new -key app.key -out app.csr
```

This will ask you to fill in several fields (country, state, organization, etc.). You can use the same passphrase when prompted.

[![QQ20140318-2](/images/https-ssl/QQ20140318-2.webp)](/images/https-ssl/QQ20140318-2.webp)

### Step 3: Generate the Server Private Key

Strip the passphrase from the key so Nginx can use it without interactive input:

```bash
openssl rsa -in app.key -out app_server.key
```

[![QQ20140318-3](/images/https-ssl/QQ20140318-3.webp)](/images/https-ssl/QQ20140318-3.webp)

### Step 4: Sign the Certificate

```bash
openssl req -new -x509 -days 3650 -key app_server.key -out app_server.crt
```

The prompts are similar to Step 2. **Make sure the Common Name field matches your actual domain name** — this is the most common mistake.

After completing these steps, you will have four files. The two you need for Nginx are `app_server.crt` (the certificate) and `app_server.key` (the private key).

## Configure Nginx

Copy the certificate and key files to your Nginx configuration directory:

```bash
cp app_server.crt app_server.key /etc/nginx/conf.d/
```

Open your Nginx config file and set the listen port to 443 with SSL enabled:

```nginx
ssl on;
ssl_certificate /etc/nginx/conf.d/app_server.crt;
ssl_certificate_key /etc/nginx/conf.d/app_server.key;
```

**Important:** Use absolute paths for the certificate and key files.

[![QQ20140318-4](/images/https-ssl/QQ20140318-4.webp)](/images/https-ssl/QQ20140318-4.webp)

Restart Nginx to apply the changes:

```bash
sudo service nginx restart
```

> **Note:** Self-signed certificates are suitable for development and testing only. Browsers will show a security warning because the certificate is not issued by a trusted Certificate Authority. For production use, consider Let's Encrypt or a commercial CA.