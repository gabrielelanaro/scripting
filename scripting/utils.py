"""Functions of generic utility
"""

def partition(alist, indices):
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]