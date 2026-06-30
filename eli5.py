#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.request
import urllib.error

OLLAMA_API = "http://localhost:11434"

LEVEL_CONFIG = {
    "eli5": {
        "label": "🧒 ELI5 (Explain Like I'm 5)",
        "prompt": (
            "You are explaining to a 5-year-old. Use only simple words, "
            "a short relatable analogy, and keep it to 2-3 sentences. "
            "No jargon whatsoever."
        ),
    },
    "hs": {
        "label": "🎒 High School",
        "prompt": (
            "You are explaining to a high school student. Use a relatable "
            "real-world example, define any technical terms you introduce, "
            "and keep it to a short paragraph."
        ),
    },
    "college": {
        "label": "🎓 College Level",
        "prompt": (
            "You are explaining to an undergraduate student. Be precise, "
            "include the core mechanism and why it matters, and use "
            "appropriate terminology with brief definitions."
        ),
    },
    "expert": {
        "label": "🔬 Expert",
        "prompt": (
            "You are explaining to a domain expert. Be technical and nuanced. "
            "Cover edge cases, trade-offs, and real-world implementation "
            "considerations. Assume deep familiarity with the field."
        ),
    },
}

ALL_LEVELS = ["eli5", "hs", "college", "expert"]


def get_model() -> str:
    """Return the first available Ollama model."""
    try:
        with urllib.request.urlopen(f"{OLLAMA_API}/api/tags", timeout=5) as resp:
            data = json.loads(resp.read())
            models = [m["name"] for m in data.get("models", [])]
            if not models:
                print("No Ollama models found. Run: ollama pull llama3.2", file=sys.stderr)
                sys.exit(1)
            return models[0]
    except urllib.error.URLError:
        print(
            "Cannot reach Ollama. Is it running? Try: ollama serve",
            file=sys.stderr,
        )
        sys.exit(1)


def explain(concept: str, level: str, model: str) -> None:
    config = LEVEL_CONFIG[level]
    print(f"\n{config['label']}")
    print("-" * 40)

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": config["prompt"]},
            {"role": "user", "content": f"Explain: {concept}"},
        ],
        "stream": True,
    }).encode()

    req = urllib.request.Request(
        f"{OLLAMA_API}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for line in resp:
                chunk = json.loads(line.decode())
                token = chunk.get("message", {}).get("content", "")
                print(token, end="", flush=True)
                if chunk.get("done"):
                    break
        print()
    except urllib.error.URLError as e:
        print(f"\nRequest failed: {e}", file=sys.stderr)
        sys.exit(1)


def run_interactive(model: str) -> None:
    print(f"ELI5 Anything 🧠  (model: {model})")
    print('Type a concept and press Enter. Type "quit" to exit.\n')
    while True:
        try:
            concept = input("📝 Enter concept: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if not concept:
            continue
        if concept.lower() in {"quit", "exit", "q"}:
            print("Bye!")
            break
        print_concept_header(concept)
        for level in ALL_LEVELS:
            explain(concept, level, model)


def print_concept_header(concept: str) -> None:
    print("\n" + "=" * 60)
    print(f"  Concept: {concept}")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Explain any concept at multiple reading levels using Ollama."
    )
    parser.add_argument("concept", nargs="?", help="Concept to explain")
    parser.add_argument(
        "--level",
        action="append",
        choices=list(LEVEL_CONFIG.keys()),
        dest="levels",
        metavar="LEVEL",
        help="Reading level(s): eli5, hs, college, expert (repeatable)",
    )
    parser.add_argument("--model", help="Ollama model to use (auto-detected if omitted)")
    args = parser.parse_args()

    model = args.model or get_model()
    levels = args.levels or ALL_LEVELS

    if args.concept:
        print_concept_header(args.concept)
        for level in levels:
            explain(args.concept, level, model)
    else:
        run_interactive(model)


if __name__ == "__main__":
    main()
