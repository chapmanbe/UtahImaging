

    import pydas
    from wrapPydas import wrapPydas as wp
    import SimpleITK as sitk
    import matplotlib.pyplot as pp


    
    pcd = wp.wrapPydas("brian.chapman@utah.edu",token=u"gxwYbPVlgriFO4B6JPeIHPLEU4Bg2lN9I9XKOIVV",url="http://155.100.62.165/midas")
    fname = pcd.getFileName("PittCTPA","Private/TestData","pe0017s4.mha")
    img = sitk.ReadImage(str(fname))

## Now generate derived data doing some simple manipulations in SimpleITK


    mipz = sitk.MaximumProjection(img,2)
    mipy = sitk.MaximumProjection(img,1)
    mipx = sitk.MaximumProjection(img,0)
    sitk.WriteImage(mipz,"/tmp/pe0017s4_zmip.nii.gz")
    sitk.WriteImage(mipy,"/tmp/pe0017s4_ymip.nii.gz")
    sitk.WriteImage(mipx,"/tmp/pe0017s4_xmip.nii.gz")


    itemz = pcd.findItemInPath(pcd.community_id,pcd.folders[:],"pe0017s4_zmip.nii.gz")
    itemy = pcd.findItemInPath(pcd.community_id,pcd.folders[:],"pe0017s4_ymip.nii.gz")
    itemx = pcd.findItemInPath(pcd.community_id,pcd.folders[:],"pe0017s4_xmip.nii.gz")
    print itemz,itemy,itemx

    {'item_id': u'60', 'folder_id': u'6'} {'item_id': u'61', 'folder_id': u'6'} {'item_id': u'62', 'folder_id': u'6'}



    if( itemz ):
        print "deleting itemz"
        pcd.driver.delete_item(pcd.token,itemz['item_id'])
        
    if( itemy ):
        print "deleting itemy"
        pcd.driver.delete_item(pcd.token,itemy['item_id'])
        
    if( itemx ):
        print "deleting itemx"
        pcd.driver.delete_item(pcd.token,itemx['item_id'])

    deleting itemz
    deleting itemy
    deleting itemx


## Now Upload derived files


    print pcd.item
    print pcd.community_id

    {'item_id': u'1', 'folder_id': u'6'}
    4



    pcd.uploadDerivedFile(src="/tmp/pe0017s4_zmip.nii.gz",dest="pe0017s4_zmip.nii.gz",description="This is a zmip generated from pe0017s4.mha",
                          metadatapairs=[("Processing Algorithm","SimpleITK"),("Direction",2)],
                          privacy="Public")
    pcd.uploadDerivedFile(src="/tmp/pe0017s4_ymip.nii.gz",dest="pe0017s4_ymip.nii.gz",description="This is a ymip generated from pe0017s4.mha",
                          metadatapairs=[("Processing Algorithm","SimpleITK"),("Direction",1)],
                          privacy="Public")
    pcd.uploadDerivedFile(src="/tmp/pe0017s4_xmip.nii.gz",dest="pe0017s4_xmip.nii.gz",description="This is a xmip generated from pe0017s4.mha",
                          metadatapairs=[("Processing Algorithm","SimpleITK"),("Direction",0)],
                          privacy="Public")



    print mipz.GetSize(),mipy.GetSize(),mipx.GetSize()
    amipz = sitk.GetArrayFromImage(mipz)
    amipy = sitk.GetArrayFromImage(mipy)
    amipx = sitk.GetArrayFromImage(mipx)
    pp.gray()
    pp.figure(0)
    pp.imshow(amipz[0,:,:])
    pp.figure(1)
    pp.imshow(amipy[:,0,:])
    pp.figure(2)
    pp.imshow(amipx[:,:,0])
    pp.gray()
    pp.show()

    (512, 512, 1) (512, 1, 382) (1, 512, 382)



![png](wrapPydasNotebook_files/wrapPydasNotebook_9_1.png)



![png](wrapPydasNotebook_files/wrapPydasNotebook_9_2.png)



![png](wrapPydasNotebook_files/wrapPydasNotebook_9_3.png)



    


    fnamez = pcd.getFileName("PittCTPA","Private/TestData","pe0017s4_zmip.nii.gz")
    fnamey = pcd.getFileName("PittCTPA","Private/TestData","pe0017s4_ymip.nii.gz")
    fnamex = pcd.getFileName("PittCTPA","Private/TestData","pe0017s4_xmip.nii.gz")



    mipz = sitk.ReadImage(str(fnamez))
    mipy = sitk.ReadImage(str(fnamey))
    mipx = sitk.ReadImage(str(fnamex))
    
    amipz = sitk.GetArrayFromImage(mipz)
    amipy = sitk.GetArrayFromImage(mipy)
    amipx = sitk.GetArrayFromImage(mipx)
    
    pp.figure(0)
    pp.imshow(amipz[0,:,:])
    pp.figure(1)
    pp.imshow(amipy[:,0,:])
    pp.figure(2)
    pp.imshow(amipx[:,:,0])
    pp.gray()
    pp.show()


![png](wrapPydasNotebook_files/wrapPydasNotebook_12_0.png)



![png](wrapPydasNotebook_files/wrapPydasNotebook_12_1.png)



![png](wrapPydasNotebook_files/wrapPydasNotebook_12_2.png)



    import shutil
    shutil.rmtree(pcd.writeRoot)



    import os
    print os.path.exists(pcd.writeRoot)

    True



    os.mkdir(pcd.writeRoot)


    
