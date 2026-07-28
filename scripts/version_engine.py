#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version_engine.py - Dual Versioning Strategy Engine for AI Project Template.
Supports SemVer 2.0 and CalVer version strategies, regex validation, bumping logic,
and commit message formatting (Header 強制規範: Conventional Commits / CalVer 前綴，Body 不限制/允許使用中文說明).
"""

import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Tuple, Dict, Any, Optional

class VersionStrategy(ABC):
    """Abstract Base Class for Version Strategies."""
    
    @property
    @abstractmethod
    def strategy_name(self) -> str:
        pass

    @abstractmethod
    def validate_version(self, version_str: str) -> bool:
        """Validate if the string matches the version format."""
        pass

    @abstractmethod
    def bump_version(self, current_version: str, bump_type: str = "patch") -> str:
        """Bump the current version based on the bump type (major/minor/patch)."""
        pass

    @abstractmethod
    def validate_commit_header(self, header_str: str) -> Tuple[bool, str]:
        """Validate commit message header."""
        pass

    @abstractmethod
    def format_commit_header(self, version_str: str, summary_str: str, commit_type: str = "feat") -> str:
        """Format a valid commit message header."""
        pass


class SemVerStrategy(VersionStrategy):
    """
    SemVer 2.0 Strategy (vMAJOR.MINOR.PATCH[-PRERELEASE])
    Used for code, software, libraries, and technical research projects.
    Header format: <type>(<scope>): <summary> (Conventional Commits)
    """
    
    # SemVer 2.0 regex (optional leading 'v')
    SEMVER_REGEX = re.compile(
        r"^v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
        r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
        r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )
    
    # Conventional Commits Header regex: type(scope)!: summary OR type(scope): summary OR type: summary
    CONVENTIONAL_HEADER_REGEX = re.compile(
        r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
        r"(?:\((?P<scope>[\w\-\.]+)\))?"
        r"!?:\s+(?P<summary>.+)$"
    )

    @property
    def strategy_name(self) -> str:
        return "semver"

    def validate_version(self, version_str: str) -> bool:
        return bool(self.SEMVER_REGEX.match(version_str))

    def bump_version(self, current_version: str, bump_type: str = "patch") -> str:
        match = self.SEMVER_REGEX.match(current_version)
        if not match:
            # Fallback if invalid
            return "v1.0.0"
        
        major = int(match.group("major"))
        minor = int(match.group("minor"))
        patch = int(match.group("patch"))

        bump_type = bump_type.lower()
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        else: # patch (default)
            patch += 1

        return f"v{major}.{minor}.{patch}"

    def validate_commit_header(self, header_str: str) -> Tuple[bool, str]:
        # Conventional Commit Header validation
        # Rule: Header must strictly follow Conventional Commit format, English type/summary recommended
        match = self.CONVENTIONAL_HEADER_REGEX.match(header_str.strip())
        if not match:
            return False, (
                "Header does not follow Conventional Commits format!\n"
                "Expected format: <type>(<scope>): <summary>  (e.g., 'feat(core): add feature')\n"
                "Valid types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
            )
        return True, "Valid Conventional Commit Header"

    def format_commit_header(self, version_str: str, summary_str: str, commit_type: str = "feat") -> str:
        clean_summary = summary_str.strip()
        if not clean_summary:
            clean_summary = f"release {version_str}"
        
        # Ensure type is valid
        if commit_type not in ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]:
            commit_type = "feat"
            
        return f"{commit_type}: {clean_summary}"


class CalVerStrategy(VersionStrategy):
    """
    CalVer Strategy (vYYYY.MM.DD or vX.Y.YYYYMMDD.Z)
    Used for notes, daily logs, research collection, and documentation projects.
    Header format: vX.Y.YYYYMMDD.Z <summary> or vYYYY.MM.DD <summary>
    """
    
    # CalVer regex matching either vX.Y.YYYYMMDD.Z or vYYYY.MM.DD[.Z]
    CALVER_REGEX_8DIGIT = re.compile(r"^v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<date>\d{8})\.(?P<seq>\d+)$")
    CALVER_REGEX_DATE = re.compile(r"^v(?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2})(?:\.(?P<seq>\d+))?$")

    @property
    def strategy_name(self) -> str:
        return "calver"

    def validate_version(self, version_str: str) -> bool:
        return bool(self.CALVER_REGEX_8DIGIT.match(version_str) or self.CALVER_REGEX_DATE.match(version_str))

    def bump_version(self, current_version: str, bump_type: str = "patch") -> str:
        today_str = datetime.now().strftime("%Y%m%d")
        
        match_8 = self.CALVER_REGEX_8DIGIT.match(current_version)
        if match_8:
            major = match_8.group("major")
            minor = match_8.group("minor")
            old_date = match_8.group("date")
            seq = int(match_8.group("seq"))
            
            if old_date == today_str:
                seq += 1
            else:
                seq = 1
            return f"v{major}.{minor}.{today_str}.{seq}"

        # Default fallback to 8-digit CalVer v1.0.YYYYMMDD.1
        return f"v1.0.{today_str}.1"

    def validate_commit_header(self, header_str: str) -> Tuple[bool, str]:
        # Header must start with a valid version tag
        parts = header_str.strip().split(" ", 1)
        version_part = parts[0]
        if not self.validate_version(version_part):
            return False, (
                f"CalVer Commit Header must start with a valid version (e.g., 'v1.0.{datetime.now().strftime('%Y%m%d')}.1 Summary')\n"
                f"Got version prefix: '{version_part}'"
            )
        if len(parts) < 2 or not parts[1].strip():
            return False, "CalVer Commit Header must include a summary after the version tag."
        return True, "Valid CalVer Commit Header"

    def format_commit_header(self, version_str: str, summary_str: str, commit_type: str = "feat") -> str:
        clean_summary = summary_str.strip()
        return f"{version_str} {clean_summary}"


def get_version_strategy(strategy_name: str) -> VersionStrategy:
    """Factory function to get the appropriate VersionStrategy instance."""
    name = (strategy_name or "").lower().strip()
    if name == "calver":
        return CalVerStrategy()
    # Default to SemVer Strategy
    return SemVerStrategy()


def validate_commit_message(message: str, strategy: VersionStrategy) -> Tuple[bool, str]:
    """
    Validate full commit message.
    Header must pass strategy validation.
    Body is allowed to contain Chinese (CJK) and detailed multi-line descriptions.
    """
    lines = [line.rstrip() for line in message.strip().splitlines()]
    if not lines or not lines[0]:
        return False, "Commit message cannot be empty."
    
    header = lines[0]
    valid_header, msg = strategy.validate_commit_header(header)
    if not valid_header:
        return False, msg

    # Note: Body is explicitly permitted to contain Chinese characters and markdown descriptions.
    return True, "Commit message valid."
