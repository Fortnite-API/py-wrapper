# Documentation
This is the documentation for the project. It is written in reStructuredText and can be found in this directory.

## Previewing Documentation
### Building for Development
It's recommended to use [sphinx auto build](https://pypi.org/project/sphinx-autobuild/) to preview the documentation. 
In this directory, run the following command:

```bash
sphinx-autobuild . ./_build/html
```

### Building for Production
To build the documentation for production, run the following command in this directory:

```bash
sphinx-build -b html -j auto -a -n -T -W --keep-going . _build/html
```

Ensure you have the following dependencies installed in your environment:

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -U -r requirements.txt
pip install -e .[docs]
```