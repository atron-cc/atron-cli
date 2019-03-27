import setuptools
from distutils.core import setup
from atron_cli import VERSION

setup(
    name='atron_cli',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    version=VERSION,
    description='A tool to intract with your MicroPython board.',
    author='Ahmadreza Zibaei',
    install_requires=["click"],
    author_email='zibaeiahmadreza@gmail.com',
    url='https://github.com/atron-cc/atron-cli',
    license='MIT',
    classifiers=[
        "Topic :: Utilities",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['micropython', 'hardware', 'circuitpython'],
    entry_points='''
        [console_scripts]
        atron=atron_cli.atron:cli
    ''',
)
