import glob
import os
import SimpleITK as sitk
import numpy as np
from sklearn import mixture

idir = "/media/brian/CCTS/PittVolumes"
sdir = "/media/brian/CCTS/LungSegmentation2"
odir = "/media/brian/CCTS/LungLabeling"

if not os.path.exists(odir):
    os.mkdir(odir)
@profile
def getNext(imgiter):
    while True:
        seg = imgiter.next()
        if os.path.exists(os.path.join(idir,os.path.basename(seg))):
            return seg
@profile
def getValues(seg):
    img = sitk.GetArrayFromImage(sitk.ReadImage(seg))
    inds = np.nonzero(img.flat)
    inds = np.nonzero(img.flat)[0]
    img = sitk.GetArrayFromImage(sitk.ReadImage(os.path.join("../PittVolumes",seg)))
    vals = img.flat[inds]
    return vals, inds, img.shape
@profile
def getMMImage(vals,inds,shape):
    gmm = mixture.GMM(n_components=3,covariance_type='full')
    gmm.fit(vals)
    labels = gmm.predict(vals)
    newimg = np.zeros(shape,dtype=np.uint8)
    newimg.flat[inds] = labels
    newimg.flat[inds] = labels+1
    return newimg
def main():
    files = glob.glob(os.path.join(sdir,"*.nii.gz"))
    imgiter = iter(files)
    seg = getNext(imgiter)
    vals,inds,shape = getValues(seg)
    newimg = getMMImage(vals,inds,shape)

    sitk.WriteImage(sitk.GetImageFromArray(newimg),os.path.join(odir,seg))

if __name__ == '__main__':
    main()
