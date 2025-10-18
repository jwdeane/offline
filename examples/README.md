# Configuration Examples

This directory contains example configuration files for common development scenarios. Copy and customize them for your needs.

## Available Examples

### `mise-unified.yaml` (⭐ Recommended)
Unified tool management using mise for all development tools.
- Python, Node, Terraform, Go, Rust, Ruby via mise
- Docker images for services
- Simplified configuration

**Use case**: Modern development with unified tool management

### `python-minimal.yaml`
Minimal Python development setup with essential tools.
- Python 3.11 & 3.12
- Basic testing and linting tools
- No Docker dependencies

**Use case**: Quick Python scripting and small projects

### `web-fullstack.yaml`
Full-stack web development environment.
- Python & Node.js runtimes
- PostgreSQL, Redis, MongoDB
- Web frameworks (Django, FastAPI, Flask)
- Nginx

**Use case**: Building web applications with backend and database

### `cloud-infra.yaml`
Cloud infrastructure and DevOps tools.
- Terraform with major cloud providers
- AWS, Azure, Google Cloud CLIs
- Infrastructure as Code tools

**Use case**: Cloud infrastructure management and deployment

### `data-science.yaml`
Data science and machine learning environment.
- Scientific Python stack (NumPy, Pandas, etc.)
- ML frameworks (TensorFlow, PyTorch)
- Jupyter notebooks
- Visualization tools

**Use case**: Data analysis and machine learning projects

## Using Examples

```bash
# Copy an example
cp examples/web-fullstack.yaml offline.yaml

# Customize it for your needs
vim offline.yaml

# Sync dependencies
offline sync
```

## Creating Your Own

Start with an example that's closest to your needs, then:

1. Add/remove Docker images based on your requirements
2. Adjust Python versions to match your projects
3. Add specific packages you frequently use
4. Configure Terraform providers if doing infrastructure work

See the main README for full configuration documentation.
