__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"

import sys
import os
import random
import time

import click
import boto3
import botocore

from . import _session
from . import hanga_constants as const
from . import hanga_util as util
from .describe_stack import _describe_stack

@click.option('--name', '-n',
                required=True,
                type=click.STRING,
                help='Stack name')

@click.command(name='delete')
def delete_stack(name):
    """
    Delete a stack
    """    
    try:
        _describe_stack(name=name)  # Check if the stack exists     
        click.secho('WARNING: Resources of the stack will be deleted and unrecoverable if they are unprotected with RETAIN.', fg=const.FG_WARN)
        isYes = util.query_yes_no('Do you really want to delete this stack?', 'no')
        if not isYes:
            click.secho('You have aborted this change set.', fg=const.FG_INF) 
            sys.exit(0)
        
        _session.cf.delete_stack(StackName=name)
        click.secho('The stack has been deleted!', fg=const.FG_INF)                                                     
    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)