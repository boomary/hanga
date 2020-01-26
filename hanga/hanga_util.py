import sys
import json

import click

from . import hanga_constants as const
from botocore.exceptions import ClientError

def recaseTuple(torigin, ldesire):
    mUpperDesire = map(lambda x:x.upper(), ldesire)
    lUpperDesire = list(mUpperDesire)
    lorigin = list(torigin)
    for i in range(len(lorigin)):
        lorigin[i] = ldesire[lUpperDesire.index(lorigin[i].upper())]
    
    return tuple(lorigin)

def uppercaseTuple(torigin):
    mUpperOrigin = map(lambda x:x.upper(), torigin)
    return tuple(mUpperOrigin)

def reformS3Prefix(prefix):
    if prefix == '/':
        prefix = ''
    
    if prefix.startswith('/'):
        prefix = prefix[1:]
    
    if not prefix.endswith('/') and prefix != '':
        prefix = prefix + '/'
    
    return prefix


def getJsonDataFromFile(sJson):
    try:
        with open(sJson, 'r') as fJson:
            text = fJson.read()
            jsonData = json.loads(text)  
    except FileNotFoundError:
        handleFileNotFound(sJson)
    except json.decoder.JSONDecodeError: 
        click.secho(const.ERM_JSON_INVALID, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_FILE_NOTFOUND)    
    return jsonData                 

def handleFileNotFound(file):
        click.secho('%s: %s' % (const.ERM_FILE_NOTFOUND, file), bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_FILE_NOTFOUND)    

def handleClientError(error):
    click.secho('%s: %s' % (error.response['Error']['Code'], 
                            error.response['Error']['Message']), 
                            bg=const.BG_ERROR, fg=const.FG_ERROR)
    sys.exit(100)



