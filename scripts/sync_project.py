#!/usr/bin/env python3
"""
Project Synchronization Engine

Minimal viable implementation: reads .sync-state.json, uses the correct
version strategy to bump the project version.

Full features (static quality checks, auto-todo, memory update) are planned
for a future iteration.
"""
import os
import sys
import json
import argparse
from typing import List, Dict, Tuple, Optional
from utils import resolve_repo_root
from version_engine import get_strategy


def _load_sync_state(repo_root: str) -> dict:
    """Load .sync-state.json from the repository root."""
    state_file = os.path.join(repo_root, ".sync-state.json")
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "v0.1.0", "version_strategy": "semver"}


def _save_sync_state(repo_root: str, state: dict) -> None:
    """Save .sync-state.json to the repository root."""
    from datetime import datetime
    state["last_updated"] = datetime.now().isoformat()
    state_file = os.path.join(repo_root, ".sync-state.json")
    with open(state_file, "w", encoding="utf-8", newline="\n") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def sync_project(bump_type: str = "patch"):
    """Synchronize project: bump version using the configured strategy."""
    root = resolve_repo_root()
    print(f"[SYNC] Synchronizing project at {root}...")

    # Load state
    state = _load_sync_state(root)
    current_version = state.get("version", "v0.1.0")
    strategy_name = state.get("version_strategy", "semver")

    # Get the correct strategy engine
    strategy = get_strategy(root)
    print(f"[SYNC] Strategy: {strategy_name} | Current: {current_version}")

    # Bump version
    version_num = current_version.lstrip("v")
    new_version_num = strategy.bump(version_num, bump_type)
    new_version = f"v{new_version_num}"

    # Update state
    state["version"] = new_version
    _save_sync_state(root, state)

    print(f"[SYNC] Version bumped: {current_version} -> {new_version}")
    print("[SYNC] Synchronization completed successfully.")
    return new_version


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize project state.")
    parser.add_argument(
        "--bump", choices=["patch", "minor", "major"],
        default="patch", help="Version bump type (default: patch)"
    )
    args = parser.parse_args()
    sync_project(args.bump)
