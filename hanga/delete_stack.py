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
        deleteAction = False
        _describe_stack(name=name)  # Check if the stack exists     
        click.secho('WARNING: Resources of the stack will be deleted and unrecoverable if they are unprotected with RETAIN.', fg=const.FG_WARN)
        isYes = util.query_yes_no('Do you really want to delete this stack?', 'no')
        if not isYes:
            click.secho('You have aborted this change set.', fg=const.FG_INF) 
            sys.exit(0)
        
        _session.cf.delete_stack(StackName=name)
        deleteAction = True
        eResponse = _wait_for_done_deletion(name)
        if eResponse != const.DELETE_COMPLETE:
            click.secho('The stack was unsuccessfully deleted with this status: %s!' % eResponse, fg=const.FG_ERROR)
    except botocore.exceptions.ClientError as error:
        if deleteAction and str(error.response['Error']['Code']) == 'ValidationError' and str(error.response['Error']['Message']).endswith('does not exist'):
            click.secho('The stack has been deleted!', fg=const.FG_INF)  
        else:
            util.handleClientError(error)

def _wait_for_done_deletion(name):  
    click.secho('Please wait while the stack is being deleted...', fg=const.FG_INF)

    eResponse = const.DELETE_IN_PROGRESS
    response = None   
    running_time = 0
    anim_index = 0
    
    while eResponse == const.DELETE_IN_PROGRESS:

        print(const.ANIM_STRING[anim_index % const.ANIM_LEN], end="\r")   
        
        if running_time % const.DELAY_TIME_FOR_DESCRIBE_CHANGE_SET == 0.0:
            response = _session.cf.describe_stacks(StackName=name) 
            response = response[const.STACKS][0]
            eResponse = response[const.STACK_STATUS]
   
        anim_index += 1
        time.sleep(const.DELAY_TIME_FOR_ANIMATION)
        running_time += const.DELAY_TIME_FOR_ANIMATION

    return eResponse

