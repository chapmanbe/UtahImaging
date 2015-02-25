import dicom
import glob
import os

def getOrderedListOfFiles(d,suffix="*.dcm"):
    """d: directory name containing dicom images
    suffix: expected suffix for files"""
    files = glob.glob(os.path.join(d,suffix))

    files = [(dicom.read_file(f,stop_before_pixels=True).InstanceNumber,f) for f in files]
    files.sort(key= lambda s: s[0])
    instance,files = zip(*files)
    return files



