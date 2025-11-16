"""Command line wrapper around the ActionEngine."""

from __future__ import annotations

import argparse
import json

from .engine import ActionEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate natural language into action plans.")
    parser.add_argument("utterance", help="User request for Iris", nargs="+")
    args = parser.parse_args()

    utterance = " ".join(args.utterance)
    engine = ActionEngine()
    plan = engine.build_plan(utterance)
    print(json.dumps(plan.to_dict(), indent=2))


if __name__ == "__main__":  # pragma: no cover
    main()
