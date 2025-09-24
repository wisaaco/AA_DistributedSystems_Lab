UV Basics
=========


# Project configuration
- create a project
uv init

- install a virtual env. (or with an specific python version)
uv venv
uv venv --python 3.10

- install dependencies 
- if there is not specific version of python in the project, uv will use the default one in the system
uv add pandas
uv add pandas==2.0.0

- install from old requirements.txt file
uv add -r requirements.txt

- from another project.toml
uv sync --from-file project.toml

- Sync dependencies in the project
uv sync

# How to run a script
uv run main.py

Note: VS automatticaly detects your .venv

# If you want to clean the project: remove the .venv folder
# If u want to restart it: uv sync
