# Troubleshooting Guide

Common issues and solutions when using the offline development bootstrap tool.

## Installation Issues

### "uv: command not found"
**Solution**: Install uv:
```bash
# Official installer (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew on macOS
brew install uv

# Check installation
uv --version
```

### "offline: command not found" after installation
**Solution**: Add Python scripts directory to PATH:
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# Then reload
source ~/.bashrc  # or source ~/.zshrc
```

## Configuration Issues

### "Configuration file not found"
**Solution**: Initialize a configuration file:
```bash
offline init
```

### Invalid YAML syntax
**Solution**: Check your YAML formatting:
- Use 2 spaces for indentation (no tabs)
- Ensure colons have a space after them
- Validate with: `python3 -c "import yaml; yaml.safe_load(open('offline.yaml'))"`

## Mise Issues

### "mise not found"
**Solution**: Install mise:
```bash
# Official installer (recommended)
curl https://mise.run | sh

# Or via Homebrew on macOS
brew install mise

# Add to shell profile
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
# Or for zsh:
echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc

# Verify installation
mise --version
```

### "mise install fails"
**Solution**:
- Check internet connection
- Ensure sufficient disk space
- Try installing tool manually: `mise install python@3.12`
- Check mise doctor: `mise doctor`

### Which tool manager should I use?
**Answer**: 
- **Recommended**: Use `mise` for runtime versions (Python, Node, Terraform, etc.) and `uv` for Python packages
- **Alternative**: Use `uv` for Python and install other tools manually
- `mise` advantages: unified management, hundreds of tools, offline-first design
- You can use both or either depending on your needs

## Docker Issues

### "Docker not found"
**Solution**: Install Docker Desktop:
- macOS: https://www.docker.com/products/docker-desktop/
- Verify: `docker --version`

### "Cannot connect to Docker daemon"
**Solution**: 
- Ensure Docker Desktop is running
- Check Docker daemon status: `docker ps`
- On Linux, add user to docker group: `sudo usermod -aG docker $USER`

### Docker pull fails with "timeout"
**Solution**:
- Check internet connection
- Increase timeout if on slow connection
- Try pulling manually: `docker pull <image>`

## Python/uv Issues

### "uv not found"
**Solution**: Install uv:
```bash
# Recommended (official installer)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew on macOS
brew install uv

# Verify installation
uv --version
```

### "uv python install fails"
**Solution**:
- Check internet connection
- Ensure sufficient disk space
- Try installing manually: `uv python install 3.12`

### Python package caching fails
**Solution**:
- Verify package names are correct
- Check uv cache directory exists: `uv cache dir`
- Clear cache and retry: `uv cache clean`

## Terraform Issues

### "Terraform not found"
**Solution**: Install Terraform:
```bash
# macOS
brew install terraform

# Or download from https://www.terraform.io/downloads

# Verify
terraform version
```

### "Terraform init fails"
**Solution**:
- Check provider source and version in config
- Ensure internet connectivity
- Try initializing manually in a test directory
- Check Terraform cache: `~/.terraform.d/plugin-cache`

### Provider version conflicts
**Solution**:
- Use version constraints: `~> 5.0` instead of specific versions
- Check provider compatibility
- Update provider versions in config

## Performance Issues

### Sync takes too long
**Solution**:
- Reduce number of items in configuration
- Use `--no-docker`, `--no-python`, or `--no-terraform` to skip specific types
- Run sync during off-peak hours
- Check internet bandwidth

### Disk space issues
**Solution**:
- Check available space: `df -h`
- Clean Docker images: `docker system prune -a`
- Clean uv cache: `uv cache clean`
- Remove unused Terraform providers

## macOS-Specific Issues

### Permission denied on bootstrap.sh
**Solution**:
```bash
chmod +x bootstrap.sh
./bootstrap.sh
```

### Command line tools not found
**Solution**: Install Xcode Command Line Tools:
```bash
xcode-select --install
```

## General Tips

### Enable verbose output
Add debugging to understand what's happening:
```bash
# For Docker
docker pull <image> --progress=plain

# For Python
uv --verbose python install 3.12

# For Terraform
TF_LOG=DEBUG terraform init
```

### Check logs
Look in:
- Docker Desktop logs (via UI)
- Terminal output
- System logs: `~/Library/Logs` (macOS)

### Reset everything
If all else fails:
```bash
# Remove all cached data
docker system prune -a
uv cache clean
rm -rf ~/.offline/terraform

# Reinstall offline tool
uv pip uninstall offline
uv sync

# Start fresh
offline init --force
offline sync
```

## Getting Help

If you're still having issues:

1. Check existing issues: https://github.com/jwdeane/offline/issues
2. Create a new issue with:
   - Your OS and version
   - Output of `offline --version`
   - Full error message
   - Your configuration file (without sensitive data)
3. Include what you've already tried

## Common Workarounds

### Can't install Docker
Skip Docker caching:
```bash
offline sync --no-docker
```

### Can't install Terraform
Skip Terraform caching:
```bash
offline sync --no-terraform
```

### Want minimal setup
Use a minimal config:
```yaml
docker:
  images: []
python:
  versions: ["3.12"]
  packages: ["pytest"]
  requirements_files: []
terraform:
  providers: []
```
