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

@click.option('--field', '-f',
                help='Field to be printed out. You can print out one or more fields:\n'
                     'hanga dresources -f <field> -f <field> ...\n'
                     'By default, ResourceType, LogicalResourceId, ResourceStatus, and Timestamp are printed out.',
                default = const.DEFAULT_RESOURCE_FIELDS,
                multiple=True,
                type=click.Choice(const.STACK_RESOURCE_SUMMARY_FILEDS, case_sensitive=False))

@click.option('--max-items', '-m',
                help='Maximum number of resources to be returned (default: 100)\n',
                default = 100,
                type=int)

@click.command(name='lresources')
def list_resources(name, field, max_items):
    """
    List resources of a stack
    """
    _list_resources(name, field, max_items)

def _list_resources(name, field, max_items):
     count_results = 0
     nextToken = None
 
     while True and count_results < max_items:
          try:
               if nextToken is None:
                    response = _session.cf.list_stack_resources(StackName=name)
               else:
                    response = _session.cf.list_stack_resources(StackName=name, NextToken=nextToken)   
          except botocore.exceptions.ClientError as error:
               util.handleClientError(error)   
          # except:
          #     click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
          #     sys.exit(const.ERC_OTHERS)  
          
          field = util.recaseTuple(field, const.STACK_RESOURCE_SUMMARY_FILEDS)
          
          json = response[const.STACK_RESOURCE_SUMMARIES]

          for resource in json:
               if count_results >= max_items:
                    break

               iField = iter(field)
               row = resource[next(iField)]

               for i in iField:
                    value = resource.get(i)
                    col = str(value) if value else const.NULL
                    row = row + const.DELIM + col 
               count_results += 1
               click.echo(row)

          nextToken = response.get(const.NEXT_TOKEN)
          if nextToken is None:
               break
     
     click.secho('\nTotal number of reources returned:', fg=const.FG_INF)
     click.echo(count_results)