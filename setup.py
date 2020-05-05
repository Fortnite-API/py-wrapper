import re

import setuptools
from setuptools import setup

version = ''
with open('fortnite_api/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')


readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name='fortnite-api',
    author='Luc1412',
    author_email='Luc1412.lh@gmail.com',
    url='https://github.com/Fortnite-API/py-wrapper',
    project_urls={
        # "Documentation": "https://fortnite-api.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/Fortnite-API/py-wrapper/issues",
        "Code": "https://github.com/Fortnite-API/py-wrapper"
    },
    version=version,
    packages=setuptools.find_packages(),
    license='MIT',
    description='A python wrapper for Fortnite-API.com',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=['requests>=2.22.0', 'aiohttp>=3.3.0'],
    python_requires='>=3.5.3',
    download_url='https://github.com/Fortnite-API/py-wrapper/archive/v2.0.1.tar.gz',
    keywords=['fortnite', 'fortnite-api.com', 'shop', 'cosmetics', 'fortnite api', 'fortnite shop'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
