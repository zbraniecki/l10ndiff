from collections import OrderedDict
from .entity import entities

def intersect(*args):
    r = set(args[0])
    for arg in args[1:]:
        r &= set(arg)
    return [x for x in args[0] if x in r]

def getpos(keylist, key):
    ret = {'before': None, 'after': None}
    pos = keylist.index(key)
    if pos > 0:
        ret['after'] = keylist[pos-1]
    if pos < len(keylist)-1:
        ret['before'] = keylist[pos+1]
    return ret

def diff_lists(*lists, **kval):
    values = kval.get('values', True)
    keys = intersect(*[l.keys() for l in lists])
    ldiff = EntityListDiff()
    for key in keys:
        ediff = entities(*[l[key] for l in lists], values=values)
        if ediff:
            kdiff = {'elem': ediff,
                     'flags': set(('present',)),
                     'pos': None}
            ldiff[key] = kdiff
    for i,l in enumerate(lists):
        for k in l.keys():
            if k not in keys:
                kdiff = ldiff.get(k, [])
                if not kdiff:
                    kdiff = {'elem': [None]*len(lists),
                             'flags': set(),
                             'pos': None}
                for i2, l2 in enumerate(lists):
                    if k in l2:
                        kdiff['elem'][i2] = l2[k]
                kdiff['flags'].add('added')
                kdiff['pos'] = getpos(list(l.keys()), k)
                ldiff[k] = kdiff
    return ldiff

class EntityListDiff(OrderedDict):
    def __init__(self, id=None):
        self.id = id
        super(EntityListDiff, self).__init__(self)

    # pos - may be a number or a tuple ('after','id') or ('before','id')
    def add(self, flag, ediff, id, pos=None):
        self[id] = {'elem': ediff, 'flags': [flag], 'pos': pos}


def lists(*lists, **kwalues):
    values = kwalues.get('values', True)
    eldiff = diff_lists(*lists, values=values)
    return eldiff
    
