# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## Virtual environment

* `make create_environment` - Create virtual environment
* `source venv/bin/activate` - Activate virtual environment
* `ipython kernel install --user --name=venv` - Install virtual environment as the kernel of jupyter notebooks

## Tricks from "Data Science if Software: Developer #lifehacks for the Jupyter Data Scientist"

["Data Science if Software: Developer..." - Peter Bull l ODSC East 2017](https://youtu.be/HM56wCNxCnQ)

```
pip install nbdime
# in a git repo,
git-nbdiffdriver config --enable
git diff notebooks/
```

```
# paste https://gist.github.com/pjbull/221685a8e03a01baaf1e (bit.ly/py-html-config) into:
vim ~/.jupyter/jupyter_notebook_config.py
cd notebooks
touch .ipynb_saveprogress
# so now, when a .ipynb is edited, a directory is created with plain .py and .html copies
```
