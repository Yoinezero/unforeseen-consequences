.PHONY: help build up down restart logs shell db-shell migrate migrate-auto clean reset dev prod

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Docker operations
build: ## Build the application container
	cd docker && docker-compose build --no-cache

up: ## Start all services in detached mode
	cd docker && docker-compose up -d

down: ## Stop and remove all containers
	cd docker && docker-compose down

restart: ## Restart all services
	@$(MAKE) down
	@$(MAKE) up

logs: ## Show logs for all services
	cd docker && docker-compose logs -f

logs-app: ## Show logs for the app service only
	cd docker && docker-compose logs -f app

logs-db: ## Show logs for the database service only
	cd docker && docker-compose logs -f db

# Development operations
dev: ## Start development environment
	@echo "Starting development environment..."
	@$(MAKE) up
	@echo "Services started!"
	@echo "  - API: http://localhost:8000"
	@echo "  - Database Admin: http://localhost:8080"
	@echo "  - PostgreSQL: localhost:5432"
	@echo ""
	@echo "Run 'make logs' to view logs or 'make shell' to access app container"

# Container access
shell: ## Access the application container shell
	cd docker && docker-compose exec app bash

db-shell: ## Access the database container shell
	cd docker && docker-compose exec db psql -U okolo_user -d okolo_ai_db

# Database operations
migrate: ## Run database migrations
	cd docker && docker-compose exec -w /app/src app python -m alembic upgrade head

migrate-auto: ## Generate automatic migration based on model changes
	@read -p "Migration message: " message; \
	cd docker && docker-compose exec -w /app/src app python -m alembic revision --autogenerate -m "$$message"

migrate-create: ## Create a new empty migration
	@read -p "Migration message: " message; \
	cd docker && docker-compose exec -w /app/src app python -m alembic revision -m "$$message"

migrate-history: ## Show migration history
	cd docker && docker-compose exec -w /app/src app python -m alembic history

migrate-current: ## Show current migration version
	cd docker && docker-compose exec -w /app/src app python -m alembic current

# Maintenance operations
clean: ## Remove all containers, volumes, and images
	cd docker && docker-compose down -v --rmi all --remove-orphans
	docker system prune -f

reset: ## Reset the entire environment (clean + build + up)
	@$(MAKE) clean
	@$(MAKE) build
	@$(MAKE) up

# Production operations
prod: ## Start production environment
	cd docker && docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d

# Health checks
status: ## Show status of all services
	cd docker && docker-compose ps

health: ## Check health of all services
	@echo "Checking service health..."
	@cd docker && docker-compose ps --filter "status=running"
	@echo ""
	@echo "API Health:"
	@curl -s http://localhost:8000/v1/health/ || echo "API not responding"
	@echo ""
	@echo "Database connection:"
	@cd docker && docker-compose exec db pg_isready -U okolo_user -d okolo_ai_db || echo "Database not ready"

# Testing
test: ## Run tests inside the container
	cd docker && docker-compose exec app uv run pytest

test-build: ## Build and test the application
	@$(MAKE) build
	@$(MAKE) up
	@sleep 10
	@$(MAKE) test
