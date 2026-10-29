# asr-llm-sst
A pipeline to phone calls -> LLM -> Respose


# Appendix
export LLM_BASE_URL="https://b6hl7p7dgrpqf8-8000.proxy.runpod.net/v1"
export LLM_API_KEY="EMPTY"

curl "$LLM_BASE_URL/models" \
  -H "Authorization: Bearer $LLM_API_KEY"