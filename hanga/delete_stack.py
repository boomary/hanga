__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"

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