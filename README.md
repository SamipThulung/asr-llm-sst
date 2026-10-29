# asr-llm-sst
A pipeline to phone calls -> LLM -> Respose


# Appendix
export LLM_BASE_URL="https://b6hl7p7dgrpqf8-8000.proxy.runpod.net/v1"
export LLM_API_KEY="EMPTY"

export LLM_BASE_URL="https://b6hl7p7dgrpqf8-8000.proxy.runpod.net/v1"
export LLM_API_KEY="EMPTY"
curl "$LLM_BASE_URL/models"   -H "Authorization: Bearer $LLM_API_KEY"
pwd
cd asr-llm-sst/
python conect_to_llm.py 
pip install fastapi uvicorn
uvicorn relay:app --host 127.0.0.1 --port 8003
curl "$LLM_BASE_URL/models"   -H "Authorization: Bearer $LLM_API_KEY"
uvicorn relay:app --host 127.0.0.1 --port 8003

curl "$LLM_BASE_URL/models" \
  -H "Authorization: Bearer $LLM_API_KEY"

```cmd
git remote set-url origin git@github.com:SamipThulung/asr-llm-sst.git
git config --global user.email "samipthulung3@gmail.com"
git config --global user.name "SamipThulung"
ssh-keygen -t ed25519 -C "samipthulung3@gmail.com"
cat ~/.ssh/id_ed25519.pub

mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts

ssh-keygen -lf ~/.ssh/known_hosts
ssh -T git@github.com

```