import re

def grep(pattern, filename):
    """Given a regex *pattern* return the lines in the file *filename*
    that contains the pattern.

    """
    return greplines(pattern, open(filename))
    
def greplines(pattern, lines):
    """Given a list of strings *lines* return the lines that match
    pattern.

    """
    res = []
    for line in lines:
        match = re.search(pattern, line)
        if match is not None:
            res.append(line)
    return res
    
    