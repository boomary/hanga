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

def deploy_stack(name, template, bucket, object_prefix, params, tags, upload, iam, named_iam, auto_expand, default, isUpdated):
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
        cName = name + str(random.randint(100000,999999)) # change set name
        cType = 'UPDATE' if isUpdated else 'CREATE'

        response = _session.cf.create_change_set(StackName=name,
                                            TemplateURL=templateUrl,
                                            Parameters=paramList,
                                            ChangeSetName=cName,
                                            ChangeSetType=cType,
                                            Tags=tagList)
        csId = response[const.CHANGESET_ID]
        stackId = response[const.STACK_ID]
        click.secho('\nThe following change set (ARN - name) is being created:', fg=const.FG_INF)                                                
        click.echo('%s - %s' % (csId, cName))                                                     
        click.secho('and deployed to the stack:', fg=const.FG_INF)
        click.echo(stackId)  

        response = _wait_for_done_changeset(name, cName)
        click.echo(response)
        
        # TODO: Change set results to be shown for confirmation
        
        isYes = util.query_yes_no('\nDo you want to execute this change set?', 'no')
        if not isYes:
            _session.cf.delete_stack(StackName=name)
            click.secho('You have aborted this change set.', fg=const.FG_INF) 
            sys.exit(0)

        response = _session.cf.execute_change_set(StackName=name,
                                            ChangeSetName=cName)  
        click.secho('The change set is being deployed.', fg=const.FG_INF)                                                     
    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)
    # except:
    #     click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
    #     sys.exit(const.ERC_OTHERS)  


# def _describe_change_set(StackName=name, ChangeSetName=cName):
#     # NextToken to be included
#     response = session.cf.client.describe_change_set(StackName=name,
#                                         ChangeSetName=cName)
#     return response

def _wait_for_done_changeset(name, cName):   
    click.secho('Please wait while the change set is being created...', fg=const.FG_INF)

    eResponse = ''
    response = None   
    running_time = 0
    anim_index = 0
    
    while eResponse not in [const.CS_CREATE_COMPLETE, const.CS_FAILED]:
        print(const.ANIM_STRING[anim_index % const.ANIM_LEN], end="\r")   
        if running_time % const.DELAY_TIME_FOR_DESCRIBE_CHANGE_SET == 0:
            response = _session.cf.describe_change_set(StackName=name,
                                        ChangeSetName=cName) 
   
        eResponse = response[const.CS_STATUS]
        anim_index += 1
        time.sleep(const.DELAY_TIME_FOR_ANIMATION)
        running_time += const.DELAY_TIME_FOR_ANIMATION

    click.secho('The change set is ready!', fg=const.FG_INF)

    return response