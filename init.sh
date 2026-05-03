sudo systemctl enable ollama
sudo systemctl start ollama

sleep 3

ollama pull gemma3

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
