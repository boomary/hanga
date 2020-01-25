
import boto3

def _init_session(profile):
    global cf
    session = boto3.Session(profile_name=profile)
    cf = session.client('cloudformation')
