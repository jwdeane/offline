"""Terraform provider caching functionality."""

import json
import subprocess
from pathlib import Path
from typing import Dict

from .config import TerraformConfig


class TerraformCache:
    """Manage Terraform provider caching."""

    def __init__(self, config: TerraformConfig):
        self.config = config

    def _check_terraform(self) -> bool:
        """Check if Terraform is installed."""
        try:
            subprocess.run(
                ["terraform", "version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def cache(self) -> Dict[str, any]:
        """Cache Terraform providers."""
        if not self._check_terraform():
            return {
                "success": False,
                "cached": 0,
                "message": "Terraform not found. Install from: https://www.terraform.io/downloads",
            }

        # Create a temporary Terraform configuration
        cache_dir = Path.home() / ".offline" / "terraform"
        cache_dir.mkdir(parents=True, exist_ok=True)

        tf_file = cache_dir / "main.tf"
        
        # Generate Terraform configuration with required providers
        tf_config = 'terraform {\n  required_providers {\n'
        for provider in self.config.providers:
            provider_name = provider.source.split('/')[-1]
            tf_config += f'    {provider_name} = {{\n'
            tf_config += f'      source  = "{provider.source}"\n'
            tf_config += f'      version = "{provider.version}"\n'
            tf_config += '    }\n'
        tf_config += '  }\n}\n'

        tf_file.write_text(tf_config)

        cached = 0
        errors = []

        try:
            # Run terraform init to download providers
            result = subprocess.run(
                ["terraform", "init"],
                cwd=cache_dir,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode == 0:
                cached = len(self.config.providers)
            else:
                errors.append(result.stderr)
        except subprocess.TimeoutExpired:
            errors.append("Terraform init timeout")
        except Exception as e:
            errors.append(str(e))

        if errors:
            return {
                "success": False,
                "cached": cached,
                "message": f"Terraform init failed: {errors[0][:100]}",
            }

        return {"success": True, "cached": cached, "message": ""}

    def status(self) -> Dict[str, int]:
        """Get status of cached Terraform providers."""
        total = len(self.config.providers)
        cached = 0

        if not self._check_terraform():
            return {"cached": 0, "total": total}

        # Check if providers are cached
        cache_dir = Path.home() / ".offline" / "terraform" / ".terraform" / "providers"
        if cache_dir.exists():
            # Count cached providers by checking directory structure
            for provider in self.config.providers:
                provider_parts = provider.source.split('/')
                provider_path = cache_dir / provider_parts[0] / provider_parts[1] / provider_parts[2]
                if provider_path.exists():
                    cached += 1

        return {"cached": cached, "total": total}
