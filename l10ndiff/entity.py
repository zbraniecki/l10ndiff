import sys

if sys.version >= '3':
    basestring = str
    string = str
else:
    string = unicode

def intersect(*args):
    r = set(args[0])
    for arg in args[1:]:
        r &= set(arg)
    return list(r)

def equalseq(iterator):
    try:
        iterator = iter(iterator)
        first = next(iterator)
        return all(first == rest for rest in iterator)
    except StopIteration:
        return True

def equaltypeseq(iterator):
    try:
        iterator = iter(iterator)
        first = next(iterator)
        return all(type(first) == type(rest) for rest in iterator)
    except StopIteration:
        return True

class NodeDiff(dict):
    pass

class EntityDiff(NodeDiff):
    def __init__(self, id=None):
        self.id = id

def diff_values(*args):
    if isinstance(args[0], basestring):
        return args
    if isinstance(args[0], list):
        fdiff = []
        l = max([len(i) for i in args])
        for i in range(0, l):
            vals = [j[i] for j in args]
            if not equalseq(vals):
                fdiff.append(vals)
            else:
                fdiff.append(None)
        return fdiff
    if isinstance(args[0], dict):
        keys = intersect(*[i.keys() for i in args])
        fdiff = {}
        for key in keys:
            fdiff[key] = diff_values(*[i[key] for i in args])
        return fdiff
    if hasattr(args[0], '_fields'):
        return diff_nodes(*args)
    return args

def diff_nodes(*args):
    fields = []
    for node in args:
        fields.append(node._fields)
    fields = intersect(*fields)
    ndiff = NodeDiff()
    for field in fields:
        fdiff = []
        for node in args:
            if not hasattr(node, field):
                fdiff.append(None)
            else:
                fdiff.append(getattr(node, field))
        if equalseq(fdiff):
            pass
        else:
            print('---')
            print('nequal')
            print(field)
            print(hasattr(fdiff[0], '_fields'))
            print(type(fdiff[0]))
            print('====')
            if len(set(map(type, fdiff))) == 1:
                print('equal types')
                if hasattr(fdiff[0], '_fields'):
                    ndiff[field] = diff_nodes(*fdiff)
                else:
                    ndiff[field] = diff_values(*fdiff)
            else:
                print('different types')
                print(fdiff)
                ndiff[field] = fdiff
    return ndiff

def entities(*args):
    if len(args) < 2:
        raise TypeError('diff() must have at least two arguments.')
    ediff = diff_nodes(*args)
    return ediff

