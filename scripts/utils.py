"""
Core Utility Helpers for AiProjectTemplate Scripts
"""
import os
from typing import Optional, List, Dict, Tuple

def resolve_repo_root(start_dir: Optional[str] = None) -> str:
    """
    Resolve the repository root directory by walking upwards until finding .git or .sync-state.json
    """
    current = start_dir or os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, ".git")) or os.path.exists(os.path.join(current, ".sync-state.json")):
            return current
        current = os.path.dirname(current)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
