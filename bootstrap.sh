#!/bin/bash
# Bootstrap script for offline development environment setup
# This script installs the offline CLI tool and creates a sample configuration

set -e

echo "🚀 Offline Development Environment Bootstrap"
echo "============================================="
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "Detected OS: ${MACHINE}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION detected"

# Install mise if not present
if ! command -v mise &> /dev/null; then
    echo ""
    echo "📦 Installing mise (development environment manager)..."
    curl https://mise.run | sh
    # Add to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    echo "✓ mise installed"
    echo ""
    echo "⚠️  Note: You may need to add mise to your shell profile."
    echo "   Run: echo 'eval \"\$(~/.local/bin/mise activate bash)\"' >> ~/.bashrc"
    echo "   Or for zsh: echo 'eval \"\$(~/.local/bin/mise activate zsh)\"' >> ~/.zshrc"
else
    echo "✓ mise detected"
fi

# Install uv if not present (required for Python package management)
if ! command -v uv &> /dev/null; then
    echo ""
    echo "📦 Installing uv (Python package manager)..."
    if [ "$MACHINE" = "Mac" ]; then
        if command -v brew &> /dev/null; then
            brew install uv
        else
            curl -LsSf https://astral.sh/uv/install.sh | sh
        fi
    else
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
    # Add to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    echo "✓ uv installed"
else
    echo "✓ uv detected"
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed. Docker image caching will be unavailable."
    echo "   Install Docker Desktop for Mac: https://www.docker.com/products/docker-desktop/"
else
    echo "✓ Docker detected"
fi

# Check Terraform
if ! command -v terraform &> /dev/null; then
    echo "⚠️  Terraform is not installed. Terraform provider caching will be unavailable."
    echo "   Install Terraform: https://www.terraform.io/downloads"
else
    echo "✓ Terraform detected"
fi

echo ""
echo "📦 Installing offline CLI tool..."

# Install the offline tool using uv
uv sync

echo "✓ offline CLI tool installed"
echo ""

# Create sample configuration if it doesn't exist
if [ ! -f "offline.yaml" ]; then
    echo "📝 Creating sample configuration..."
    offline init
else
    echo "✓ Configuration file already exists: offline.yaml"
fi

echo ""
echo "✅ Bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Review and customize offline.yaml"
echo "  2. Run 'offline sync' to cache dependencies"
echo "  3. Run 'offline status' to check cache status"
echo ""
echo "Run 'offline --help' for more information."
