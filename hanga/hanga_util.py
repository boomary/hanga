from . import hanga_constants as const

def recaseTuple(torigin, ldesire):
    mLowerDesire = map(lambda x:x.lower(), ldesire)
    lLowerDesire = list(mLowerDesire)
    lorigin = list(torigin)
    for i in range(len(lorigin)):
        lorigin[i] = ldesire[lLowerDesire.index(lorigin[i].lower())]
    
    return tuple(lorigin)



