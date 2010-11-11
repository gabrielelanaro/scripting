"""
Defining bash commands for python developement

cp
mv
mkdir
rm
touch

sh
call
"""
import os,shutil,unittest

def basename(src):
    "Unix basename"
    if src[-1] == "/":
        src = src[:-1]
    return os.path.basename(src)

def cp(src,dst,recursive=False):
    """This is an enhanced version of the classic shell CP utility"""
    #print src,dst
    if not os.path.exists(src):
        raise Exception("Source File %s does not exists"%src)
    # Base call
    if os.path.isfile(src):
        #print "Copying ", src, "in", dst
        shutil.copy(src,dst)
 
    # Recursive call
    if os.path.isdir(src):
        if os.path.exists(dst):
            # Create a directory, inside
            # TODO: This should be done only for the first directory?
            dst=os.path.join(dst, basename(src))
        #print "Making directory", dst
        mkdir(dst)

        for f in os.listdir(src):
            cp(os.path.join(src,f), dst, recursive)

def mkdir(src,parent=False):
    if parent:
        os.makedirs(src)
    else:
        os.mkdir(src)

def rm(src,recursive=False):
    if os.path.isfile(src):
        os.remove(src)
    else:
        if recursive:
            shutil.rmtree(src)

def touch(src,times=None):
    with file(src, 'a'):
        os.utime(src,times)


