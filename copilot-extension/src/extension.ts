import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

// ── Constants ─────────────────────────────────────────────────────────────────

const PARTICIPANT_ID = 'dreamteam.agent';

const ALL_PROFILES = [
  'POWER',
  'BALANCED',
  'FAST',
  'BUDGET',
  'COPILOT_PRO',
  'COPILOT_STANDARD',
  'LOCAL',
  'LOCAL_QUALITY',
  'LOCAL_BALANCED',
  'LOCAL_FAST',
] as const;

// ── Activation ────────────────────────────────────────────────────────────────

export function activate(context: vscode.ExtensionContext): void {
  const participant = vscode.chat.createChatParticipant(
    PARTICIPANT_ID,
    handleDreamTeamChat,
  );
  participant.iconPath = new vscode.ThemeIcon('robot');
  context.subscriptions.push(participant);
}

export function deactivate(): void {}

// ── Chat handler ──────────────────────────────────────────────────────────────

async function handleDreamTeamChat(
  request: vscode.ChatRequest,
  _context: vscode.ChatContext,
  stream: vscode.ChatResponseStream,
  token: vscode.CancellationToken,
): Promise<vscode.ChatResult> {
  const root = findAgencyRoot();

  if (!root) {
    stream.markdown(
      '❌ **DreamTeam project not found.**\n\n' +
        'Open the folder containing `agency.py` in VS Code, then try again.',
    );
    return {};
  }

  const prompt = request.prompt.trim();

  switch (request.command) {
    case 'status':
      return handleStatus(root, stream);

    case 'profile':
      return handleProfile(root, prompt, stream);

    case 'run':
    default: {
      const task = prompt;
      if (!task) {
        stream.markdown(helpText());
        return {};
      }
      return handleRun(root, task, stream, token);
    }
  }
}

// ── /run ──────────────────────────────────────────────────────────────────────

async function handleRun(
  root: string,
  task: string,
  stream: vscode.ChatResponseStream,
  token: vscode.CancellationToken,
): Promise<vscode.ChatResult> {
  const python = getPython(root);

  stream.markdown(`🚀 **Starting DreamTeam crew…**\n\n> **Task:** ${task}\n\n`);

  // Stream raw agency output inside a code block
  stream.markdown('```\n');

  return new Promise<vscode.ChatResult>((resolve) => {
    const proc = cp.spawn(python, ['agency.py', '--task', task], {
      cwd: root,
      env: { ...process.env },
    });

    const onCancel = token.onCancellationRequested(() => {
      proc.kill('SIGTERM');
      stream.markdown('\n[Cancelled by user]\n```\n\n⚠️ Run cancelled.');
      resolve({});
    });

    proc.stdout.on('data', (chunk: Buffer) => {
      stream.markdown(chunk.toString());
    });

    proc.stderr.on('data', (chunk: Buffer) => {
      stream.markdown(chunk.toString());
    });

    proc.on('error', (err) => {
      onCancel.dispose();
      stream.markdown('\n```\n\n');
      stream.markdown(
        `❌ **Failed to start agency:** ${err.message}\n\n` +
          'Make sure Python and the project dependencies are installed:\n' +
          '```bash\npython -m venv venv && source venv/bin/activate\npip install -r requirements.txt\n```',
      );
      resolve({});
    });

    proc.on('close', (code) => {
      onCancel.dispose();
      stream.markdown('\n```\n\n');

      if (code === 0) {
        // Append the review report if it was generated
        const report = readFile(root, 'review_report.md');
        if (report) {
          stream.markdown('---\n\n### 📋 Review Report\n\n' + report + '\n\n');
        }
        stream.markdown('✅ **Crew run complete.**');
      } else {
        stream.markdown(
          `❌ **Agency exited with code ${code}.**\n\n` +
            'Check your `.env` file — at least one of ' +
            '`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or `GITHUB_TOKEN` must be set.',
        );
      }

      resolve({});
    });
  });
}

// ── /profile ──────────────────────────────────────────────────────────────────

async function handleProfile(
  root: string,
  arg: string,
  stream: vscode.ChatResponseStream,
): Promise<vscode.ChatResult> {
  const agencyPath = path.join(root, 'agency.py');

  // Read current profile from agency.py
  let content: string;
  try {
    content = fs.readFileSync(agencyPath, 'utf-8');
  } catch {
    stream.markdown('❌ Could not read `agency.py`.');
    return {};
  }

  const currentMatch = content.match(/^from config\.profiles import (\w+)/m);
  const current = currentMatch?.[1] ?? 'unknown';

  // No argument → show current profile and options
  if (!arg) {
    const rows = ALL_PROFILES.map(
      (p) => `| \`${p}\` | ${p === current ? '✅ **active**' : ''} |`,
    ).join('\n');

    stream.markdown(
      `### Active Profile: \`${current}\`\n\n` +
        `| Profile | Status |\n|---|---|\n${rows}\n\n` +
        `Switch with: \`@dreamteam /profile COPILOT_PRO\``,
    );
    return {};
  }

  // Validate the requested profile
  const newProfile = arg.toUpperCase() as (typeof ALL_PROFILES)[number];
  if (!(ALL_PROFILES as readonly string[]).includes(newProfile)) {
    stream.markdown(
      `❌ Unknown profile \`${newProfile}\`.\n\nValid options: ` +
        ALL_PROFILES.map((p) => `\`${p}\``).join(', '),
    );
    return {};
  }

  // Patch agency.py
  const updated = content.replace(
    /^from config\.profiles import \w+/m,
    `from config.profiles import ${newProfile}`,
  );
  try {
    fs.writeFileSync(agencyPath, updated);
  } catch (err: unknown) {
    stream.markdown(
      `❌ Failed to update \`agency.py\`: ${(err as Error).message}`,
    );
    return {};
  }

  stream.markdown(
    `✅ Profile switched to **\`${newProfile}\`** in \`agency.py\`.\n\n` +
      profileNote(newProfile),
  );
  return {};
}

