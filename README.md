# ELI5 Anything 🧠

A local AI tool that explains any concept at four reading levels — from a 5-year-old to a domain expert — using Ollama. Runs entirely on your machine. No API keys. No internet required.

## Demo

```
📝 Enter concept: RBAC
============================================================
  Concept: RBAC
============================================================
🧒 ELI5 (Explain Like I'm 5)
----------------------------------------
Imagine a school where only teachers can go into the supply closet,
only the principal can enter the server room, and students can only
go to classrooms. RBAC is like that — everyone gets access to only
the places they're supposed to be in, based on their job.

🎒 High School
----------------------------------------
RBAC stands for Role-Based Access Control. Instead of giving each
person individual permissions, you assign them a "role" (like Admin,
Editor, or Viewer), and that role comes with a preset list of things
they can do. It's like how a part-time employee badge only opens
certain doors, while a manager badge opens more.

🎓 College Level
----------------------------------------
...

🔬 Expert
----------------------------------------
...
```

## Features

- **4 reading levels:** ELI5, High School, College, Expert
- **Interactive mode:** run it and keep asking questions
- **Single-shot mode:** pass a concept directly as an argument
- **Auto-detects** your installed Ollama model
- **Fully local:** no data leaves your machine
- **Zero dependencies:** pure Python standard library

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- A pulled model (e.g. `ollama pull llama3.2`)

## Installation

```bash
git clone https://github.com/debugbae/eli5-anything.git
cd eli5-anything
```

No `pip install` needed — zero third-party dependencies.

## Usage

```bash
# Interactive mode — keeps prompting until you quit
python eli5.py

# Explain a specific concept (all 4 levels)
python eli5.py "transformer architecture"

# Single level only
python eli5.py --level eli5 "machine learning"

# Multiple specific levels
python eli5.py --level hs --level college "zero trust security"

# Use a specific Ollama model
python eli5.py --model mistral "quantum computing"
```

## Why I Built This

Jargon is a barrier. Whether you're onboarding a new team member, explaining a technical concept to an executive, or just trying to understand something yourself — having a tool that can instantly translate complexity into clarity is genuinely useful.

This project also demonstrates:

- Structured prompt engineering across multiple personas
- Local LLM integration via the Ollama API
- Clean CLI design with `argparse`
- Graceful error handling for API connectivity issues

## How It Works

Each reading level has a carefully crafted system prompt that instructs the model to adjust vocabulary, depth, and framing. The tool sends the user's concept + the level prompt to Ollama's local REST API and streams back the response.

```
User input → Level prompt + Concept → Ollama API → Formatted output
```

## Levels

| Level    | Audience       | Style                                          |
|----------|----------------|------------------------------------------------|
| `eli5`   | 5-year-old     | Simple analogy, 2–3 sentences                 |
| `hs`     | High schooler  | Relatable example, some terms defined          |
| `college`| Undergrad      | Precise, includes mechanism + significance     |
| `expert` | Practitioner   | Technical, nuanced, edge cases                 |
