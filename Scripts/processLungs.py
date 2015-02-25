import os
import glob
import sitkfuncs
import SimpleITK as sitk
from IPython.parallel import Client
from IPython.parallel import require
import sqlite3 

rc = Client()
rc.ids
dview = rc[:]

ddir = "/media/brian/CCTS/PittVolumes"
outdir = "/media/brian/CCTS/LungSegmentation2"
sdir = "/media/brian/CCTS/brian/Dropbox/UofU/ImagePhenotyping/Scripts"
if not os.path.exists(outdir):
    os.mkdir(outdir)

@require(sitk,glob,'dicom',os,sqlite3,sitkfuncs)
def callLungExtractor(cmd):
    conn = sqlite3.connect(cmd[2])
    cursor = conn.cursor()
    try:
        sitkfuncs.naive_lung_extractor(cmd[0],cmd[1])
        cursor.execute("""INSERT INTO results(case_num,result) VALUES (?,?)""",(cmd[0],"Success",))
        conn.commit()
        msg = "Success"
    except Exception, error:
        cursor.execute("""INSERT INTO results(case_num,result) VALUES (?,?)""",(cmd[0],str(error),))
        msg = str(error)
    conn.commit()
    return cmd[0],cmd[1],msg




def main():
    files = glob.glob(os.path.join(ddir,"__RV*.nii.gz"))
    dbname = "lungProcessingResults.sqlite"
    conn = sqlite3.connect(dbname)
    conn.execute("""CREATE TABLE IF NOT EXISTS results(case_num txt, result txt)""")
    conn.commit()
    
    #startloc = files.index(os.path.join(ddir,"PE000629__Exam_24110__Ser_000004.nii.gz"))
    startloc = 0
    cmds = [(f,os.path.join(outdir,os.path.basename(f)),os.path.join(sdir,dbname)) for f in files[startloc:]]
    rslts = dview.map_async(callLungExtractor,cmds).get()
    #rslts = map(callLungExtractor,cmds)
    print rslts

if __name__ == '__main__':
    main()


