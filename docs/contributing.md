# Contributing

## General Python info
In this package we make extensive use of the [Returns library](https://github.com/dry-python/returns). Its a library that forces us to try and write None free code and also wraps exceptions. It changes return values to Result 'Monads' with Success and Failure return containers or Maybe and Nothing containers. This helps us to do kind of railway-oriented-programming when working with mapping.

We also use [marshmallow](https://marshmallow.readthedocs.io), which is the tool we se to describe models and do validation.

## New Environment Tools
Lately we have gotten a few great python environment managers. The first being [PyEnv](https://github.com/pyenv/pyenv). Pyenv makes working with multiple versions of python easier. The second tool is [Poetry](https://poetry.eustace.io/). Poetry lets us create a lock file of all our dependencies, this means that both version of python and version of each dependency and its dependencies will be equal for everyone working on the project. It also uses the new pyproject.toml file which is the 'new' setup.py and requirements.txt in 1 file. Poetry also handles building and publishing.


## Setup the tools

get pyenv - pyenv lets you work with multiple versions of python
```sh
$ brew update
$ brew install pyenv
```

Put this command into the of `~/.bash_profile` or run `pyenv init` to make sure where to put it for for example zsh.
```
$ eval "$(pyenv init -)"
```

install a version of python 3.7+: This installs a clean python to pyenvs folders and lets us reference that as a 'base' in our virtualenvs.
```sh
$ pyenv install 3.7.4
```

get poetry - dependency management:
```sh
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

Make poetry create virtualenv in project folder. This makes it easier for IDE's to run correct virtualenv while debuging/running linters etc.
```sh
$ poetry config settings.virtualenvs.in-project true
```

## Setup dev environment

activate pyenv for the current shell
```sh
$ pyenv shell 3.7.4
```

This creates a virtualenv and installs all dependencies including dev:
```sh
$ poetry install
```

Now test that everything works. poetry run, runs a command in the virtualenv
```sh
$ poetry run pytest
```

initialize pre-commit hooks for git
```sh
$ poetry run pre-commit install
```
