"""
Shell-like commands for scripting development
"""
import fnmatch
import os, shutil
import shlex,subprocess,itertools,tarfile
from functools import wraps
import collections
import zipfile
from glob import glob # We can import that from other modules

def take_str_or_list(f):
    '''
    Allow the function decorated to take as the first argument a
    string or an iterable.
    
    If the first arg is a string, call *f* with the string as the
    first argument, if the first argument is an iterable, call f on
    each item of the iterable and return a list of the results.
    '''
    @wraps(f)
    def wrapper(*args,**kw):
        first = args[0]
        if isinstance(first, str):
            return f(*args,**kw)
        elif hasattr(first, "__iter__"):
            return [f(arg, *args[1:], **kw) for arg in first]
        else:
            raise Exception("First argument should be a string or a list")
    return wrapper

def basename(src):
    "Unix basename"
    if src[-1] == "/":
        src = src[:-1]
    return os.path.basename(src)

@take_str_or_list
def cp(src,dst):
    """
    Copy files and directories

    :param src: can be a string or an iterable and is the file/s to copy
    ;param dst: the destination file or directory
    """
    if not os.path.exists(src):
        raise Exception("Source File %s does not exists"%src)

    # Base call
    if os.path.isfile(src):
        shutil.copy(src,dst)
 
    # Recursive call
    if os.path.isdir(src):
        if os.path.exists(dst):
            # Create a directory, inside
            # TODO: This should be done only for the first directory?
            dst=os.path.join(dst, basename(src))
        mkdir(dst)

        for f in os.listdir(src):
            cp(os.path.join(src,f), dst)

def find(glob, startdir = "."):
    '''
    Return a list of files that matches glob

    :param glob: is the pattern to search for like *.py or *.py?
    :param startdir: the path from where to search
    '''
    for root, dirs, files in os.walk(startdir):
        for file_ in files:
            if fnmatch.fnmatch(file_,glob):
                yield os.path.join(root,file_)

@take_str_or_list
def mkdir(src,parent=False):
    '''
    Make a directory

    :param parent: if True, create all the directory structure
    '''

    if parent:
        os.makedirs(src)
    else:
        os.mkdir(src)


@take_str_or_list
def rm(src):
    '''
    Remove a file or a directory
    
    :param src: a string or an iterable, representing the file/s to remove
    '''
    if os.path.isfile(src):
        os.remove(src)
    else:
        shutil.rmtree(src)

@take_str_or_list
def touch(src,times=None):
    '''
    Create *src* file if it doesn't exists or update his modification
    time according to *times*.
    '''
    f = open(src, 'a')
    os.utime(src,times)
    f.close()

def sh_args(args):
    p = subprocess.Popen(args)
    p.wait()
    return p.returncode

def sh_cmdln(cmdl, args):
    p = subprocess.Popen(itertools.chain(shlex.split(cmdl), args))
    p.wait()
    return p.returncode

def archive(src, dst, format="tar"):
    '''
    Create an archive *dst* from the directory *src*. The format can
    be specified with the *format* parameter that can be:
    
    - tar
    - gzip
    - bz2
    - zip
    '''
    
    if format == "zip":
        arch = zipfile.ZipFile(dst,"w")
        for root,dirs,files in os.walk(src):
            for f in files:
                towrite = os.path.join(root, f)
                towritename = os.path.relpath(towrite,
                                               os.path.join(src,".."))
                arch.write(towrite, towritename)
        arch.close()
        return
    
    open_method = {"tar":"w",
                   "gzip":"w:gz",
                   "bz2":"w:bz2"}
    
    arch = tarfile.open(dst,open_method[format])
    arch.add(src,arcname=basename(src))
    arch.close()

def unpack(src, dst, format=None):
    """Unpack the archive *src* in the destination directory
    *dst*. The format can be *tar*, *gzip*, *bz2*, *zip* or *None* to
    auto-select the format based on the extension.

    """
    if not format:
        base, ext = os.path.splitext(src)
    else:
        ext = format

    ext2open_method = {".zip": "zip",
                       ".gz": "r:gz",
                       ".bz2": "r:bz2",
                       ".tar": "r:"}

    if ext2open_method[ext] == "zip":
        arch = zipfile.ZipFile(src,"r")
    else:
        arch = tarfile.open(src, ext2open_method[ext])

    arch.extractall(dst)
    arch.close()
