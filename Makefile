.PHONY: install dev test lint format build clean publish help

help:
	@echo "Available commands:"
	@echo "  make install    - Install package in development mode"
	@echo "  make dev        - Install with dev dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code"
	@echo "  make build      - Build package"
	@echo "  make clean      - Remove build artifacts"
	@echo "  make publish    - Publish to PyPI"

install:
	uv sync

dev:
	uv sync --extra dev

test:
	uv run pytest -v

lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

build: clean
	uv build

clean:
	rm -rf dist build *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

publish: build
	uv publish
