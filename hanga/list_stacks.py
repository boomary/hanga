import sys

import click
import boto3
import botocore

from . import _session
from . import hanga_constants as const
from . import hanga_util as util


@click.option('--field', '-f',
                help='Field to be printed out. You can one or more fields:\n'
                     'hanga list -f <field> -f <field> ...\n'
                     'Default: -f StackName -f StackStatus',
                default = (const.STACK_NAME, const.STACK_STATUS),
                multiple=True,
                type=click.Choice(const.STACK_SUMMARY_FILEDS, case_sensitive=False))
              

@click.option('--match-name', '--mn',
                help='List stacks based on a condition matching their name.\n'
                     'Default: -nm exactly *',
                default=(const.EXACTLY, const.ALL),          
                nargs=2, type=click.Tuple([click.Choice(const.STRING_MATCH_CONDITIONS, case_sensitive=False), str]))

@click.option('--match-status', '--ms',
                help='List stacks based on a condition matching their status',  
                default=const.STACK_STATUS_FILTERS_TUPLE,
                multiple=True,
                type=click.Choice(const.STACK_STATUS_FILTERS, case_sensitive=False))


@click.command(name='list')
def list_stacks(field, match_name, match_status):
    """
    List stacks
    """

    mn_cond, mn_value = match_name

    try:
        response = _session.cf.list_stacks()
    except botocore.exceptions.ClientError:
        click.secho(const.ERM_INVALID, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_INVALID)
    except:
        click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)  

    json = response[const.STACK_SUMMARIES]
    for response in json:

        stackStatus = str(response[const.STACK_STATUS])
        match_status = util.recaseTuple(match_status, const.STACK_STATUS_FILTERS)
        
        contOuterLoop = True
        for s in match_status:
            if s != stackStatus:
                continue
            else:
                contOuterLoop = False
                break
        
        if contOuterLoop:
            continue

        stackName = response[const.STACK_NAME]
        mn_cond = mn_cond.lower()
         
        if mn_cond == const.EXACTLY and mn_value == const.ALL:
            pass
        elif mn_cond == const.EXACTLY and mn_value != stackName:
            continue
        elif mn_cond == const.CONTAINS and mn_value not in stackName:
            continue
        elif mn_cond == const.STARTS_WITH and not stackName.startswith(mn_value):
            continue
        elif mn_cond == const.ENDS_WITH and not stackName.endswith(mn_value):
            continue  
        
        field = util.recaseTuple(field, const.STACK_SUMMARY_FILEDS)
        iField = iter(field)
        row = response[next(iField)]
        
        for i in iField:
            try:
                col = str(response[i])
            except: 
                col = const.NULL
            row = row + const.DELIM + col
        click.echo(row)