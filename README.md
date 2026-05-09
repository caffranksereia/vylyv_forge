# Forge

Forge is a Python CLI tool for generating clean project structures, APIs, SaaS backends, and modules faster.

Built with:

- Python
- Typer
- Rich

## Features

- Interactive terminal menu
- Create Python projects
- Create API projects
- Create SaaS backend projects
- Create modules inside existing projects
- Optional router generation
- Optional test generation
- Optional CRUD starter generation
- Automatic virtual environment creation
- Automatic pip upgrade
- Automatic dependency installation
- Safe `requirements.txt` update without duplicates

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/vylyv-forge.git
cd vylyv-forge
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Install Forge locally:

```bash
python -m pip install -e .
```

## Usage

Start Forge with the interactive menu:

```bash
forge
```

You will see:

```txt
1 - Create project
2 - Create module
3 - Show help
0 - Exit
```

## Create a project

Interactive mode:

```bash
forge
```

Direct command:

```bash
forge create my_project
```

Create a basic Python project:

```bash
forge create my_project --template basic
```

Create an API project:

```bash
forge create my_api --template api
```

Create a SaaS backend project:

```bash
forge create my_saas --template saas
```

Short option:

```bash
forge create my_saas -t saas
```

## Available templates

### Basic

A simple Python project structure.

```txt
my_project/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── main.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

### API

A FastAPI starter project.

```txt
my_api/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── schemas/
│   └── services/
└── tests/
```

Run the API:

```bash
uvicorn src.main:app --reload
```

### SaaS

A SaaS backend architecture starter.

```txt
my_saas/
├── README.md
├── requirements.txt
├── .env.example
├── logs/
├── src/
│   ├── app.py
│   ├── core/
│   ├── database/
│   ├── modules/
│   ├── routers/
│   └── shared/
└── tests/
```

Run the SaaS backend:

```bash
uvicorn src.app:app --reload
```

## Create a module

Go inside a generated project:

```bash
cd my_saas
```

Create a module:

```bash
forge module users
```

Create a module with router:

```bash
forge module users --with-router
```

Create a module with router and tests:

```bash
forge module users --with-router --with-tests
```

Create a module with CRUD starter files:

```bash
forge module users --with-router --with-tests --crud
```

Do not update `requirements.txt`:

```bash
forge module users --no-requirements
```

## Module structure

Example:

```bash
forge module clients --with-router --with-tests --crud
```

Creates:

```txt
src/modules/clients/
├── __init__.py
├── dto/
│   ├── __init__.py
│   └── create_clients_dto.py
├── repository/
│   ├── __init__.py
│   └── clients_repository.py
├── service/
│   ├── __init__.py
│   ├── clients_service.py
│   └── clients_crud_service.py
└── validators/
    ├── __init__.py
    └── clients_validator.py
```

Also creates:

```txt
src/routers/clients_router.py
tests/test_clients.py
```

## Options

### Project command

```bash
forge create NAME
```

Options:

```txt
--template, -t     Choose template: basic, api, saas
--no-venv          Do not create virtual environment
--no-install       Do not install dependencies
```

Example:

```bash
forge create demo_api -t api --no-install
```

### Module command

```bash
forge module NAME
```

Options:

```txt
--with-router       Create router file
--with-tests        Create test file
--crud              Create CRUD starter files
--no-requirements   Do not update requirements.txt
```

Example:

```bash
forge module orders --with-router --with-tests --crud
```

## Development

Install locally in editable mode:

```bash
python -m pip install -e .
```

Run help:

```bash
forge --help
```

Run interactive menu:

```bash
forge
```

## Requirements

Forge requires Python 3.10 or higher.

Main dependencies:

```txt
typer
rich
```

## Roadmap

Planned features:

- Add database migration generator
- Add router registration automation
- Add service/repository CRUD templates
- Add Docker template
- Add authentication starter
- Add `.env` setup helper
- Add project config file
- Add plugin system
- Add update command

## License

MIT License.

## Author

Created by Vylyv.