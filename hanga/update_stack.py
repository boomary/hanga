__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"

import click

from .deploy_stack import deploy_stack

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

@click.command(name='update')
def update_stack(name, template, bucket, object_prefix, params, tags, upload, iam, named_iam, auto_expand, default):
    """
    Create a change set for updating an existing stack and deploy it
    """
    deploy_stack(name, template, bucket, object_prefix, params, tags, upload, iam, named_iam, auto_expand, default, True)    