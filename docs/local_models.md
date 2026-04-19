# Running with Local Models (Ollama)

DreamTeam supports running **entirely offline** using [Ollama](https://ollama.com) —
no API keys, no cloud costs, full data privacy.

---

## How it works

The `get_llm()` factory in `config/settings.py` auto-detects Ollama models by
name prefix (`llama`, `mistral`, `phi`, `codellama`, `qwen`, `deepseek`, etc.)
and routes them to `langchain_ollama.ChatOllama`, which speaks to a locally
running Ollama daemon.

```
agency.py
  └─► get_llm("qwen2.5-coder:14b")
        └─► ChatOllama(model="qwen2.5-coder:14b")
              └─► HTTP → http://localhost:11434  (Ollama daemon)
                    └─► GPU / CPU inference
```

---

## Step 1 — Install Ollama

```bash
# macOS
brew install ollama

# macOS / Linux (official install script)
curl -fsSL https://ollama.com/install.sh | sh

# Windows — download the installer from https://ollama.com/download
```

Verify:
```bash
ollama --version   # e.g. ollama version 0.3.x
```

---

## Step 2 — Install the Python integration

```bash
source venv/bin/activate
pip install langchain-ollama
```

> `langchain-ollama` is not in `requirements.txt` by default to keep the install
> lightweight for cloud users. Add it if your team always runs locally.

---

## Step 3 — Choose a hardware tier

Three local profiles are available. Pick the one that fits your machine:

| Profile | Models | RAM | VRAM | Quality |
|---|---|---|---|---|
| `LOCAL_QUALITY` | 70B + 32B | 32 GB+ | 24 GB+ | ⭐⭐⭐⭐⭐ |
| `LOCAL_BALANCED` ← default `LOCAL` | 14B + 8B | 16 GB | 12 GB | ⭐⭐⭐⭐ |
| `LOCAL_FAST` | 7B + 3.8B | 8 GB | 6 GB | ⭐⭐⭐ |

**Rule of thumb:** Each billion parameters needs ~0.6 GB VRAM (4-bit quantised).
A 14B model needs ~9 GB VRAM.

---

## Step 4 — Pull the required models

Pull **every model** used by your chosen profile before running.

### `LOCAL_FAST` (8 GB RAM — MacBook Air / entry gaming PC)

```bash
ollama pull mistral:7b          # manager + architect + reviewer
ollama pull qwen2.5-coder:7b    # developer  ← best 7B code model
ollama pull phi3:mini           # tester + devops  (3.8B, very fast)
```

### `LOCAL_BALANCED` (16 GB RAM — MacBook Pro M2/M3 / mid-range PC)

```bash
ollama pull llama3.1:8b         # manager + reviewer
ollama pull mistral:7b          # architect
ollama pull qwen2.5-coder:14b   # developer  ← best 14B code model
ollama pull phi3:medium         # tester + devops
```

### `LOCAL_QUALITY` (32 GB RAM — Mac Studio / high-end workstation)

```bash
ollama pull llama3.1:70b        # manager + architect + reviewer
ollama pull qwen2.5-coder:32b   # developer  ← near-GPT-4 code quality
ollama pull mistral:7b          # tester + devops (fast fallback)
```

Check download progress:
```bash
ollama list   # shows all downloaded models and sizes
```

---

## Step 5 — Start the Ollama daemon

```bash
# Start in the background (stays running across terminal sessions)
ollama serve &

# Or run in a dedicated terminal window
ollama serve
```

Verify it's running:
```bash
curl http://localhost:11434/api/tags   # should return JSON listing your models
```

On macOS, Ollama also installs a menu-bar app that keeps the daemon alive automatically.

---

## Step 6 — Configure `agency.py`

```python
# agency.py — Section 1

# Option A: use a pre-built local profile
from config.profiles import LOCAL          # alias for LOCAL_BALANCED
# from config.profiles import LOCAL_FAST   # 8 GB RAM
# from config.profiles import LOCAL_QUALITY  # 32 GB+ RAM
PROFILE = LOCAL

# Option B: custom local profile
from config.profiles import AgencyProfile
PROFILE = AgencyProfile(
    name="my_local",
    description="Custom local setup with DeepSeek Coder.",
    manager="llama3.1:8b",
    architect="mistral:7b",
    developer="deepseek-coder:6.7b",   # or "qwen2.5-coder:7b"
    reviewer="llama3.1:8b",
    default="phi3:mini",
)
```

---

## Step 7 — Run

```bash
source venv/bin/activate
python agency.py
```

No API keys required. No internet connection required (after model download).

---

## Model comparison for each role

### Manager (orchestrates the crew)
Needs strong instruction-following and reasoning.

| Model | Size | Quality | RAM |
|---|---|---|---|
| `llama3.1:70b` | 40 GB | ⭐⭐⭐⭐⭐ | 48 GB |
| `llama3.1:8b` | 4.7 GB | ⭐⭐⭐⭐ | 8 GB |
| `mistral:7b` | 4.1 GB | ⭐⭐⭐ | 8 GB |

### Architect (reads codebase, plans implementation)
Needs large context window and structured output.

| Model | Size | Quality | RAM |
|---|---|---|---|
| `llama3.1:70b` | 40 GB | ⭐⭐⭐⭐⭐ | 48 GB |
| `mistral:7b` | 4.1 GB | ⭐⭐⭐⭐ | 8 GB |
| `phi3:medium` | 7.9 GB | ⭐⭐⭐ | 10 GB |

### Developer (writes code — most important role)
Use a code-specialised model here for best results.

| Model | Size | Quality | RAM |
|---|---|---|---|
| `qwen2.5-coder:32b` | 19 GB | ⭐⭐⭐⭐⭐ | 22 GB |
| `qwen2.5-coder:14b` | 9 GB | ⭐⭐⭐⭐ | 12 GB |
| `qwen2.5-coder:7b` | 4.7 GB | ⭐⭐⭐⭐ | 8 GB |
| `deepseek-coder:6.7b` | 3.8 GB | ⭐⭐⭐ | 6 GB |
| `codellama:13b` | 7.4 GB | ⭐⭐⭐ | 10 GB |

> **Recommendation:** Always use a `qwen2.5-coder` model for the developer role.
> It consistently outperforms `codellama` and `llama3.1` on coding benchmarks at every size.

### Reviewer (critical code analysis)
Needs reasoning and attention to instruction.

| Model | Size | Quality | RAM |
|---|---|---|---|
| `llama3.1:70b` | 40 GB | ⭐⭐⭐⭐⭐ | 48 GB |
| `llama3.1:8b` | 4.7 GB | ⭐⭐⭐⭐ | 8 GB |
| `mistral:7b` | 4.1 GB | ⭐⭐⭐ | 8 GB |

### Tester / DevOps (default role — fast turn-around)

| Model | Size | Quality | RAM |
|---|---|---|---|
| `phi3:medium` | 7.9 GB | ⭐⭐⭐⭐ | 10 GB |
| `phi3:mini` | 2.3 GB | ⭐⭐⭐ | 4 GB |
| `mistral:7b` | 4.1 GB | ⭐⭐⭐ | 8 GB |

---

## Performance tips

### Use GPU acceleration

Ollama uses the GPU automatically if available. To verify:

```bash
ollama run mistral:7b "Say hello"
# Look for: GPU layers: 32  (or similar)
```

**Apple Silicon (M1/M2/M3/M4):** Ollama uses the Metal GPU backend — all models run fully on the Neural Engine + GPU, even on MacBook Air.

**NVIDIA:** Ensure CUDA drivers are installed: `nvidia-smi`.

**AMD:** ROCm support is available for select GPUs.

### Increase Ollama context window

By default Ollama caps context at 2048 tokens. For the Architect agent,
which reads large codebases, increase it:

```bash
# Create a custom Modelfile
cat > Modelfile << 'EOF'
FROM llama3.1:8b
PARAMETER num_ctx 8192
EOF

ollama create llama3.1-8k -f Modelfile
```

Then use `"llama3.1-8k"` as the architect model in your profile.

### Run multiple models simultaneously

If you have enough RAM, Ollama can keep multiple models loaded at once:

```bash
# macOS / Linux
export OLLAMA_MAX_LOADED_MODELS=3
ollama serve
```

### CPU-only (no GPU)

Ollama works on CPU only — it will just be slower.
Set `num_thread` to match your CPU core count:

```bash
export OLLAMA_NUM_PARALLEL=1
OLLAMA_NUM_PARALLEL=1 ollama serve
```

---

## Disable MCP servers in local mode

MCP servers require Node.js and internet (GitHub/Brave). To skip them,
comment out the `_safe_attach` calls in `mcp_servers/adapters.py`:

```python
def run_with_mcp_tools(callback):
    print("\n🔌 MCP disabled in local mode\n")
    tools_by_role = {k: [] for k in ("architect", "developer", "reviewer", "tester", "devops")}
    return callback(tools_by_role)
```

Or simply don't set `GITHUB_TOKEN` / `BRAVE_API_KEY` — the servers will be
skipped automatically with a ⚠️ warning.

---

## Troubleshooting

### `Connection refused` / `Could not connect to Ollama`

```bash
# Ollama is not running — start it
ollama serve

# Verify the API is listening
curl http://localhost:11434/api/tags
```

### `model not found`

```bash
# Pull the missing model
ollama pull qwen2.5-coder:14b

# List downloaded models
ollama list
```

### Out of memory / model crashes

- Try a smaller model tier (`LOCAL_FAST`)
- Reduce context in the Modelfile
- Close other memory-hungry applications
- Increase macOS swap: System Settings → General → Storage

### Slow inference

- Ensure GPU acceleration is active: `ollama run <model> "test"` and check for `gpu layers`
- Use a smaller quantised variant: `qwen2.5-coder:7b-instruct-q4_K_M`
- On CPU, expect 3–8 tokens/second for 7B models

### `langchain_ollama` import error

```bash
pip install langchain-ollama
```

### Context window exceeded

```bash
# Create a custom model with larger context
cat > Modelfile << 'EOF'
FROM qwen2.5-coder:14b
PARAMETER num_ctx 16384
EOF
ollama create qwen2.5-coder-16k -f Modelfile
```

Then update your profile: `developer="qwen2.5-coder-16k"`.
