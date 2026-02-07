from __future__ import annotations

import argparse
from pathlib import Path
import sys

from camp_registration.registry import CampRegistry, DEFAULT_SESSIONS


def build_parser() -> argparse.ArgumentParser:
    sessions = ", ".join(DEFAULT_SESSIONS)
    parser = argparse.ArgumentParser(
        description="Camp registration program",
        epilog=f"Available sessions: {sessions}.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_parser = subparsers.add_parser("register", help="Register a camper")
    register_parser.add_argument("name")
    register_parser.add_argument("age", type=int)
    register_parser.add_argument("session")

    list_parser = subparsers.add_parser("list", help="List campers")
    list_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )

    export_parser = subparsers.add_parser("export", help="Export campers to JSON")
    export_parser.add_argument("path", type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    registry = CampRegistry()

    if args.command == "register":
        camper = registry.register_camper(args.name, args.age, args.session)
        print(
            f"Registered {camper.name} (age {camper.age}) for {camper.session} session."
        )
    elif args.command == "list":
        if not registry.campers:
            print("No campers registered yet.")
            return 0

        if args.format == "json":
            import json

            print(json.dumps([c.__dict__ for c in registry.campers], indent=2))
        else:
            for camper in registry.campers:
                print(f"{camper.name} (age {camper.age}) - {camper.session}")
    elif args.command == "export":
        registry.export_json(args.path)
        print(f"Exported {len(registry.campers)} campers to {args.path}.")
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
