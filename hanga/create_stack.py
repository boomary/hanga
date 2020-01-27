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
                help='S3 object prefix (i.e., directory)\n'
                        'By default, the prefix is empty (i.e., root the bucket).',
                default='')

@click.option('--params', '--parameters', 
                help='Parameter file',
                default=None)

@click.option('--tags',
                help='Tag file',
                default=None)               

@click.option('--upload', '-u',
                help='Upload the template file to the bucket prefix',
                default=False,
                is_flag=True)  

@click.option('--iam',
                help='Enable CAPABILITY_IAM',
                default=False,
                is_flag=True)  

@click.option('--named-iam',
                help='Enable CAPABILITY_NAMED_IAM',               
                default=False,
                is_flag=True)  

@click.option('--auto-expand',
                help='Enable CAPABILITY_AUTO_EXPAND',
                default=False,
                is_flag=True)  

@click.option('--default', '-f',
                help='Default files to be deployed, that is,\n'
                     '  {stack name}.yaml - Template file\n'
                     '  {stack name}-params.yaml - parameter file\n'
                     '  {stack name}-tags.yaml - tag file.\n',
                default=False,
                is_flag=True)                               

@click.command(name='create')
def create_stack(name, template, bucket, object_prefix, params, tags, upload, iam, named_iam, auto_expand, default):
    """
    Create a new stack
    """
    _create_stack(name, template, bucket, object_prefix, params, tags, upload, iam, named_iam, auto_expand, default, False)    

def _create_stack(name, template, bucket, object_prefix, params, tags, upload, iam, named_iam, auto_expand, default, isDryRun):
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
        if (isDryRun):
            cName = name + str(random.randint(100000,999999)) # change set name
            response = _session.cf.create_change_set(StackName=name,
                                                TemplateURL=templateUrl,
                                                Parameters=paramList,
                                                ChangeSetName=cName,
                                                Tags=tagList)
            csId = response[const.CHANGESET_ID]
            stackId = response[const.STACK_ID]
            click.secho('\nThe following change set (ARN - name) is being created:', fg=const.FG_INF)                                                
            click.echo('%s - %s' % (csId, cName))                                                     
            click.secho('and deployed to the stack:', fg=const.FG_INF)
            click.echo(stackId)  

            # Confirm prompt to be added
            # And change set to be monitored until it is ready
            time.sleep(15)
            response = _session.cf.execute_change_set(StackName=name,
                                                ChangeSetName=cName)  
            click.secho('The change set is being deployed.', fg=const.FG_INF)                                                
                                                                                                         
        else:
            response = _session.cf.create_stack(StackName=name,
                                                TemplateURL=templateUrl,
                                                Parameters=paramList,
                                                Tags=tagList)
            stackId = response[const.STACK_ID]
            click.secho('\nThe following new stack is being updated:', fg=const.FG_INF)
            click.echo(stackId)                                                     
    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)
    except:
        click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)  
    
   
       


