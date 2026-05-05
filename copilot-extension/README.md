# DreamTeam — Copilot Chat Extension

Invoke your **DreamTeam multi-agent AI crew** directly from GitHub Copilot Chat in VS Code.

## Requirements

- VS Code **1.90+** with the **GitHub Copilot** extension
- Python **3.12+** with DreamTeam dependencies installed (`pip install -r requirements.txt`)
- At least one LLM provider API key (see `.env.example`)

## Install

```bash
cd copilot-extension
npm install
npm run package          # produces dreamteam-copilot-0.1.0.vsix
```

Then install the `.vsix` in VS Code:

```
Extensions panel → ··· → Install from VSIX → select dreamteam-copilot-0.1.0.vsix
```

## Usage

Open the DreamTeam project folder in VS Code, then use Copilot Chat:

### Run a task
```
@dreamteam Build a FastAPI REST API for a todo list with PostgreSQL and JWT auth
```
The agent crew will run autonomously and stream output live in the chat panel.
The **review report** is shown at the end.

### Slash commands

| Command | What it does |
|---|---|
| `@dreamteam /run <task>` | Explicitly run a task |
| `@dreamteam /profile` | Show the currently active model profile |
| `@dreamteam /profile COPILOT_PRO` | Switch profile (edits `agency.py` for you) |
| `@dreamteam /status` | Preview `review_report.md`, `test_results.md`, active task |

### Available profiles

| Profile | Models | Requirements |
|---|---|---|
| `BALANCED` | Claude Sonnet 4.5 · Gemini 2.5 Flash · GPT-4.1 | `ANTHROPIC_API_KEY` + `GOOGLE_API_KEY` + `OPENAI_API_KEY` |
| `COPILOT_PRO` | GitHub Models: Claude 3.7 Sonnet · GPT-4o | `GITHUB_TOKEN` with `models:read` scope |
| `COPILOT_STANDARD` | GitHub Models: GPT-4o all roles | `GITHUB_TOKEN` with `models:read` scope |
| `LOCAL` | Ollama local models | [Ollama](https://ollama.com) running locally |

## Using with GitHub Copilot (no OpenAI/Anthropic key needed)

1. Create a GitHub Personal Access Token with the `models:read` permission scope
2. Add it to your `.env`:
   ```
   GITHUB_TOKEN=ghp_...
   ```
3. Switch profile in Copilot Chat:
   ```
   @dreamteam /profile COPILOT_PRO
   ```
4. Run a task:
   ```
   @dreamteam Add a /health endpoint and request logging middleware
   ```

## Development

```bash
npm run watch     # rebuild on file change
npm run compile-check  # typecheck without building
```

To debug, open `copilot-extension/` in VS Code and press **F5**.
