![](https://cdn.vivaanverma.com/02824232-1DCB-465D-9D73-67D80F829601.jpeg)

# Sirius: create APIs that shine like a star

Sirius, commonly known as the brightest star in the night sky, is also an
API framework written with ease-of-use and developer experience in mind.
By learning from frameworks written not only in Python, but other languages
too, Sirius provides a set of distinctive features aiming to provide the best
possible experience developing a dazzling application on a starry night.

[![Twitter](https://img.shields.io/twitter/follow/siriusapi?color=%23e39ff6&logo=twitter&logoColor=white&style=for-the-badge)](https://twitter.com/siriusapi)

## Features

- File-system based routing
- Full ASGI compliance
- A simple configuration system
- A zero-boilerplate experience
- A CLI utility
- State-of-the-art documentation

## Getting Started

→ [Installation](#installation)<br/>
→ [Usage](#usage)

## Installation

Currently, the only way to install Sirius is using `pip`, the Python package manager.
Either within a virtual environment, or globally, Sirius can be installed with:

```zsh
$ python3 -m pip install sirius-api
```

## Usage

After installing Sirius, you can create a new project! Throughout the documentation we'll
work on an API that mocks data about planets 🪐.

### Project Structure

A basic Sirius project will contain the following files in its root directory:

→ `pyproject.toml`/`poetry.lock` - Files to define dependencies, Sirius is in here!<br/>
→ `sirius.config.toml` - Sirius needs configuration... you provide configuration!

Then, the truly galactic part. File-system routing!
Create a directory called `src` and within it a subdirectory named `routes`.

We have now entered holy land - there is no turning back once you realise that every file
you define from now on, will be an endpoint in your API.
