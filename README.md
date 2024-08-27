# BrainAgriculture

This Django project is containerized using Docker and includes various utilities for development and management. Below you'll find instructions for setting up, running, and maintaining the project.

## Table of Contents

- [Initial Setup](#project-setup)
- [Fixtures](#fixtures)
- [Testing and Linting](#testing-and-linting)
- [Development Commands](#development-commands)
- [Cleanup](#cleanup)


## Project Setup

### Prerequisites

- Docker
- Docker Compose
- Python 3.12
- [Just: a handy way to save and run project-specific commands, check the instalation process](https://github.com/casey/just) 

## Initial Setup

1. **Create the virtual environment and install the project dependencies:**

   ```bash
   just venv
   ```

2. **Start the project using Docker Compose:**

   ```bash
   just run-start
   ```

3. **The _run-set-db_, it applies database migrations, creates a Django superuser (user: admin, password: admin), and loads initial fixture data into the database:**

    ```bash
   just run-set-db
   ```

## Fixtures

- **Run fixtures:**
    Fixtures for crops and rural producers are available in the `brain_ag/api/fixtures` directory. Load these fixtures into the database with the following command:
    ```bash
    just run-fixtures
    ```

## Testing and Linting

- **Run the tests:**
    This command executes the Django test suite inside the Docker container, specifically targeting the tests located in `brain_ag/api/tests`.
    ```bash
    just run-test
    ```



- **Check code formatting and linting:**
    This command performs the following checks:
    - **Black**: Checks if the code adheres to the Black code style.
    - **isort**: Checks if import statements are properly sorted.
    - **flake8**: Checks for code style violations and errors.
    
    ```bash
    just run-lint
    ```
    
## Development Commands

- **Start the development environment:**

    ```bash
    just run-start
    ```

- **Stop the development environment:**

    ```bash
    just run-down
    ```

- **Rebuild the Docker containers:**

    ```bash
    just run-build
    ```

- **Rebuild and restart the Docker containers:**

    ```bash
    just run-build-start
    ```

- **Open a bash shell in the API container:**

    ```bash
    just run-docker-bash
    ```

- **Open the Django shell:**

    ```bash
    just run-django-shell
    ```

## Cleanup

- **Clean up the environment:**
    This command stops the Docker containers, removes the virtual environment, and cleans up temporary files.
    ```bash
    just clean
    ```

  

