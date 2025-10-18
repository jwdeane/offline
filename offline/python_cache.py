"""Python version and package caching via uv."""

import subprocess
from pathlib import Path
from typing import Dict

from .config import PythonConfig


class PythonCache:
    """Manage Python version and package caching via uv."""

    def __init__(self, config: PythonConfig):
        self.config = config

    def _check_uv(self) -> bool:
        """Check if uv is installed."""
        try:
            subprocess.run(
                ["uv", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def cache(self) -> Dict[str, any]:
        """Cache Python versions and packages."""
        if not self._check_uv():
            return {
                "success": False,
                "cached": 0,
                "message": "uv not found. Install from: https://github.com/astral-sh/uv",
            }

        cached = 0
        errors = []

        # Install Python versions
        for version in self.config.versions:
            try:
                result = subprocess.run(
                    ["uv", "python", "install", version],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                if result.returncode == 0:
                    cached += 1
                else:
                    errors.append(f"Python {version}: {result.stderr}")
            except Exception as e:
                errors.append(f"Python {version}: {str(e)}")

        # Cache packages
        for package in self.config.packages:
            try:
                # Use uv pip compile to cache package metadata
                result = subprocess.run(
                    ["uv", "pip", "compile", "-", "--quiet"],
                    input=package,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                if result.returncode == 0:
                    cached += 1
                else:
                    errors.append(f"{package}: {result.stderr}")
            except Exception as e:
                errors.append(f"{package}: {str(e)}")

        # Process requirements files
        for req_file in self.config.requirements_files:
            req_path = Path(req_file)
            if not req_path.exists():
                errors.append(f"{req_file}: file not found")
                continue

            try:
                result = subprocess.run(
                    ["uv", "pip", "compile", str(req_path), "--quiet"],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode == 0:
                    cached += 1
                else:
                    errors.append(f"{req_file}: {result.stderr}")
            except Exception as e:
                errors.append(f"{req_file}: {str(e)}")

        if errors and cached == 0:
            return {
                "success": False,
                "cached": 0,
                "message": f"All failed: {', '.join(errors[:2])}",
            }

        return {"success": True, "cached": cached, "message": ""}

    def status(self) -> Dict[str, int]:
        """Get status of cached Python versions and packages."""
        cached = 0
        total = (
            len(self.config.versions)
            + len(self.config.packages)
            + len(self.config.requirements_files)
        )

        if not self._check_uv():
            return {"cached": 0, "total": total}

        # Check installed Python versions
        try:
            result = subprocess.run(
                ["uv", "python", "list"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                installed_versions = result.stdout
                for version in self.config.versions:
                    if version in installed_versions:
                        cached += 1
        except Exception:
            pass

        # For packages, we assume they're cached if uv cache exists
        # This is a simplification; exact status would require more complex checking
        try:
            result = subprocess.run(
                ["uv", "cache", "dir"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                # If cache dir exists, count packages as potentially cached
                cached += len(self.config.packages) + len(self.config.requirements_files)
        except Exception:
            pass

        return {"cached": cached, "total": total}
