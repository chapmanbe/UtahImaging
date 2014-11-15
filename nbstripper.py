#Modified from
# http://stackoverflow.com/questions/18734739/using-ipython-notebooks-under-version-control

from IPython.nbformat import current
import io
from os import remove, rename
from shutil import copyfile
from subprocess import Popen
from sys import argv
import argparse

parser = argparse.ArgumentParser(description="strip output from IPython notebook and add stripped version to git")
parser.add_argument('--message', '-m',help="message for the git commit",default="undocumented change")
parser.add_argument('files',metavar="files",nargs="+", help="list of notebooks to be committed")

args = parser.parse_args()

for filename in args.files:
    # Backup the current file
    backup_filename = filename + ".backup"
    copyfile(filename,backup_filename)

    try:
        # Read in the notebook
        with io.open(filename,'r',encoding='utf-8') as f:
            notebook = current.reads(f.read(),format="ipynb")

        # Strip out all of the output and prompt_number sections
        for worksheet in notebook["worksheets"]:
            for cell in worksheet["cells"]:
               cell.outputs = []
               if "prompt_number" in cell:
                    del cell["prompt_number"]

        # Write the stripped file
        with io.open(filename, 'w', encoding='utf-8') as f:
            current.write(notebook,f,format='ipynb')

        # Run git add to stage the non-output changes
        print("git add",filename)
        Popen(["git","add",filename]).wait()

    finally:
        # Restore the original file;  remove is needed in case
        # we are running in windows.
        remove(filename)
        rename(backup_filename,filename)
        Popen(["git","commit","-m",args.message]).wait()
