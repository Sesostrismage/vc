# Visualization Course (VC) repo
Repository to illustrate tips and tricks for exploration and visualization of tabular data using Python. The link to the companion presentation [can be found here](https://docs.google.com/presentation/d/1qKf_4JmTFqb-OldIl1Fp1gvSKnPdeFfY531qPktCGRc/edit?usp=sharing).

All the example scripts are in /scripts

## Setup Python
Install Python 3, for example using [Anaconda](https://www.anaconda.com/products/individual).

Optionally create a separate environment to use with this repo: [Instructions](https://docs.anaconda.com/anaconda/navigator/getting-started/#navigator-managing-environments)

Clone this repo to somewhere on your computer, then make sure that the Python environment can find it py using a .pth file. If your Python environment is e.g. at `C:\Anaconda3\envs\vc` and your repo is at `C:\code\vc`, then in `C:\Anaconda3\envs\vc\Lib\site-packages` create a file ending in .pth (for example, vc.pth), where the only text in the file is the path to the folder containing the repo:

```
C:\code
```
This lets you use the normal import statements, where the repo is accessible by `import vc`

Install the necessary packages to run the code in this repo using the requirements.txt in the root of the repo: [Instructions](https://note.nkmk.me/en/python-pip-install-requirements/)

You can run the scripts via the command line:
```
streamlit run [path to file from root of the repo]
bokeh serve --show [path to file from root of the repo]
```
, or...

## Setup VS Code (optional)
My preferred development environment is [VS Code](https://code.visualstudio.com/) for ease of use, being able to do most tasks in one place, and high customizability.

Using Anaconda Navigator, install the `conda` package in the environment. This package seems to be needed to automatically activate the environment when opening a terminal window in VS Code.

In the terminal window, press `Select default profile` to be Command Prompt. You still need to close the first terminal the automatically opens up, but when you then open a new terminal, it should automatically activate the chosen Python environment. I have no idea why it has to be like this, but it's the only setup I've found that works, even if it's clunky. Honestly, you might still need to fiddle around and look on StackOverflow to figure out how  to auto-active the Python environment. If someone knows a better way to set this up, please let me know. :-)

Install the [Multi-command extension](https://marketplace.visualstudio.com/items?itemName=ryuta46.multi-command).

Set up multi-commands to run Streamlit and Bokeh scripts easily. This is done in VS Code by calling the command `Preferences: Open Settings (JSON).` There, add the following:

```
"multiCommand.commands": [
    {
        "command": "multiCommand.streamlitActiveFile",
        "label": "Streamlit: Run Active File",
        "description": "Streamlit run active file in active terminal",
        "sequence": [
            "workbench.action.terminal.focus",
            {
                "command": "workbench.action.terminal.sendSequence",
                "args": {
                    "text": "streamlit run ${relativeFile}\u000D"
                }
            }
        ]
    },
    {
        "command": "multiCommand.bokehActiveFile",
        "label": "Bokeh: Serve Active File",
        "description": "Bokeh serve active file in active terminal",
        "sequence": [
            "workbench.action.terminal.focus",
            {
                "command": "workbench.action.terminal.sendSequence",
                "args": {
                    "text": "bokeh serve --show ${relativeFile}\u000D"
                }
            }
        ]
    }
]
```
In VS Code, run the command `Preferences: Open keyboard shortcuts (JSON)` and add the following:
```
{
    "key": "ctrl+l",
    "command": "multiCommand.streamlitActiveFile"
},
{
    "key": "ctrl+shift+b",
    "command": "multiCommand.bokehActiveFile"
}
```
Now you should be able to run Streamlit and Bokeh scripts with the shortcuts above.
