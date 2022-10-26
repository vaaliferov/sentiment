#!/usr/bin/env bash
apt update && apt install -y python3-pip
pip3 install --upgrade pip cython wheel
pip3 install --no-cache-dir -r reqs.txt
