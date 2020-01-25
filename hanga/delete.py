import click

@click.command(name='delete')
def delete():
    """
    Delete a stack
    """
    click.echo('delete')