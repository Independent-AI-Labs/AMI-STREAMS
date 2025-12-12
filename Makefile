# Streams Module Makefile

UV ?= uv
PYTHON_VERSION ?= 3.12

.PHONY: setup test clean

setup:
	@echo "Syncing streams dependencies..."
	$(UV) python install $(PYTHON_VERSION)
	$(UV) sync --dev

test:
	$(UV) run pytest -q

clean:
	rm -rf .venv
