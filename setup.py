import re

import setuptools
from setuptools import setup

version = ''
with open('fortnite_api/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)  # type: ignore

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()

extras_require = {
    'tests': ['pytest', 'pytest-asyncio', 'pytest-cov', 'python-dotenv'],
    'docs': ['sphinx', 'sphinxcontrib_trio', 'sphinxcontrib-websupport', 'typing-extensions', 'furo', 'sphinx-copybutton'],
    'dev': ['black', 'isort'],
    'speed': [
        'orjson',
    ],
}

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='fortnite-api',
    author='Luc1412',
    author_email='Luc1412.lh@gmail.com',
    url='https://github.com/Fortnite-API/py-wrapper',
    project_urls={
        # "Documentation": "https://fortnite-api.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/Fortnite-API/py-wrapper/issues",
        "Code": "https://github.com/Fortnite-API/py-wrapper",
    },
    version=version,
    packages=setuptools.find_packages(),
    license='MIT',
    description='A python wrapper for Fortnite-API.com',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires='>=3.8.0',
    download_url=f'https://github.com/Fortnite-API/py-wrapper/archive/refs/tags/v{version}.tar.gz',
    keywords=['fortnite', 'fortnite-api.com', 'shop', 'cosmetics', 'fortnite api', 'fortnite shop'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
