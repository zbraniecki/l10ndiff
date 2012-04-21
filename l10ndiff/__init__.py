import sys

from .entity import *

if sys.version >= '3':
    basestring = str
    string = str
else:
    string = unicode

def compare_nodes(*args):
    val_is_different = False
    e1 = args[0]
    vals = [e1.value]
    for node in args[1:]:
        if node is None:
            vals.append(None)
            val_is_different = True
        else:
            vals.append(node.value)
            if e1.value != node.value:
                val_is_different = True
    if val_is_different:
        return vals
    else:
        return []

def entity(*args):
    if len(args) < 2:
        raise TypeError('diff() must have at least two arguments.')
    ediff = compare_nodes(*args)
    return ediff
