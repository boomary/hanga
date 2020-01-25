import click

@click.option('--name', '-n',
                required=True,
                type=click.STRING,
                help='Stack name')

@click.option('--template', '-t',
                required=True,
                type=click.STRING,
                help='Stack template')

@click.option('--bucket', '-b',
                required=True,
                type=click.STRING,
                help='S3 bucket prefix')

@click.option('--params', '-p',
                type=click.STRING,
                help='Parameter file')

@click.option('--tags', '-t',
                type=click.STRING,
                help='Tag file')               

@click.option('--upload', '-u',
                is_flag=True,
                help='Upload to the bucket prefix')  

@click.option('--default', '-d',
                is_flag=True,
                help='Default parameter and tag files')                               

@click.command()
def create():
    """
    Create a new stack
    """
    click.echo('create')