import sys

import click
import boto3
import botocore

from . import _session
from . import hanga_constants as const

@click.command(name='delete')
def delete_stack():
    """
    Delete a stack
    """    
    pass