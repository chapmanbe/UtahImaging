
from IPython.parallel import Client

rc = Client()
dview = rc[:]

with dview.sync_imports():
    import SimpleITK as sitk
    import dicomUtils
    import glob
    import os
    import dicom


ddir = "/media/brian/MyData/HD1/Repository/Scrubbed/"
outdir = "/media/brian/CCTS/PittVolumes"
if not os.path.exists(outdir):
    os.mkdir(outdir)


# In[7]:
def convertDir(cmd):
    root = cmd[0]
    d = cmd[1]
    ddir = cmd[2]
    outdir = cmd[3]
    try:
        dfs = glob.glob(os.path.join(root,d,"*.dcm"))
        df = dicom.read_file(dfs[0],stop_before_pixels = True)
        if "BOTTOM" in df.SeriesDescription.upper():
            fname = os.path.join(root,d)
            tmp = fname.split(ddir)[1].replace(" ","")
            tmp = tmp.split(os.path.sep)
            #tmp = [t.replace(" ","") for t in tmp]
            outname = "__".join(tmp)+".nii.gz"
            print d,outname
            files = dicomUtils.getOrderedListOfFiles(fname)
            reader = sitk.ImageSeriesReader()
            reader.SetFileNames(files)
            #ct_img = reader.Execute()
            #sitk.WriteImage(ct_img, os.path.join(outdir,outname))
            return outname
        else:
            return ""
    except Exception, error:
        return error
rslts = {}
for root, dirs, files in os.walk(ddir):
    cmds = [(root,d,ddir,outdir) for d in dirs]
    try:
        rslts[d] =  dview.map_async(convertDir,cmds).get()
    except:
        pass

keys = rslts.keys()
keys.sort()
for k in keys:
    print k,rslts[k]
# In[ ]:



