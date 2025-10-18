# Makefile for offline development tool

.PHONY: install dev test lint clean help

help:
	@echo "Available commands:"
	@echo "  make install   - Install the offline tool"
	@echo "  make dev       - Install in development mode with dev dependencies"
	@echo "  make test      - Run tests (if available)"
	@echo "  make lint      - Run linters"
	@echo "  make clean     - Remove build artifacts"
	@echo "  make bootstrap - Run the bootstrap script"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	@echo "No tests configured yet"

lint:
	@command -v ruff >/dev/null 2>&1 && ruff check offline/ || echo "ruff not installed, skipping"
	@command -v black >/dev/null 2>&1 && black --check offline/ || echo "black not installed, skipping"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

bootstrap:
	./bootstrap.sh