// ── /status ───────────────────────────────────────────────────────────────────

async function handleStatus(
  root: string,
  stream: vscode.ChatResponseStream,
): Promise<vscode.ChatResult> {
  stream.markdown(`### 📂 DreamTeam Status\n\n**Project root:** \`${root}\`\n\n`);

  const outputFiles = [
    { file: 'project_tasks.md', label: '📋 Task file' },
    { file: 'review_report.md', label: '🔍 Review report' },
    { file: 'test_results.md', label: '🧪 Test results' },
  ];

  for (const { file, label } of outputFiles) {
    const content = readFile(root, file);
    if (content) {
      const preview = content.length > 600
        ? content.slice(0, 600) + '\n…(truncated)'
        : content;
      stream.markdown(`**${label}** (\`${file}\`)\n\n\`\`\`markdown\n${preview}\n\`\`\`\n\n`);
    } else {
      stream.markdown(`**${label}** — \`${file}\` not found\n\n`);
    }
  }

  // Show active profile
  try {
    const agencyContent = fs.readFileSync(path.join(root, 'agency.py'), 'utf-8');
    const match = agencyContent.match(/^from config\.profiles import (\w+)/m);
    if (match) {
      stream.markdown(`**Active profile:** \`${match[1]}\``);
    }
  } catch { /* ignore */ }

  return {};
}

// ── Utilities ─────────────────────────────────────────────────────────────────

/**
 * Find the first workspace folder that contains agency.py.
 */
function findAgencyRoot(): string | undefined {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders) { return undefined; }

  for (const folder of folders) {
    if (fs.existsSync(path.join(folder.uri.fsPath, 'agency.py'))) {
      return folder.uri.fsPath;
    }
  }
  return undefined;
}

/**
 * Resolve the Python executable — prefer the project venv if present.
 */
function getPython(root: string): string {
  const isWin = process.platform === 'win32';
  const candidates = isWin
    ? [
        path.join(root, 'venv', 'Scripts', 'python.exe'),
        path.join(root, '.venv', 'Scripts', 'python.exe'),
        'python',
      ]
    : [
        path.join(root, 'venv', 'bin', 'python'),
        path.join(root, '.venv', 'bin', 'python'),
        'python3',
        'python',
      ];

  for (const p of candidates) {
    if (path.isAbsolute(p) && fs.existsSync(p)) { return p; }
    if (!path.isAbsolute(p)) { return p; } // system python — let PATH resolve
  }
  return 'python3';
}

/**
 * Safely read a file from the project root. Returns null if not found.
 */
function readFile(root: string, filename: string): string | null {
  try {
    return fs.readFileSync(path.join(root, filename), 'utf-8');
  } catch {
    return null;
  }
}

/**
 * Extra guidance shown after switching to specific profiles.
 */
function profileNote(profile: string): string {
  if (profile === 'COPILOT_PRO' || profile === 'COPILOT_STANDARD') {
    return (
      '> ⚠️ Requires `GITHUB_TOKEN` with `models:read` scope in your `.env`.\n' +
      '> Copilot Pro/Pro+ subscribers get higher rate limits.\n' +
      '> Browse available models: https://github.com/marketplace/models'
    );
  }
  if (profile.startsWith('LOCAL')) {
    return '> ℹ️ Requires [Ollama](https://ollama.com) running locally. Pull models with `ollama pull <model>`.';
  }
  return '';
}

// ── Help text ─────────────────────────────────────────────────────────────────

function helpText(): string {
  return `## 🤖 DreamTeam — Multi-Agent AI Crew

**Run a task** (just describe it):
\`\`\`
@dreamteam Build a FastAPI REST API for a todo list with PostgreSQL
\`\`\`

**Slash commands:**

| Command | Description |
|---|---|
| \`@dreamteam /run <task>\` | Explicitly run a task |
| \`@dreamteam /profile\` | Show the active model profile |
| \`@dreamteam /profile COPILOT_PRO\` | Switch to a different profile |
| \`@dreamteam /status\` | Show recent output files |

**Available profiles:**

| Profile | Models used |
|---|---|
| \`POWER\` | Claude Opus 4.5 · Gemini 2.5 Pro · GPT-4.1 |
| \`BALANCED\` | Claude Sonnet 4.5 · Gemini 2.5 Flash · GPT-4.1 |
| \`FAST\` | Claude Haiku · Gemini 2.0 Flash · GPT-4.1-mini |
| \`BUDGET\` | GPT-4.1-mini + Gemini 2.0 Flash across all roles |
| \`COPILOT_PRO\` | GitHub Models (Claude 3.7 · GPT-4o) — no extra API keys |
| \`COPILOT_STANDARD\` | GitHub Models (GPT-4o all roles) |
| \`LOCAL\` | Ollama local models — no API costs |
`;
}
