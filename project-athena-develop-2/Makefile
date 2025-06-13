ENV ?= dev

.PHONY: backend frontend backend-dev frontend-dev backend-prod frontend-prod dev prod install

install:
	@echo "Installing dependencies and pre-commit hooks..."
	uv sync
	pre-commit install

backend:
ifeq ($(ENV),dev)
	@echo "Running dev backend..."
	uv run fastapi dev backend/main.py
else ifeq ($(ENV),prod)
	@echo "Running prod backend..."
	uv run uvicorn backend.main:app
else
	@echo "Error: Unknown ENV='$(ENV)'. Must be 'dev' or 'prod'." && exit 1
endif

frontend:
ifeq ($(ENV),dev)
	@echo "Running dev frontend..."
	@cp .streamlit/config.dev.toml .streamlit/config.toml
	PYTHONPATH=. uv run streamlit run frontend/Home.py
else ifeq ($(ENV),prod)
	@echo "Running prod frontend..."
	@cp .streamlit/config.prod.toml .streamlit/config.toml
	PYTHONPATH=. uv run streamlit run frontend/Home.py
else
	@echo "Error: Unknown ENV='$(ENV)'. Must be 'dev' or 'prod'." && exit 1
endif

# Specific environment targets (can still be used if preferred)
backend-dev:
	$(MAKE) backend ENV=dev

backend-prod:
	$(MAKE) backend ENV=prod

frontend-dev:
	$(MAKE) frontend ENV=dev

frontend-prod:
	$(MAKE) frontend ENV=prod

dev:
	$(MAKE) backend ENV=dev & $(MAKE) frontend ENV=dev

prod:
	$(MAKE) backend ENV=prod & $(MAKE) frontend ENV=prod

lint:
	@echo "Checking for linting issues..."
	uv run ruff check .

format:
	@echo "Formatting code..."
	uv run ruff format .

fix:
	@echo "Formatting code and fixing linting issues..."
	uv run ruff format .
	uv run ruff check . --fix

