import sys

import click

from . import _session
from . import hanga_constants as const


# @click.option('--nameFilterType', '-f',
#               help='List stack name containing the given TEXT')

# @click.option('--name',
#               help='List stack name containing the given TEXT')


@click.option('--print', '-p',
                help='Field to be printed out',
                multiple=True,
                type=click.Choice(const.STACK_SUMMARY_FILEDS, case_sensitive=True))
              

@click.option('--name-match', '--nm',
                help='List stacks based on a condition matching their name',  
                default=(const.EXACTLY, const.ALL),          
                nargs=2, type=click.Tuple([click.Choice(const.STRING_MATCH_CONDITIONS, case_sensitive=True), str]))

@click.option('--status-match', '--sm',
                help='List stacks based on a condition matching their status',  
                default=const.STACK_STATUS_FILTERS_TUPLE,
                multiple=True,
                type=click.Choice(const.STACK_STATUS_FILTERS, case_sensitive=True))


@click.command(name='list')
def list_stacks(print, name_match, status_match):
    """
    List stacks
    """

    name_match_cond, name_match_value = name_match

    try:
        response = _session.cf.list_stacks()
    except:
        click.secho(const.ERM_PROFILE_INVALID, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_PROFILE_INVALID)

    for response in response[const.STACK_SUMMARIES]:

        stackStatus = str(response[const.STACK_STATUS])

        contOuterLoop = True
        for s in status_match:
            if s != stackStatus:
                continue
            else:
                contOuterLoop = False
                break
        
        if contOuterLoop:
            continue

        stackName = str(response[const.STACK_NAME])

        if name_match_cond == const.EXACTLY and name_match_value == const.ALL:
            pass
        elif name_match_cond == const.EXACTLY and name_match_value != stackName:
            continue
        elif name_match_cond == const.CONTAINS and name_match_value not in stackName:
            continue
        elif name_match_cond == const.STARTS_WITH and not stackName.startswith(name_match_value):
            continue
        elif name_match_cond == const.ENDS_WITH and not stackName.endswith(name_match_value):
            continue  

        row = stackName
        
        for p in print:
            try:
                row = row + const.DELIM + str(response[p])
            except:
                row = row + const.DELIM + const.NULL
        click.echo(row)