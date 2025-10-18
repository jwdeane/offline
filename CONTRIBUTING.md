# Contributing to Offline

Thank you for your interest in contributing to the Offline development bootstrap tool! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/offline.git
   cd offline
   ```
3. Install in development mode:
   ```bash
   uv pip install -e .
   ```

## Development Setup

### Using DevContainer (Recommended)
The easiest way to get started is using the provided devcontainer:

1. Install VS Code and the Dev Containers extension
2. Open the repository in VS Code
3. Click "Reopen in Container" when prompted
4. The container will automatically install dependencies

### Manual Setup
If you prefer to develop locally:

```bash
# Install the tool in editable mode using uv
uv pip install -e .

# Or use mise tasks (recommended)
mise run install

# Install development dependencies with uv
uv pip install ruff black mypy
```

### Using mise Tasks
This project uses mise for task automation. View available tasks:

```bash
# List all tasks
mise tasks

# Run common tasks
mise run install    # Install the tool
mise run lint       # Run linters
mise run clean      # Clean build artifacts
mise run bootstrap  # Run bootstrap script
```

## Making Changes

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the code style guidelines below

3. Test your changes:
   ```bash
   offline init
   offline sync -c offline.yaml
   offline status -c offline.yaml
   ```

4. Commit your changes with clear commit messages:
   ```bash
   git add .
   git commit -m "Add feature: description of your feature"
   ```

5. Push to your fork and create a pull request

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Keep functions focused and modular
- Add docstrings to functions and classes
- Use meaningful variable names

Run linters before committing:
```bash
mise run lint
```

## Testing

Currently, the project doesn't have automated tests. When adding new features:

1. Manually test the CLI commands
2. Test with various configuration options
3. Test error handling (missing tools, invalid configs, etc.)
4. Document your testing steps in the PR

Future contributions for test infrastructure are welcome!

## Areas for Contribution

### High Priority
- [ ] Add automated tests (pytest)
- [ ] Add npm/yarn package caching
- [ ] Add maven/gradle artifact caching
- [ ] Cache cleanup/pruning commands
- [ ] Better progress indicators
- [ ] Logging to file

### Medium Priority
- [ ] Network detection and auto-sync
- [ ] Configuration validation
- [ ] Multiple configuration profiles
- [ ] Export/import cache between machines
- [ ] Bandwidth usage reporting

### Nice to Have
- [ ] Web UI for configuration
- [ ] Cache analytics/statistics
- [ ] Integration with CI/CD systems
- [ ] Plugin system for custom cachers
- [ ] Cache compression

## Pull Request Guidelines

1. **Keep PRs focused**: One feature or fix per PR
2. **Update documentation**: Update README.md if adding features
3. **Test thoroughly**: Include testing steps in PR description
4. **Clear descriptions**: Explain what and why, not just how
5. **Follow code style**: Run linters before submitting

## Questions or Issues?

- Open an issue for bugs or feature requests
- Tag maintainers for urgent issues
- Be patient and respectful in communications

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
