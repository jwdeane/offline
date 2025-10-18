"""Command-line interface for offline development bootstrap."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import Config
from .docker_cache import DockerCache
from .mise_cache import MiseCache
from .python_cache import PythonCache
from .terraform_cache import TerraformCache

console = Console()


@click.group()
@click.version_option()
def main():
    """Offline development environment bootstrap tool.
    
    Cache dependencies locally for offline development:
    - Docker images
    - Development tools (via mise)
    - Python versions and packages (via uv)
    - Terraform providers
    """
    pass


@main.command()
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, path_type=Path),
    default="offline.yaml",
    help="Path to configuration file",
)
@click.option(
    "--docker/--no-docker",
    default=True,
    help="Cache Docker images",
)
@click.option(
    "--python/--no-python",
    default=True,
    help="Cache Python versions and packages",
)
@click.option(
    "--terraform/--no-terraform",
    default=True,
    help="Cache Terraform providers",
)
@click.option(
    "--mise/--no-mise",
    default=True,
    help="Cache development tools via mise",
)
def sync(config, docker, python, terraform, mise):
    """Sync/update all cached dependencies."""
    try:
        cfg = Config.load(config)
    except FileNotFoundError:
        console.print(f"[red]Configuration file not found: {config}[/red]")
        console.print("[yellow]Run 'offline init' to create a sample configuration.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error loading configuration: {e}[/red]")
        sys.exit(1)

    console.print("[bold blue]Starting offline cache sync...[/bold blue]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        if docker and cfg.docker:
            task = progress.add_task("Caching Docker images...", total=None)
            docker_cache = DockerCache(cfg.docker)
            result = docker_cache.cache()
            progress.update(task, completed=True)
            if result["success"]:
                console.print(f"[green]✓ Docker: {result['cached']} images cached[/green]")
            else:
                console.print(f"[yellow]⚠ Docker: {result['message']}[/yellow]")

        if mise and cfg.mise:
            task = progress.add_task("Caching development tools (mise)...", total=None)
            mise_cache = MiseCache(cfg.mise)
            result = mise_cache.cache()
            progress.update(task, completed=True)
            if result["success"]:
                console.print(f"[green]✓ Mise: {result['cached']} tools cached[/green]")
            else:
                console.print(f"[yellow]⚠ Mise: {result['message']}[/yellow]")

        if python and cfg.python:
            task = progress.add_task("Caching Python environments...", total=None)
            python_cache = PythonCache(cfg.python)
            result = python_cache.cache()
            progress.update(task, completed=True)
            if result["success"]:
                console.print(f"[green]✓ Python: {result['cached']} versions/packages cached[/green]")
            else:
                console.print(f"[yellow]⚠ Python: {result['message']}[/yellow]")

        if terraform and cfg.terraform:
            task = progress.add_task("Caching Terraform providers...", total=None)
            terraform_cache = TerraformCache(cfg.terraform)
            result = terraform_cache.cache()
            progress.update(task, completed=True)
            if result["success"]:
                console.print(f"[green]✓ Terraform: {result['cached']} providers cached[/green]")
            else:
                console.print(f"[yellow]⚠ Terraform: {result['message']}[/yellow]")

    console.print("\n[bold green]Cache sync completed![/bold green]")


@main.command()
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default="offline.yaml",
    help="Output configuration file path",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing configuration file",
)
def init(output, force):
    """Initialize a sample configuration file."""
    if output.exists() and not force:
        console.print(f"[yellow]Configuration file already exists: {output}[/yellow]")
        console.print("[yellow]Use --force to overwrite[/yellow]")
        sys.exit(1)

    sample_config = """# Offline Development Environment Configuration

# Docker images to cache locally
docker:
  images:
    - "python:3.11"
    - "python:3.12"
    - "node:20"
    - "node:latest"
    - "postgres:16"
    - "redis:7"
    - "nginx:alpine"

# Development tools via mise (recommended for unified tool management)
# mise can manage Python, Node, Terraform, Go, and hundreds of other tools
# See: https://mise.jdx.dev
mise:
  tools:
    - "python@3.12"
    - "python@3.11"
    - "node@20"
    - "terraform@1.9"
    - "go@1.22"
    # Add more tools as needed. Format: toolname@version
    # Examples: ruby@3.3, java@21, rust@latest

# Python versions and packages to cache via uv (alternative to mise for Python)
python:
  # Python versions to install via uv
  versions:
    - "3.9"
    - "3.10"
    - "3.11"
    - "3.12"
  
  # Common packages to cache
  packages:
    - "pytest"
    - "black"
    - "ruff"
    - "mypy"
    - "requests"
    - "flask"
    - "fastapi"
    - "django"
    - "numpy"
    - "pandas"
  
  # Optional: requirements files to cache
  requirements_files: []
    # - "./requirements.txt"
    # - "./requirements-dev.txt"

# Terraform providers to cache (alternative to managing terraform via mise)
terraform:
  providers:
    - source: "hashicorp/aws"
      version: "~> 5.0"
    - source: "hashicorp/azurerm"
      version: "~> 3.0"
    - source: "hashicorp/google"
      version: "~> 5.0"
    - source: "hashicorp/kubernetes"
      version: "~> 2.0"
"""

    output.write_text(sample_config)
    console.print(f"[green]✓ Configuration file created: {output}[/green]")
    console.print("\n[blue]Edit the configuration file to customize your cache.[/blue]")
    console.print(f"[blue]Then run: offline sync -c {output}[/blue]")


@main.command()
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, path_type=Path),
    default="offline.yaml",
    help="Path to configuration file",
)
def status(config):
    """Show status of cached dependencies."""
    try:
        cfg = Config.load(config)
    except FileNotFoundError:
        console.print(f"[red]Configuration file not found: {config}[/red]")
        sys.exit(1)

    console.print("[bold blue]Offline Cache Status[/bold blue]\n")

    if cfg.docker:
        docker_cache = DockerCache(cfg.docker)
        status_info = docker_cache.status()
        console.print(f"[cyan]Docker Images:[/cyan] {status_info['cached']}/{status_info['total']} cached")

    if cfg.mise:
        mise_cache = MiseCache(cfg.mise)
        status_info = mise_cache.status()
        console.print(f"[cyan]Mise Tools:[/cyan] {status_info['cached']}/{status_info['total']} cached")

    if cfg.python:
        python_cache = PythonCache(cfg.python)
        status_info = python_cache.status()
        console.print(f"[cyan]Python Versions/Packages:[/cyan] {status_info['cached']}/{status_info['total']} cached")

    if cfg.terraform:
        terraform_cache = TerraformCache(cfg.terraform)
        status_info = terraform_cache.status()
        console.print(f"[cyan]Terraform Providers:[/cyan] {status_info['cached']}/{status_info['total']} cached")


if __name__ == "__main__":
    main()
