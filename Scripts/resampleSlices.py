
import SimpleITK as sitk
import os
import glob
import sys

# In[6]:
sample = int(sys.argv[1])

dest_dir = "/media/brian/CCTS/DeepLearning/PAH_Measurement_Slice"

base = "Subsampled_%d"%sample
newDir = os.path.join(dest_dir,base)
if not os.path.exists(newDir):
    os.mkdir(newDir)

files = glob.glob(os.path.join(dest_dir,"*.dcm"))

for f in files:
    resample = sitk.ResampleImageFilter()
    img = sitk.ReadImage(f)
    inSp = img.GetSpacing()
    inSz = img.GetSize()
    outSp = [inSp[0]*sample,inSp[1]*sample,1]
    outSz = [inSz[0]/sample,inSz[1]/sample,1]
    resample.SetOutputDirection(img.GetDirection())
    resample.SetOutputOrigin(img.GetOrigin())
    resample.SetOutputSpacing(outSp)
    resample.SetSize(outSz)
    img2 = resample.Execute(img)
    bname = os.path.basename(f)
    sitk.WriteImage(img2,os.path.join(newDir,bname))
                            
