# offline

> What do you need when the lights go dark?

A bootstrap tool for caching development dependencies locally to enable offline development. When the internet goes down, continue hacking on new projects with pre-cached Docker images, development tools (via mise), Python packages (via uv), and Terraform providers.

## 🚀 Quick Start

```bash
# Clone and bootstrap
git clone https://github.com/jwdeane/offline.git
cd offline
./bootstrap.sh

# Or manually install
pip install -e .

# Create configuration
offline init

# Customize offline.yaml to your needs
# Then sync dependencies
offline sync

# Check status
offline status
```

## 📋 Features

- **Docker Image Caching**: Pre-pull commonly used Docker images
- **Development Tools (via mise)**: Unified management for Python, Node, Terraform, Go, and [hundreds more](https://mise.jdx.dev/registry.html)
- **Python Environment Caching**: Install Python versions and packages via uv (alternative to mise)
- **Terraform Provider Caching**: Download Terraform providers locally
- **Periodic Updates**: Run `offline sync` periodically to keep caches fresh
- **Configuration-Driven**: Simple YAML configuration for all dependencies
- **Cross-Platform**: Works on macOS, Linux (and Windows with WSL)

## 🛠️ Requirements

### Required
- Python 3.9 or later
- pip

### Optional (for specific features)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) - for Docker image caching
- [mise](https://mise.jdx.dev) - for unified development tool management (recommended, auto-installed by bootstrap)
- [uv](https://github.com/astral-sh/uv) - for Python version/package caching (auto-installed by bootstrap)
- [Terraform](https://www.terraform.io/downloads) - for Terraform provider caching (can be managed by mise)

## 📖 Usage

### Initialize Configuration

```bash
offline init
```

Creates a sample `offline.yaml` configuration file with common defaults.

### Sync Dependencies

```bash
# Sync all configured dependencies
offline sync

# Sync only specific types
offline sync --no-docker           # Skip Docker images
offline sync --no-mise             # Skip mise tools
offline sync --no-python           # Skip Python packages
offline sync --no-terraform        # Skip Terraform providers

# Use custom config file
offline sync -c my-config.yaml
```

### Check Cache Status

```bash
offline status
```

Shows what's currently cached locally.

## ⚙️ Configuration

The `offline.yaml` file controls what gets cached. Here's an example:

```yaml
# Docker images to cache locally
docker:
  images:
    - "python:3.11"
    - "python:3.12"
    - "node:20"
    - "postgres:16"
    - "redis:7"

# Development tools via mise (recommended)
# mise manages Python, Node, Terraform, Go, and hundreds more
mise:
  tools:
    - "python@3.12"
    - "node@20"
    - "terraform@1.9"
    - "go@1.22"

# Python versions and packages to cache via uv (alternative to mise for Python)
python:
  # Python versions to install
  versions:
    - "3.11"
    - "3.12"
  
  # Packages to cache
  packages:
    - "pytest"
    - "black"
    - "requests"
    - "fastapi"
  
  # Optional: requirements files to cache
  requirements_files:
    - "./requirements.txt"

# Terraform providers to cache (alternative to managing terraform via mise)
terraform:
  providers:
    - source: "hashicorp/aws"
      version: "~> 5.0"
    - source: "hashicorp/google"
      version: "~> 5.0"
```

### Why mise?

[mise](https://mise.jdx.dev) is a unified development environment manager that:
- **Manages hundreds of tools**: Python, Node, Terraform, Go, Ruby, Java, and more
- **Offline-first design**: Tools are cached locally and work without internet
- **Fast and efficient**: Written in Rust, faster than alternatives like asdf
- **No shims**: Direct binaries, better performance
- **Per-project versions**: Automatic tool switching with `.mise.toml` files

**Recommended approach**: Use `mise` for tool management (Python, Node, Terraform, etc.) and `uv` for Python package dependencies. This gives you the best of both worlds:
- mise handles runtime versions
- uv handles Python packages
- Docker handles container images

## 🔄 Periodic Updates

Add to your crontab or run manually:

```bash
# Run weekly on Sunday at 2 AM
0 2 * * 0 cd /path/to/offline && /usr/local/bin/offline sync

# Or create a simple update script
cat > update-cache.sh << 'EOF'
#!/bin/bash
cd /path/to/offline
offline sync
EOF
chmod +x update-cache.sh
```

## 🐳 Development Container

This repository includes a devcontainer configuration for testing. While the target OS is macOS, the devcontainer provides a consistent Linux environment for development and testing.

```bash
# Open in VS Code with Dev Containers extension
code .
# Then: "Reopen in Container"
```

The devcontainer includes:
- Python 3.12
- Docker-in-Docker
- Terraform
- All necessary extensions

## 🎯 Use Cases

### New Project Setup
When starting a new project offline, you'll have immediate access to:
- Common Docker images (databases, web servers, language runtimes)
- Popular Python packages and multiple Python versions
- Terraform providers for major cloud platforms

### Airplane Coding
Download everything you need before a flight, then hack away at 35,000 feet.

### Remote/Low-Bandwidth Work
Pre-cache dependencies when you have good internet, use them when you don't.

### CI/CD Optimization
Use cached dependencies to speed up builds and reduce external dependencies.

## 📝 Tips

1. **Start Small**: Begin with a minimal config and add dependencies as needed
2. **Regular Updates**: Run `offline sync` weekly to keep caches fresh
3. **Share Configs**: Share `offline.yaml` with your team for consistent environments
4. **Disk Space**: Docker images and packages can be large; monitor disk usage
5. **Version Pinning**: Use specific versions in config for reproducibility

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional package managers (npm, maven, etc.)
- Better caching strategies
- Progress indicators and logging
- Cache cleanup/pruning commands
- Network detection and auto-sync

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- [Docker](https://www.docker.com/) - Container platform
- [Terraform](https://www.terraform.io/) - Infrastructure as code
