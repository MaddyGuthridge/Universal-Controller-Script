
# Style Guidelines

This software is intended to be a collaborative work, and contributions are
welcome from anyone, but in order to maintain the quality of the program, there
are guidelines in place for code style.

## Code Style

* Indentation: 4 spaces
* Typing: where it is reasonable, type hints should always be included on
  function definitions. The project should remain compliant with MyPy.
* Modules and functions should be documented with docstring. If you use VS Code,
  a configuration for the Python Docstring Generator extension is provided which
  should be used automatically. For reference, this file is provided in 
  `resources/docstring_template.mustache`.

## Development environment

* I'd recommend working on the project using 
  [VS Code](https://code.visualstudio.com), with the recommended extensions
  installed. This should help ensure that the code is safe and clean.
  You can use any editor you see fit, but it may be more difficult to maintain
  code style requirements.
* You should work on this project within a
  [virtual environment](https://docs.python.org/3/library/venv.html) in order to
  avoid the risk of dependency conflicts. Make sure you install the dependencies
  from `requirements.txt`.
