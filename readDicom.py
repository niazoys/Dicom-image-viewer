import os
import pydicom

class readDicom():

    def readFile(self,path):
        #Read the dicom file
        if path:
            img=pydicom.dcmread((path))
        return img
    
    # def displayImage(self,img):
    #     #plot the image 
    #     fig, ax = plt.subplots()
    #     vizMethod=VizMethod()
    #     data=vizMethod.naiveMethod(img.pixel_array)
    #     im=ax.imshow(data,cmap=plt.cm.bone, aspect='auto',vmin=0,vmax=255)
    #     return fig,im
    