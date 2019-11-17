import re

import setuptools

long_description = ''
with open("README.md", "r") as fh:
    long_description = fh.read()

version = ''
with open('fortnite_api/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

requirements = ['requests>=2.22.0', 'aiohttp>=3.3.0,<3.6.0']
try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    pass

setuptools.setup(
    name='fortnite-api',
    packages=setuptools.find_packages(),
    version=version,
    license='MIT',
    description='Wrapper for Fortnite-API.com',
    author='Luc1412',
    author_email='Luc1412.lh@gmail.com',
    url="https://github.com/Fortnite-API/py-wrapper",
    keywords=['fortnite', 'fortnite-api.com', 'shop', 'cosmetics'],
    install_requires=requirements,
    project_urls={
        #"Documentation": "",
        'Issue tracker': "https://github.com/Fortnite-API/py-wrapper/issues",
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.5.3',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
