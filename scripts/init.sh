#!/bin/bash

sudo systemctl enable ollama
sudo systemctl start ollama

sleep 3

cd ..
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
