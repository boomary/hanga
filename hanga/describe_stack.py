__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"


import sys

import click
import boto3
import botocore

from . import _session
from . import hanga_constants as const
from . import hanga_util as util

@click.option('--name', '-n',
                required=True,
                help='Stack name')

@click.option('--print-json', '-p',
                help='Print the whole list in plain JSON format',
                default=False,
                is_flag=True)

@click.option('--field', '-f',
                help='Field to be printed out. You can print out one or more fields:\n'
                     'hanga list -f <field> -f <field> ...\n'
                     'By default, StackName, Description, StackStatus, CreateionTime, and EnableTerrminationProtection are printed out.',
                default = tuple([const.STACK_NAME, 
                            const.DESCRIPTION,
                            const.STACK_STATUS, 
                            const.CREATION_TIME,
                            const.ENABLE_TERMINATION_PROTECTION]),
                multiple=True,
                type=click.Choice(const.STACK_DETAIL_FILEDS, case_sensitive=False))

@click.command(name='describe')
def describe_stack(name, field, print_json):
    """
    Show information of stack
    """
    _describe_stack(name, field, print_json)

def _describe_stack(name, 
                    field = tuple([const.STACK_NAME, 
                            const.DESCRIPTION,
                            const.STACK_STATUS, 
                            const.CREATION_TIME,
                            const.ENABLE_TERMINATION_PROTECTION]), 
                    print_json = False):
    try:
        response = _session.cf.describe_stacks(StackName=name)
    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)
    except:
        click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)  

    if print_json:
        click.echo(response)
    else:
        response = response[const.STACKS][0]

        field = util.recaseTuple(field, const.STACK_DETAIL_FILEDS)
        iField = iter(field)
        row = response[next(iField)]

        for i in iField:
            value = response.get(i)
            col = str(value) if value else const.NULL
            row = row + const.DELIM + col
        click.echo(row)
    return row 
    