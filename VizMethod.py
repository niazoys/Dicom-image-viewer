import numpy as np 
from numpy import interp

class VizMethod():
    def __init__(self):
        self.dicomData=np.array(([1,2]))

    def naiveMethod(self,dataArray):
        '''Method 01  (Naive method)''' 

        dataArray=dataArray/256
        dataArray= interp(dataArray,[np.min(dataArray),np.max(dataArray)],[0,256])
        return dataArray
    
    def minMaxMethod(self,dataArray):
        '''method 02 (calculate min and max pixel values and rescale the pixel values to 0 to 255)'''
        maxval=np.max(dataArray)
        minval=np.min(dataArray)
        mappedVal= interp(dataArray,[minval,maxval],[0,255])
        return mappedVal

    def windowingMethod (self,dataArray,center,width):
        '''Method 03 " Clip the image according to center and width of viewing window'''
        upLim=center+width/2
        downLim=center-width/2
        result = np.array(np.clip(dataArray,downLim,upLim))
        rescaled=interp(result,[np.min(result),np.max(result)],[0,255])
        return rescaled