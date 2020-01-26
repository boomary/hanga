import sys

import click
import boto3
import botocore

from . import _session
from . import hanga_constants as const
from . import hanga_util as util


@click.option('--field', '-f',
                help='Field to be printed out. You can print out one or more fields:\n'
                     'hanga list -f <field> -f <field> ...\n'
                     'By default, StackName and StackStatus are printed out.',
                default = tuple([const.STACK_NAME, const.STACK_STATUS]),
                multiple=True,
                type=click.Choice(const.STACK_SUMMARY_FILEDS, case_sensitive=False))
              

@click.option('--match-name', '--mn',
                help='Search stacks based on a condition matching their name.\n'
                     'By default, all stack names are searched',
                default=tuple([const.EXACTLY, const.ALL]),          
                nargs=2, type=click.Tuple([click.Choice(const.STRING_MATCH_CONDITIONS, case_sensitive=False), str]))

@click.option('--match-status', '--ms',
                help='Search stacks based on a condition matching their status type\n'
                     'You can search one or more status types can be listed\n:'
                     'hanga list -ms <type> --ms <type> ...\n'
                     'By default, all status types except DELETE_COMPLETE are searched.',  
                default=tuple(const.STACK_STATUS_FILTERS_NO_DELETE_COMPLETE),
                multiple=True,
                type=click.Choice(const.STACK_STATUS_FILTERS, case_sensitive=False))


@click.command(name='list')
def list_stacks(field, match_name, match_status):
    """
    List stacks
    """
    _list_stacks(field, match_name, match_status)


def _list_stacks(field, match_name, match_status):
    mn_cond, mn_value = match_name

    try:
        response = _session.cf.list_stacks()
    except botocore.exceptions.ClientError:
        click.secho(const.ERM_INVALID, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_INVALID)
    except:
        click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)  

    count_results = 0
    json = response[const.STACK_SUMMARIES]
    for response in json:

        stackStatus = str(response[const.STACK_STATUS])
        match_status = util.uppercaseTuple(match_status)
        
        contOuterLoop = True
        for s in match_status:
            if stackStatus != s:
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
        count_results = count_results + 1
    
    click.secho('\nTotal number of stacks found:', fg=const.FG_INF)
    click.echo(count_results)