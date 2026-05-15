"""
ELI5 Anything — explain any concept at multiple reading levels using Ollama.

Usage:
    python eli5.py                        # interactive mode
    python eli5.py "quantum entanglement" # single concept mode
    python eli5.py --level hs "RBAC"      # specific level only

Levels: eli5 | hs | college | expert
"""

import sys
import argparse
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

LEVELS = {
    "eli5": {
        "label": "🧒 ELI5 (Explain Like I'm 5)",
        "prompt": (
            "Explain the following concept as if you're talking to a 5-year-old child. "
            "Use very simple words, a short fun analogy, and keep it to 2-3 sentences. "
            "No jargon at all."
        ),
    },
    "hs": {
        "label": "🎒 High School",
        "prompt": (
            "Explain the following concept to a high school student. "
            "You can use some technical terms but define them briefly. "
            "Keep it to 3-4 sentences with a relatable example."
        ),
    },
    "college": {
        "label": "🎓 College Level",
        "prompt": (
            "Explain the following concept to a college student with some background knowledge. "
            "Be precise, use appropriate terminology, and include how it works and why it matters. "
            "Keep it to a short paragraph."
        ),
    },
    "expert": {
        "label": "🔬 Expert",
        "prompt": (
            "Explain the following concept to a domain expert. "
            "Use precise technical language, cover edge cases or nuances, "
            "and mention relevant considerations a practitioner would care about. "
            "Keep it concise but thorough."
        ),
    },
}


def query_ollama(model: str, prompt: str) -> str:
    """Send a prompt to Ollama and return the response text."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to Ollama. Make sure it's running: ollama serve")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("\n❌ Ollama timed out. Try a smaller model or shorter input.")
        sys.exit(1)


def explain(concept: str, model: str, levels: list[str]) -> None:
    """Explain a concept at one or more levels."""
    print(f"\n{'='*60}")
    print(f"  Concept: {concept}")
    print(f"{'='*60}\n")

    for level_key in levels:
        level = LEVELS[level_key]
        print(f"{level['label']}")
        print("-" * 40)

        full_prompt = f"{level['prompt']}\n\nConcept: {concept}"
        result = query_ollama(model, full_prompt)
        print(result)
        print()


def get_model() -> str:
    """Auto-detect the first available Ollama model."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json().get("models", [])
        if models:
            return models[0]["name"]
    except Exception:
        pass
    return "llama3.2"  # fallback default


def main():
    parser = argparse.ArgumentParser(
        description="ELI5 Anything — explain any concept at multiple reading levels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python eli5.py "quantum entanglement"
  python eli5.py --level eli5 "machine learning"
  python eli5.py --level hs --level college "RBAC"
  python eli5.py --model mistral "transformer architecture"
        """,
    )
    parser.add_argument(
        "concept",
        nargs="?",
        help="The concept or term to explain (omit for interactive mode)",
    )
    parser.add_argument(
        "--level",
        action="append",
        choices=list(LEVELS.keys()),
        dest="levels",
        help="Reading level(s) to use (default: all four levels)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Ollama model to use (default: auto-detected)",
    )

    args = parser.parse_args()

    model = args.model or get_model()
    levels = args.levels or list(LEVELS.keys())

    print(f"\n🤖 ELI5 Anything  |  Model: {model}")

    if args.concept:
        explain(args.concept, model, levels)
    else:
        # Interactive mode
        print("Type a concept to explain, or 'quit' to exit.\n")
        while True:
            try:
                concept = input("📝 Enter concept: ").strip()
                if concept.lower() in ("quit", "exit", "q"):
                    print("Bye!")
                    break
                if not concept:
                    continue
                explain(concept, model, levels)
            except KeyboardInterrupt:
                print("\nBye!")
                break


if __name__ == "__main__":
    main()
