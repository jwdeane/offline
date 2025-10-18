"""Docker image caching functionality."""

import subprocess
from typing import Dict, List

from .config import DockerConfig


class DockerCache:
    """Manage Docker image caching."""

    def __init__(self, config: DockerConfig):
        self.config = config

    def cache(self) -> Dict[str, any]:
        """Pull and cache Docker images."""
        cached = 0
        errors = []

        for image in self.config.images:
            try:
                result = subprocess.run(
                    ["docker", "pull", image],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                if result.returncode == 0:
                    cached += 1
                else:
                    errors.append(f"{image}: {result.stderr}")
            except subprocess.TimeoutExpired:
                errors.append(f"{image}: timeout")
            except FileNotFoundError:
                return {
                    "success": False,
                    "cached": 0,
                    "message": "Docker not found. Please install Docker.",
                }
            except Exception as e:
                errors.append(f"{image}: {str(e)}")

        if errors:
            return {
                "success": False,
                "cached": cached,
                "message": f"Some images failed: {', '.join(errors[:3])}",
            }

        return {"success": True, "cached": cached, "message": ""}

    def status(self) -> Dict[str, int]:
        """Get status of cached images."""
        cached = 0
        total = len(self.config.images)

        try:
            result = subprocess.run(
                ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                local_images = set(result.stdout.strip().split("\n"))
                for image in self.config.images:
                    if image in local_images:
                        cached += 1
        except Exception:
            pass

        return {"cached": cached, "total": total}
