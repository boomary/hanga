import sys

import click
import boto3
import botocore

from . import _session
from . import hanga_constants as const


@click.option('--bucket', '-b',
                help='S3 bucket',
                required=True,
                type=str)

@click.option('--prefix', '-p',
                help='S3 bucket prefix',
                default='/',
                required=True,
                type=str)

@click.option('--file', '-f',
                help='File to be uploaded',
                required=True,
                type=str)

@click.command(name='upload')
def upload_object(bucket, prefix, file):
    """
    Upload a file to a bucket
    """
    _upload_object(bucket, prefix, file)
 

def _upload_object(bucket, prefix, file):
    if prefix == '/':
        prefix = '' 
    elif prefix.startswith('/'):
        prefix = prefix[1:]
    elif not prefix.endswith('/'):
        prefix = prefix + '/'
    object_key = prefix + file

    try:
        _session.s3.meta.client.upload_file(Filename=file, 
                                            Bucket=bucket, 
                                            Key=object_key)
    except FileNotFoundError:
        click.secho(const.ERM_FILE_NOTFOUND, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_FILE_NOTFOUND)   
    except boto3.exceptions.S3UploadFailedError:
        click.secho(const.ERM_S3_INVALID, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_S3_INVALID)  
    except:
        click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)     
