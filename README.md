# AI Execution Intelligence

An AI execution intelligence platform built to analyze prompts, select suitable language models, execute requests, and track execution performance, costs, and output quality.

The project explores how to build a modular and observable LLM execution pipeline, with persistent execution records and measurable quality evaluations.

## Features

- **Prompt Analysis:** Classifies prompts by category, complexity, domain, and execution requirements.
- **Model Registry:** Maintains metadata about available language models.
- **Model Selection:** Selects a suitable model using configurable scoring criteria.
- **LLM Execution:** Runs prompts through Ollama.
- **Execution Tracking:** Records execution status, latency, and errors.
- **Event Tracking:** Persists events generated throughout the pipeline.
- **Cost Tracking:** Estimates execution costs using model pricing and token usage where available.
- **Quality Evaluation:** Evaluates generated responses for correctness, relevance, and completeness.
- **PostgreSQL Persistence:** Stores execution records and evaluation results.
- **Execution Analytics:** Provides access to persisted execution data.
- **Automated Testing:** Tests core services, model selection, database operations, and pipeline behavior.

## Architecture

The execution pipeline follows these stages:

1. Prompt analysis
2. Model selection
3. LLM execution
4. Execution and event tracking
5. Cost estimation
6. Quality evaluation
7. PostgreSQL persistence
8. Execution analytics

Execution and quality evaluation are handled separately, so a quality evaluation failure does not automatically invalidate a successfully generated response.

## Technology Stack

- **Language:** Python
- **LLM Runtime:** Ollama
- **Language Model:** Llama 3.1 8B
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Testing:** pytest
- **Infrastructure:** Docker Compose
- **Configuration:** Environment variables and python-dotenv

## Requirements

- Python 3.14 or later
- Docker Engine
- Docker Compose
- Ollama model `llama3.1:8b`
- An environment capable of running the required Python dependencies

## Project Structure

- `app/` — Application logic, services, schemas, and database integration.
- `app/schemas/` — Pydantic schemas for requests, execution results, selection criteria, and evaluations.
- `app/analyzer/` — Prompt analysis.
- `app/registry/` — Model registry and model metadata management.
- `app/selector/` — Model selection and scoring strategies.
- `app/execution/` — LLM execution and pipeline orchestration.
- `app/cost/` — Execution cost estimation.
- `app/database/` — Database engine and models.
- `app/analytics/` — Execution analytics.
- `app/tracking/` — Execution events and cost tracking.
- `app/evaluation/` — Response quality evaluation.
- `scripts/` — Database initialization and model registration.
- `tests/` — Automated tests.
- `docker-compose.yml` — Local PostgreSQL and Ollama services.
- `pyproject.toml` — Python package configuration and dependencies.
- `.env.example` — Example environment configuration.

## Installation

### 1. Clone the repository

Replace the placeholder with your repository URL.

    git clone <YOUR_GITHUB_REPOSITORY_URL>
    cd ai-execution-intelligence

### 2. Create and activate a virtual environment

Create a Python virtual environment:

**Linux / macOS**

    python3 -m venv venv
    source venv/bin/activate

**Windows (PowerShell)**

    py -m venv venv
    .\venv\Scripts\Activate.ps1

**Windows (Command Prompt)**

    py -m venv venv
    venv\Scripts\activate.bat

### 3. Configure environment variables

Create your local environment file:

    cp .env.example .env

Open `.env` and configure the following variables:

- `POSTGRES_USER` — PostgreSQL username.
- `POSTGRES_PASSWORD` — PostgreSQL password.
- `POSTGRES_DB` — PostgreSQL database name.
- `DATABASE_URL` — SQLAlchemy connection string.

Ensure that the username, password, and database name in `DATABASE_URL` match the corresponding PostgreSQL variables.

For example, if you choose a custom username and password, use the same values in both the PostgreSQL variables and the connection string.

Keep `.env` local and never commit real credentials.

### 4. Start the infrastructure

Start PostgreSQL and Ollama:

    docker compose up -d

Download the required model:

    docker exec -it ai_intelligence_ollama ollama pull llama3.1:8b

### 5. Install the project

Install the application and development dependencies:

    python -m pip install -e ".[dev]"

### 6. Initialize the database

Create the database tables:

    python -m scripts.create_table

Register the model:

    python -m scripts.register_models

## Usage

Run the application:

    python -m app.main

The application analyzes a prompt, selects a suitable model, executes the request, persists execution data, and attempts to evaluate the generated response.

The output includes the selected model, execution identifier, and available quality metrics.

## Testing

Run the complete test suite:

    python -m pytest

The tests cover core application services, model selection, execution tracking, persistence behavior, and pipeline error handling.

## Configuration

The application uses environment variables loaded from `.env`.

The main settings include:

- `DATABASE_URL` — PostgreSQL connection string.
- `OLLAMA_HOST` — Ollama API endpoint.
- `ANALYZER_MODEL` — Model used for prompt analysis.

See `.env.example` for the configuration template.

## Current Status

The project is under active development.

The current implementation focuses on the core execution pipeline, model selection, persistence, event tracking, cost estimation, quality evaluation, and automated testing.

## Roadmap

- Improve execution analytics.
- Compare models using measured execution results.
- Refine model-selection strategies.
- Improve cost and performance analysis.
- Expand quality evaluation and automated tests.

## License

No license has been specified yet. Until a license is added, the repository should not be assumed to grant permission to redistribute or reuse its code.
