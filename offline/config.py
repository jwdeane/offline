"""Configuration management for offline tool."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class DockerConfig:
    """Docker cache configuration."""
    images: List[str]


@dataclass
class PythonConfig:
    """Python cache configuration."""
    versions: List[str]
    packages: List[str]
    requirements_files: List[str]


@dataclass
class TerraformProvider:
    """Terraform provider configuration."""
    source: str
    version: str


@dataclass
class TerraformConfig:
    """Terraform cache configuration."""
    providers: List[TerraformProvider]


@dataclass
class Config:
    """Main configuration."""
    docker: Optional[DockerConfig] = None
    python: Optional[PythonConfig] = None
    terraform: Optional[TerraformConfig] = None

    @classmethod
    def load(cls, path: Path) -> "Config":
        """Load configuration from YAML file."""
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        docker_config = None
        if "docker" in data and data["docker"]:
            docker_config = DockerConfig(
                images=data["docker"].get("images", [])
            )

        python_config = None
        if "python" in data and data["python"]:
            python_config = PythonConfig(
                versions=data["python"].get("versions", []),
                packages=data["python"].get("packages", []),
                requirements_files=data["python"].get("requirements_files", []),
            )

        terraform_config = None
        if "terraform" in data and data["terraform"]:
            providers = []
            for provider_data in data["terraform"].get("providers", []):
                providers.append(
                    TerraformProvider(
                        source=provider_data["source"],
                        version=provider_data["version"],
                    )
                )
            terraform_config = TerraformConfig(providers=providers)

        return cls(
            docker=docker_config,
            python=python_config,
            terraform=terraform_config,
        )
