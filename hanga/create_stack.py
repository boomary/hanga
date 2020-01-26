__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"

import sys
import os

import click
import boto3
import botocore

from . import _session
from . import hanga_constants as const
from . import hanga_util as util
from . import upload_object

@click.option('--name', '-n',
                required=True,
                type=click.STRING,
                help='Stack name')

@click.option('--template', '-t',
                help='Stack template',
                required=True,
                type=click.STRING)

@click.option('--bucket', '-b',
                help='S3 bucket',
                required=True)

@click.option('--object-prefix', '-o',
                help='S3 object prefix (i.e., directory)',
                default='')

@click.option('--params', '--parameters',
                help='Parameter file',
                default=None)

@click.option('--tags',
                help='Tag file',
                default=None)               

@click.option('--upload', '-u',
                help='Upload to the bucket prefix',
                default=False,
                is_flag=True)  

@click.option('--default', '-d',
                help='Default parameter and tag files',
                default=False,
                is_flag=True)                               

@click.command(name='create')
def create_stack(name, template, bucket, object_prefix, params, tags, upload, default):
    """
    Create a new stack
    """
    object_prefix = util.reformS3Prefix(object_prefix)
    try:
        with open(template, 'r') as fTemplate:
            object_key = object_prefix + os.path.basename(fTemplate.name)
    except FileNotFoundError:
        util.handleFileNotFound(template)

    if params is not None:
        paramList = util.getJsonDataFromFile(params)
        click.secho('Use the parameter file', fg=const.FG_INF)
    else:
        paramList = list()
         
    if tags is not None:
        tagList = util.getJsonDataFromFile(tags)
        click.secho('Use the tag file', fg=const.FG_INF) 
    else:
        tagList = list()           

    if (upload):
        click.secho('The template is being uploaded to the bucket.', fg=const.FG_INF)
        upload_object._upload_object(bucket, object_key, os.path.abspath(template))
        click.secho('Upload done...', fg=const.FG_INF)
    
    templateUrl = 'https://' + bucket + '.s3.amazonaws.com/' + object_key
    try:
        response = _session.cf.create_stack(StackName=name,
                                            TemplateURL=templateUrl,
                                            Parameters=paramList,
                                            Tags=tagList)
    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)
    except:
        click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)  
    
    stackId = response[const.STACK_ID]
    click.secho('\nThe following stack is being created:', fg=const.FG_INF)
    click.echo(stackId)
