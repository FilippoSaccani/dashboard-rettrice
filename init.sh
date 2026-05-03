curl -fsSL https://ollama.com/install.sh | sh
ollama serve
sudo systemctl enable ollama
sudo systemctl start ollama
ollama pull gemma3

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt