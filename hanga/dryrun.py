__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"


import click

@click.command(name='dryrun')
def dryrun():
    """
    Dry run a stack by via a change-set creation
    """
    click.echo('dryrun')