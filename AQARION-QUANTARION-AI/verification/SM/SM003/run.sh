#!/bin/bash
set -e
python3 rank.py
python3 frobenius.py
python3 mutations.py
echo "PASS SM003"
