"""Module to control the interaction with the shell Bash
"""
import subprocess
import os

def source(fname):
    """Emulate the source command in bash, reading the environment
    from a script.

    """
    cmdlist = ['source', fname, "&&", 'env']
    
    command = ['bash', '-c', subprocess.list2cmdline(cmdlist)]
    
    proc = subprocess.Popen(command, stdout = subprocess.PIPE)
    
    for line in proc.stdout:
        line = line.rstrip('\n') # Removing trailing newline
        (key, _, value) = line.partition("=")
        os.environ[key] = value
        print(key,value)

    proc.communicate()

