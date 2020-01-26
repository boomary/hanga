from . import hanga_constants as const

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
    if prefix.startswith('/'):
        prefix = prefix[1:]
    if not prefix.endswith('/'):
        prefix = prefix + '/'
    
    return prefix




