"""Mise-based development tools caching functionality."""

import subprocess
from pathlib import Path
from typing import Dict, List

from .config import MiseConfig


class MiseCache:
    """Manage development tools caching via mise."""

    def __init__(self, config: MiseConfig):
        self.config = config

    def _check_mise(self) -> bool:
        """Check if mise is installed."""
        try:
            subprocess.run(
                ["mise", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def cache(self) -> Dict[str, any]:
        """Cache development tools via mise."""
        if not self._check_mise():
            return {
                "success": False,
                "cached": 0,
                "message": "mise not found. Install from: https://mise.jdx.dev",
            }

        cached = 0
        errors = []

        # Install tools
        for tool in self.config.tools:
            try:
                # Parse tool spec (e.g., "python@3.12" or "node@20")
                result = subprocess.run(
                    ["mise", "install", tool],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                if result.returncode == 0:
                    cached += 1
                else:
                    errors.append(f"{tool}: {result.stderr.strip()}")
            except subprocess.TimeoutExpired:
                errors.append(f"{tool}: timeout")
            except Exception as e:
                errors.append(f"{tool}: {str(e)}")

        if errors and cached == 0:
            return {
                "success": False,
                "cached": 0,
                "message": f"All failed: {', '.join(errors[:2])}",
            }

        return {"success": True, "cached": cached, "message": ""}

    def status(self) -> Dict[str, int]:
        """Get status of cached tools."""
        cached = 0
        total = len(self.config.tools)

        if not self._check_mise():
            return {"cached": 0, "total": total}

        # Check installed tools
        try:
            result = subprocess.run(
                ["mise", "list"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                installed_tools = result.stdout
                for tool in self.config.tools:
                    # Extract tool name (e.g., "python" from "python@3.12")
                    tool_name = tool.split('@')[0] if '@' in tool else tool
                    if tool_name in installed_tools:
                        cached += 1
        except Exception:
            pass

        return {"cached": cached, "total": total}
