
# Contributing

## Getting Started

1.  Set up the project as per the [main instructions](../setup.md), but instead
    of cloning the project directly, 
    [create a fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
    where your work can be done without the risk of breaking the project. When
    your work is done, you can create a pull request to merge your improvements
    into the main project.
2.  Get familiar with the project's [style guidelines](style.md)
3.  Note that documentation is only of overarching designs and how-tos. Code in
    the project is documented using docstring, and will be displayed inline by
    most code editors.
5.  Install [Python](https://www.python.org/downloads/) (if you're on Windows,
    on MacOS it is built in)
4.  Open the repository in your editor of choice. I've ensured it works well with
    [VS Code](https://code.visualstudio.com), but others should be fine too.
5.  Install any recommended extensions if you are in VS Code
6.  Open a terminal in the repository folder and create a Python 
    [virtual environment](https://docs.python.org/3/library/venv.html). This will
    keep the project's dependencies separate from any other ones you have
    installed, ensuring nothing can get broken. Run `python -m venv .venv`.
7.  When VS Code or your editor prompts you to activate the virtual environment,
    do so.
8.  Activate the virtual environment in your terminal (refer to the virtual
    environment documentation linked above). In VS Code you can just restart your
    terminal.
9.  Install the project dependencies. Run `pip install -r requirements.txt`.
10. Ensure that your coding environment is functioning correctly by running the
    code from your editor. If all your dependencies are set up correctly, it
    will start up, print the welcome message then exit.

## Documentation for Contributors

* [Devices](devices.md)
* [Plugins](plugins.md)
