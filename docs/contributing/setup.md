
# Development setup

Here are some instructions for how you can get started contributing to the
project. I look forward to seeing your awesome features!

## 0. Prerequisites

To work effectively with the project, you'll need to have a bit of knowledge of
a few tools, and install a few programs to your computer.

### a. Knowledge

* Know some basic Python - [this video](https://youtu.be/rfscVS0vtbw) is a
  great resource.

* Understand the basic concepts of Git and GitHub. [GitHub's quick-start guide](https://docs.github.com/en/get-started/quickstart/hello-world)
  is a good place to start with this. You'll also want to understand
  [how forks work](https://docs.github.com/en/get-started/quickstart/contributing-to-projects).

### b. Software

* Python - the programming language used by the Universal Controller Script.
  Installed by default on MacOS and Linux. You'll need to install it
  from [here](https://www.python.org/downloads/) on Windows.

* Poetry - the dependency management system. You can install it by running the
  instructions [available here](https://python-poetry.org/docs/).

* A code editor - I use [Visual Studio Code](https://code.visualstudio.com) so
  it will work great with this project, but if you prefer something else that
  is fine too.

## 1. Creating and installing your own development copy of the project

The Universal Controller Script is a highly-advanced piece of software, and so
to get the best experience when working with it, it takes a little bit of
setup. These instructions walk you through the process of creating a
development copy of the repository, linking it to FL Studio, and setting up
your code editor to get the best support while you work.

1. Create a fork of the project, so that you can work without the risk of
   breaking the existing project.

2. Clone your copy of the project to a location of your choice. Many developers
   have a `Source` folder where they keep all their programming work. Don't
   clone the project directly into your `FL Studio/Settings/Hardware` folder.

3. Remove any existing installation of the Universal Controller Script, since
   they will conflict with your development build.

4. Create a symbolic link between the project's `src` directory in FL Studio's
   `Documents/Image-Line/FL Studio/Settings/Hardware` folder, so that FL Studio
   can detect it. Note that to create symbolic links, you should

   * On Windows inside an admin command prompt (this doesn't work in
     PowerShell), run the command
     `mklink /D "C:\Users\<username>\Documents\Image-Line\FL Studio\Settings\Hardware\UniversalController" "\path\to\clone\location\Universal-Controller-Script\src"`.

   * On MacOS (please test) and Linux, run
     `ln -s /path/to/clone/button/Universal-Controller-Script/src/ '/path/to/user/directory/Documents/Image-Line/FL Studio/Settings/Hardware/UniversalController'`.

5. Launch FL Studio and follow the [regular setup instructions](../setup.md)
   to associate the script with your device.

6. Open the repository in your editor of choice. In VS Code, you should open
   the entire project folder for the best experience.

7. Install any recommended extensions if you are in VS Code.

8. Install the project dependencies by running `poetry install` in your
   terminal (make sure you do this in the project's folder).

9. Ensure that your environment is set up correctly by running the script in
   your terminal. You can use the command `poetry run python ./src/device_universal.py`.
   If it is working, you will see the start-up message before the program
   exits.

10. To activate proper auto-completion for the project in VS Code, open any
    Python file, then choose the Poetry environment using the
    [Select interpreter command](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter).

## 2. Creating a contribution

Like with most open source projects, contributions are best of they are small
and atomic, for example adding support for one plugin or fixing one bug. Feel
free to repeat these steps as many times as necessary.

1. Create a Git branch for your work. Most developers name their branch with
   both their name and the feature they are working on. For example, if I was
   adding support for the "Super fancy" plugin, I might call my branch
   `miguel-plugin-super-fancy`.

2. Refer to [the other documentation for contributors](./README.md) for help
   with creating your contribution. Remember you can always ask for help on the
   [Discord server](https://discord.gg/6vpfJUF) if you need it!

3. When you've finished working, create a commit and push your work. In VS
   Code, this can be done easily using [the Git panel](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git#_staging-and-committing-code-changes).

4. [Create a pull request](https://docs.github.com/en/get-started/quickstart/contributing-to-projects#making-a-pull-request)
   for your changes. Make sure your pull request has plenty of information so I
   can understand what you changed and why you changed it.

5. Wait for a code review. I want to be sure that all of the code in this
   project is of the highest quality, so please don't be upset if I have a lot
   to criticize with your contribution - it is coming from a place of love, and
   I'm happy to work with you to make your work the best it can be! If I make
   any suggestions for improvements, go back through the code and create and
   push more commits to fix them.

6. Get your code merged! Congratulations on completing your contribution, and
   thanks for your work on the project!
