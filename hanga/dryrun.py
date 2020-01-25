import click

@click.command(name='dryrun')
def dryrun():
    """
    Dry run a stack by via a change-set creation
    """
    click.echo('dryrun')