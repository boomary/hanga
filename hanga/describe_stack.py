import sys

import click
import boto3
import botocore

from . import _session
from . import hanga_constants as const


@click.option('--stack-name', '-n',
                required=True,
                help='Stack name')

@click.option('--print-json',
                is_flag=True,
                help='Print the whole response in JSON format')

@click.option('--print', '-p',
                help='Field to be printed out',
                multiple=True,
                type=click.Choice(const.STACK_DETAIL_FILEDS, case_sensitive=True))

@click.command(name='describe')
def describe_stack(stack_name, print, print_json):
    """
    Show information of stack
    """

    try:
        response = _session.cf.describe_stacks(StackName=stack_name)
    except botocore.exceptions.ClientError:
        click.secho(const.ERM_STACK_NOTFOUND, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_STACK_NOTFOUND)
    # except:
    #     click.secho(const.ERM_PROFILE_INVALID, bg=const.BG_ERROR, fg=const.FG_ERROR)
    #     sys.exit(const.ERC_PROFILE_INVALID)

    if print_json:
        click.echo(response)
    else:
        response = response[const.STACKS][0]
        row = str(response[const.STACK_NAME])
        for p in print:
            try:
                row = row + const.DELIM + str(response[p])
            except:
                row = row + const.DELIM + const.NULL
        click.echo(row)

 
    