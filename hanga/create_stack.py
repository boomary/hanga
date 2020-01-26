import sys

import click
import boto3

from . import _session
from . import hanga_constants as const
from . import upload_object

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
                help='Upload to the bucket prefix',
                is_flag=True)  

@click.option('--default', '-d',
                is_flag=True,
                help='Default parameter and tag files')                               

@click.command(name='create')
def create_stack(name, template, bucket, params, tags, upload, default):
    """
    Create a new stack
    """

    pass
    # try:
    #     response = _session.s3.upload_object

    # except botocore.exceptions.ClientError:
    #     click.secho(const.ERM_STACK_NOTFOUND, bg=const.BG_ERROR, fg=const.FG_ERROR)
    #     sys.exit(const.ERC_STACK_NOTFOUND)