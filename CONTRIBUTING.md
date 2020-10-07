# Contributing

## General Python info
In this package we make extensive use of the [Returns library](https://github.com/dry-python/returns). Its a library that forces us to try and write None free code and also wraps exceptions. It changes return values to Result 'Monads' with Success and Failure return containers or Maybe and Nothing containers. This helps us to do railway-oriented-programming when working with mapping.


## New Environment Tools
Lately we have gotten a few great python environment managers. The first being [PyEnv](https://github.com/pyenv/pyenv). Pyenv makes working with multiple versions of python easier. The second tool is [Poetry](https://poetry.eustace.io/). Poetry lets us create a lock file of all our dependencies, this means that both version of python and version of each dependency and its dependencies will be equal for everyone working on the project. It also uses the new pyproject.toml file which is the 'new' setup.py and requirements.txt in 1 file. Poetry also handles building and publishing.


## Setup the tools

Get pyenv - pyenv lets you work with multiple versions of python.
```sh
brew update
brew install pyenv
```

If you are using bash, add the following to your `~/.bash_profile` to automatically load pyenv. If you are using another shell, run `pyenv init` and it will tell you how to set it up.
```sh
eval "$(pyenv init -)"
```

Install a version of python 3.7+: This installs a clean python to pyenvs folders and lets us reference that as a 'base' in our virtualenvs.
```sh
pyenv install 3.7.4
```

Get poetry - dependency management.
```sh
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

Make poetry create virtualenvs inside of project folders. This makes it easier for IDE's to run in the correct virtualenv while debuging/running linters etc.
```sh
poetry config virtualenvs.in-project true
```

## Setup dev environment

Activate pyenv for the current shell.
```sh
pyenv shell 3.7.4
```

This creates a virtualenv and installs all dependencies including dev.
```sh
poetry install
```

Now test that everything works. Poetry run runs a command in the virtualenv.
```sh
poetry run pytest
```

Initialize pre-commit hooks for git.
```sh
poetry run pre-commit install
```
