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

@click.option('--print-json',
                help='Print the whole response in JSON format',
                default=False,
                is_flag=True)

@click.option('--field', '-f',
                help='Field to be printed out',
                default = (const.STACK_NAME, const.STACK_STATUS),
                multiple=True,
                type=click.Choice(const.STACK_DETAIL_FILEDS, case_sensitive=False))

@click.command(name='describe')
def describe_stack(name, field, print_json):
    """
    Show information of stack
    """
    _describe_stack(name, field, print_json)

def _describe_stack(name, field, print_json):
    try:
        response = _session.cf.describe_stacks(StackName=name)
    except botocore.exceptions.ClientError:
        click.secho(const.ERM_INVALID, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_INVALID)
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
            try:
                col = str(response[i])
            except: 
                col = const.NULL
            row = row + const.DELIM + col
        click.echo(row)
    return row 
    