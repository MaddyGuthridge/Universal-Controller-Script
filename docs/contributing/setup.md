
# Contributing

Note that this documentation is only of overarching designs and how-tos. Code
in the project is documented using docstring, and will be displayed inline by
most code editors.

## Getting Started

1.  If you haven't already, create a [GitHub](https://github.com/) account, and
    [set up an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

2.  [Create a fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
    of the project, so that you can work without the risk of breaking the
    existing project.

3.  Run a `git clone --recursive git@github.com:[YourUsername]/Universal-Controller-Script.git`
    command with your terminal inside a directory of your choosing (perhaps
    create a `Source` directory in your user data folder).

4.  Since the codebase contains code that isn't required by a regular
    installation, we will need to create a symbolic link between the project's
    `src` directory in FL Studio's
    `Documents/Image-Line/FL Studio/Settings/Hardware` folder, so that FL
    Studio can detect it. Note that to create symbolic links, you should

    * On Windows inside an admin command prompt (this doesn't work in
      PowerShell), run the command
      `mklink /D "C:\Users\<username>\Documents\Image-Line\FL Studio\Settings\Hardware\UniversalController" "\path\to\clone\location\Universal-Controller-Script\src"`.

    * On MacOS (please test) and Linux, run
      `ln -s /path/to/clone/button/Universal-Controller-Script/src/ '/path/to/user/directory/Documents/Image-Line/FL Studio/Settings/Hardware/UniversalController'`.

3.  Install [Python](https://www.python.org/downloads/) if you're on Windows.
    On MacOS and Linux it is built in.

4.  Open the repository in your editor of choice. I've ensured it works well
    with [VS Code](https://code.visualstudio.com), but others should be fine
    too.

5.  Install any recommended extensions if you are in VS Code.

6.  Open a terminal in the repository folder and create a Python
    [virtual environment](https://docs.python.org/3/library/venv.html). This
    will keep the project's dependencies separate from any other ones you have
    installed, ensuring nothing can get broken. Run `python -m venv .venv`.

7.  When VS Code or your editor prompts you to activate the virtual
    environment, do so.

8.  Activate the virtual environment in your terminal (refer to the virtual
    environment documentation linked above). In VS Code you can just restart
    your terminal.

9.  Install the project dependencies. Run `pip install -r requirements.txt`.

10. Ensure that your coding environment is functioning correctly by running the
    code from your editor. If all your dependencies are set up correctly, it
    will start up, print the welcome message then exit.

11. Get familiar with the project's [style guidelines](style.md)

12. Make sure you've joined the [Discord server](https://discord.gg/6vpfJUF) 
    so that I can help out if you run into any issues.
