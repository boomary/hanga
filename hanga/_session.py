
import boto3
import click

def _init_session(profile, region):
    session = boto3.Session(profile_name=profile,
                            region_name=region)

    global cf
    cf = session.client('cloudformation')

    global s3
    s3 = session.resource('s3')

