# ⚡ TermAI

## 📖 Project Overview

**TermAI** is an AI-powered command-line assistant that converts natural-language requests into terminal commands.

Instead of remembering shell syntax, users can describe what they want in plain English, and TermAI generates an appropriate command for their operating system and shell.

The project is designed around a safety-first execution pipeline where **LLM-generated commands are never executed directly**. Every generated command passes through structured validation, safety checks, and explicit user confirmation before execution.

---

## ✨ Features

| Feature | Status |
|---------|:------:|
| 🤖 Natural language → terminal command generation | ✅ |
| 🧠 Groq LLM integration | ✅ |
| 📋 Structured LLM output with Pydantic | ✅ |
| 🖥️ Automatic OS detection | ✅ |
| 💻 Shell detection (PowerShell / CMD) | ✅ |
| 🛡️ Command safety validation | ✅ |
| ⚠️ SAFE / WARNING / BLOCKED classification | ✅ |
| 👤 Explicit user confirmation before execution | ✅ |
| ⚙️ Shell-aware command execution | ✅ |
| ⏱️ Command execution timeout | ✅ |
| 📤 stdout / stderr / exit-code handling | ✅ |
| 🎨 Rich terminal output | ✅ |

---

## 🛠️ Tech Stack

### 🤖 AI

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge)

### ⚙️ CLI & Execution

![Typer](https://img.shields.io/badge/Typer-009688?style=for-the-badge)
![Rich](https://img.shields.io/badge/Rich-000000?style=for-the-badge)
![Python Subprocess](https://img.shields.io/badge/Python_Subprocess-3776AB?style=for-the-badge)

### 🛠️ Development

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## 🏗️ System Architecture

```text
                         USER
                          │
                          ▼
                   ┌─────────────┐
                   │  Typer CLI  │
                   └──────┬──────┘
                          │
                          ▼
                ┌──────────────────┐
                │ Environment      │
                │ Detection        │
                │ OS + Shell       │
                └────────┬─────────┘
                         │
                         ▼
                  ┌────────────┐
                  │  Groq LLM  │
                  └──────┬─────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Structured Output│
                │    Pydantic      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   Safety Layer   │
                └────────┬─────────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
            SAFE      WARNING    BLOCKED
              │          │          │
              └─────┬────┘          │
                    ▼               STOP
             ┌──────────────┐
             │    Human     │
             │ Confirmation │
             └──────┬───────┘
                    │
                 Approved
                    │
                    ▼
             ┌──────────────┐
             │   Executor   │
             │  subprocess  │
             └──────┬───────┘
                    │
                    ▼
              Terminal Shell
                    │
                    ▼
          stdout / stderr / exit code
```
---

## 🛡️ Safety Design

TermAI treats LLM-generated commands as untrusted output. Commands pass through multiple validation stages before execution:

```text
LLM Generated Command
        │
        ▼
Structured Validation
        │
        ▼
Safety Validation
        │
        ├── SAFE ────────┐
        │                │
        ├── WARNING ─────┤
        │                ▼
        │         User Confirmation
        │                │
        │                ▼
        │            Execution
        │
        └── BLOCKED → STOP
```

### Safety Levels

| Level | Behavior |
| :--- | :--- |
| 🟢 **SAFE** | No known dangerous pattern detected; user confirmation required |
| 🟡 **WARNING** | Potentially destructive or modifying command; explicit confirmation required |
| 🔴 **BLOCKED** | Known dangerous command; execution is stopped |

> **Note:** The safety layer is intentionally conservative. It is a V1 rule-based validator, not a complete shell security sandbox.

---

## 📂 Project Structure

```text
TermAI/
│
├── app/
│   ├── __init__.py
│   ├── cli.py              # CLI interface and application flow
│   ├── environment.py      # OS and shell detection
│   ├── models.py           # Pydantic response models
│   ├── llm.py              # Groq LLM integration
│   ├── safety.py           # Command safety validation
│   └── executor.py         # Shell command execution
│
├── .env                    # API key (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### Prerequisites

* Python 3.10+
* Git
* Groq API key
* Windows, Linux, or macOS

### 1. Clone the Repository

```bash
git clone [https://github.com/vansh-virmani/TermAI.git](https://github.com/vansh-virmani/TermAI.git)
cd TermAI
```

### 2. Create a Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

> **Warning:** Never commit your `.env` file or expose your API key publicly.

---

## ▶️ Usage

Run TermAI using:

```bash
python -m app.cli ask "list all files in the current directory"
```

TermAI detects the current environment and generates a shell-appropriate command.

### Example Output

```text
Operating System: Windows
Shell: PowerShell

You asked:
list all files in the current directory

Generated Command:
Get-ChildItem

Explanation:
Lists files and directories in the current directory.

Safety Check:
safe
No known dangerous pattern was detected.

Execute this command? [y/N]:
```

After confirmation, the command executes and outputs:

```text
Execution Result:
...
Exit Code: 0
```

---

## 🔄 Command Generation Flow

```text
Natural Language Request
          │
          ▼
   Detect OS + Shell
          │
          ▼
      Groq LLM
          │
          ▼
 Structured CommandResponse
          │
          ▼
    Safety Validation
          │
          ▼
  Human Confirmation
          │
          ▼
   Shell
```

---

## ⚠️ Limitations

* Safety validation uses rule-based checks and is not a complete security sandbox.
* LLM-generated commands may still be incorrect or unexpected.
* Complex shell syntax and edge cases may not always be detected.
* Commands require explicit user confirmation before execution.
* Execution is performed directly on the user's local machine.

---

## 🔮 Future Improvements

* More comprehensive shell-aware safety parsing
* Enhanced support for Bash and Zsh
* Persistent command history with SQLite-based logging
* Richer command risk analysis & dry-run mode
* Better handling of command pipelines and chaining
* Configurable execution timeouts
* Comprehensive unit tests for safety rules
* In-place command editing before execution
