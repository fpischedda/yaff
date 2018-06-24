"""
Yaff game runner

It runs a Yaff based appliction specifiyng its package name, example:
$ yaff run example

this script will look up the module example.main and will try to execute
the run function
"""

import importlib.util
import sys
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    '--module-name',
    default='main',
    help='The name of the module containing the run function')
@click.argument('name')
def run(module_name, name):
    sys.path.insert(0, '.')
    module = importlib.import_module(name)
    module = getattr(module, module_name)
    module.run()
