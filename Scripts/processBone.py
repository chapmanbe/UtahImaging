import os
import glob
import subprocess
import sqlite3
from IPython.parallel import Client
from IPython.parallel import require

ddir = "/media/brian/CCTS/PittVolumes"
outdir = "/media/brian/CCTS/BoneSegmentation"

@require(sqlite3,subprocess)
def runSkin(cmd):
    conn = sqlite3.connect(cmd[2])
    cursor = conn.cursor()
    rslt = subprocess.call("/home/brian/anaconda/bin/vtkpython -E /home/brian/bin/dicom2stl.py -t bone -o %s %s"%(cmd[1],cmd[0]),shell=True)
    cursor.execute("""INSERT INTO results(case_num,result) VALUES (?,?)""",(cmd[0],rslt))
    conn.commit()
    return cmd[0],rslt


def main():
    rc = Client()
    dview = rc[:]
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    dbname = os.path.join(outdir,"boneProcessingResults.sqlite")
    conn = sqlite3.connect(dbname)
    conn.execute("""CREATE TABLE IF NOT EXISTS results(case_num text, result text)""")
    conn.commit()
    files = glob.glob(os.path.join(ddir,"*.nii.gz"))
    cmds = [(f,os.path.join(outdir,os.path.basename(f))+".stl",dbname) for f in files]
    rslts = dview.map_async(runSkin,cmds).get()
    print rslts

if __name__ == '__main__':
    main()

