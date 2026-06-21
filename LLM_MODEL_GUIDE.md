# Legal AI Fine-Tuned Model Setup Guide

## Overview

Your Legal Document Analyzer comes with two response modes:

1. **Fine-Tuned Legal AI Model** (slower, ~10-30 seconds) - Most accurate, context-aware legal responses
2. **RAG Retrieval Mode** (faster, ~1-2 seconds) - Quick document context extraction

## Current Status

The system now shows which model is answering your questions at the bottom of each response:
- ✓ **Fine-tuned legal AI model** = Using the powerful fine-tuned Llama model
- ✓ **Laptop-safe RAG mode** = Using fast document retrieval (CPU-safe)
- ℹ **Document retrieval** = Using retrieval while model is loading

## Why You Might See Laptop Mode by Default

By default, on systems without a GPU, **Laptop-Safe Mode** is enabled to prevent memory issues. This uses RAG retrieval instead of loading the fine-tuned model.

## Enabling the Fine-Tuned Model

### Option 1: Full Power Mode (For GPU or High-End Computers)

Edit `.env` file or create one in the backend directory:

```env
# Enable fine-tuned model on any system
LEGAL_AI_CPU_SAFE_MODE=false
LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU=true
```

Then restart the backend:
```bash
# Stop the current backend (Ctrl+C)
# Then restart
uvicorn backend.app:app --reload
```

### Option 2: GPU Acceleration (Recommended for Speed)

If you have an NVIDIA GPU with CUDA installed:

```env
LEGAL_AI_CPU_SAFE_MODE=false
LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU=false
```

The system will automatically use GPU (much faster!).

### Option 3: Programmatic Mode Switch

Use the Chat Status page to switch modes:
- **"Full Power"** = Use fine-tuned model on CPU
- **"Laptop Mode"** = Use fast RAG retrieval

## Prerequisites for Fine-Tuned Model

1. **Model Files Present**: Ensure `backend/models/legal_lora_model/` contains:
   - `adapter_config.json`
   - `adapter_model.safetensors`
   - `tokenizer.json` or `tokenizer_config.json`

2. **Dependencies Installed**:
   ```bash
   pip install -r backend/requirements.txt
   ```
   This should include:
   - `torch`
   - `transformers`
   - `peft`
   - `accelerate`

3. **Memory Available**: 
   - CPU: ~4-8 GB RAM
   - GPU: ~4 GB VRAM

## Troubleshooting

### "Model setup needed" Message
**Problem**: Model files are not found
**Solution**: Ensure `legal_lora_model` folder exists with adapter files

### "Model attached but not loaded yet"
**Problem**: Files exist but dependencies are missing
**Solution**: 
```bash
pip install peft accelerate
```

### Responses Still Using RAG Mode
**Problem**: CPU-Safe mode is enabled
**Solution**: 
```bash
# In backend/.env
LEGAL_AI_CPU_SAFE_MODE=false
LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU=true
```

### Out of Memory (OOM) Errors
**Problem**: System doesn't have enough memory for fine-tuned model
**Solution**: Keep `LEGAL_AI_CPU_SAFE_MODE=true` or upgrade system memory

## Configuration Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `LEGAL_AI_MODEL_PATH` | `models/legal_lora_model` | Path to fine-tuned model |
| `LEGAL_AI_BASE_MODEL` | Auto-detected | Base model name |
| `LEGAL_AI_CPU_SAFE_MODE` | `true` | Disable on CPU to avoid OOM |
| `LEGAL_AI_ENABLE_FINE_TUNED_ON_CPU` | `false` | Allow fine-tuned model on CPU |
| `LEGAL_AI_MAX_NEW_TOKENS` | `256` | Max response length |
| `LEGAL_AI_TEMPERATURE` | `0.2` | Response creativity (0=deterministic, 1=creative) |

## Performance Comparison

| Metric | Fine-Tuned Model | RAG Retrieval |
|--------|-----------------|---------------|
| **Speed** | 10-30 seconds | 1-2 seconds |
| **Accuracy** | High | Medium |
| **Context Use** | Full understanding | Simple matching |
| **Legal Reasoning** | Advanced | Basic |
| **CPU Usage** | High | Low |

## Frontend Response Feedback

After each response, you'll see:
- ✓ Model source (Fine-tuned or RAG)
- Number of document chunks used
- Response details

## Testing the Model

Use these sample questions on your legal document:

1. **"What are the key termination conditions?"**
2. **"List all payment obligations mentioned."**
3. **"What penalties apply if payment is late?"**

Compare RAG vs Fine-Tuned responses to see the difference!

## Checking Backend Logs

Monitor the backend terminal to see which model is being used:

```
✓ Using fine-tuned legal model for question: What are the key...
✓ Fine-tuned model response generated successfully
```

Or:

```
⚠ Fine-tuned model unavailable. Using retrieval_fallback mode
```

## Still Having Issues?

1. **Check Status Page**: Visit Chat page to see current model status
2. **Review Backend Logs**: Look for "✓" or "⚠" indicators
3. **Verify Installation**: Run `pip list | grep -E "torch|transformers|peft"`
4. **Test Sample Document**: Upload the included `sample_lease_agreement.txt`

---

**Happy legal document analyzing!** 🚀
~