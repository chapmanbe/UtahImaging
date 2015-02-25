import SimpleITK as sitk
import glob
import os
import sys

files = glob.glob(os.path.join(sys.argv[1],"*.dcm"))

reader = sitk.
