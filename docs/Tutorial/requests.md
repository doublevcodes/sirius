# Receiving requests

Perhaps the most important part of any API is the ability to receive requests and carry out a certain
function based on the characteristics of this request.

For a simple REST API, at a high level, two things define what happens to a request.

!!! question inline end "Need a refresher on HTTP methods? Check out [this resource](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)"

1. The request endpoint
2. The HTTP request method

Sirius has ways to manage both of these with such ease. It seems logical to begin with endpoints, since HTTP methods
form a subset of operations upon each endpoint.

## Endpoints

An endpoint in a Sirius API is represented by a Python file in a certain directory. By default this magical directory
is `src/routes`. The following directory structure:

```
src/
 └─ routes/
     ├─ __init__.py
     ├─ baz.py
     └─ foo/
         ├─ __init__.py
         └─ bar.py
```

represents an API with the following endpoints:

- `/`
- `/baz`
- `/foo`
- `/foo/bar`