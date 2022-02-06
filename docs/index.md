# Sirius

![Sirius Logo](https://raw.githubusercontent.com/doublevcodes/sirius/main/docs/img/sirius.jpg)

*Create APIs that shine like a star*

---

Sirius, commonly known as the brightest star in the night sky, is also an API framework written with ease-of-use and developer experience in mind. By learning from frameworks written not only in Python, but other languages too, Sirius provides a set of distinctive features aiming to provide the best possible experience developing a dazzling application on a starry night.

## Key features

Sirius aims to take developer experience to the next level and so it provides a set of features aiming to provide a developer with little to no headaches! Some of these include, but aren't limited to:

- **File-based routing**: Perhaps what sets Sirius apart from the rest, this allows the developer to watch their API grow - inside a directory!
- **A zero-boilerplate experience**: With this, all one has to do is `pip install sirius-api`, and the rest will be done for you. Simple applications don't even need to import Sirius!
- **A CLI utility**: Don't want to programmatically be running Sirius with calls to the framework? Easy, open a terminal and `sirius dev` will do the job for you.

## Requirements

Sirius aims to be next-generation and so currently only supports **Python 3.10**. Backwards compatibility to older Python versions may be introduced at a later date.

You don't need to install any external packages to run a Sirius application... apart from Sirius :sweat_smile:

## Installation

Simple:

=== "Pip"

    ```zsh
    $ pip install sirius-api
    ```

=== "Pipenv"

    ```zsh
    $ pipenv install sirius-api
    ```

=== "Poetry"

    ```zsh
    $ poetry add sirius-api
    ```

...and you're ready to dive into an astronomical world of fun!

## Example

### Build it

A simple Sirius API that defines a root endpoint (`/`) that responds to `GET` requests with a message would look like the following:

```py
def get():
    return "Astronomically amazing!"
```

!!! note "Where does this go in my project?"
    
    The file this would be found in relative to your project would be `./routes/__init__.py`. as you'll soon lean, a file named `__init__.py` in Sirius represents a root endpoint. Keep flying! You're nearly there!

### Run it

Now that you've defined what your API should do, we need to run it! So open up a terminal and run `sirius dev`. This should start up a development server that uses
[Uvicorn](https://www.uvicorn.org/) on port 8000, so have a look at <http://localhost:8000>.

Depending on your browser, you should see some variation of the text: **Astronomically amazing!**

!!! success "You've made a complete Sirius app!"

## Recommended resources

### HTTP Client

As you progress further in your API development adventure, it would be suggested to not rely on your browser for testing them.
Instead, [HTTPie](https://httpie.io), which is a HTTP client for the CLI with a desktop app and website currently in beta, is recommended.
It provides easy-to-remember syntax and is very powerful. A simple `DELETE` request to `localhost:8000/foo`, using `sirius` as the `lib` query parameter can be represented as

```zsh
$ http POST :8000/foo sirius==lib
```

Yes: it's that easy!

### REST Architecture

The [MDN Web Developer Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP) explains REST concepts in extreme detail. Here you can find detail information on HTTP verbs
and HTTP status codes. Have a good read!


!!! tldr "Have fun developing with Sirius!"