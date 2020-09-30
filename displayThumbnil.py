import os
import numpy as np 
import matplotlib.pyplot as plt
import pydicom
import sys 
import argparse

def usage():
    print ("<program name.py> -d directory of the dicom folder | -h help")

def readDirectory(path):

    ''' This Method Reads the directory and returns a list of Dicom files'''
    imageSet = []

    #Read the the files ends with .dcm extension
    for filename in os.listdir(path):
        if filename.endswith('.dcm'):
            imgPath=os.path.join(path, filename)
            imageSet.append(pydicom.dcmread(imgPath))
    return imageSet

def displayThumbnils(imageSet):
    '''This method takes a List of dicom image and shows them in a thumbnil fashion'''

    # Define the grid size of the viewing 
    height=np.ceil(np.sqrt(len(imageSet))).astype(int)
    width=len(imageSet)/height +  1

    
    #Define the size each individule figure in the grid
    fig=plt.figure(figsize=(15,15))

    #Go through all the files and put them in the figure 
    for (idx,data) in enumerate(imageSet):
        fig.add_subplot(height,width,idx+1)
        plt.axis('off')
        plt.imshow(data.pixel_array , cmap=plt.cm.bone)
    plt.show()
    

if __name__ == "__main__":
    #path='C:\\Users\\Niaz\\OneDrive\\Study Materials\\UBx\\New folder\\CT2.55\\'
    parser=argparse.ArgumentParser()
    parser.add_argument("-d","--dir", help="Please Enter the Dicom Directory in following format <program name.py> -d directory \n" )
    
    # Read arguments from the command line
    args = parser.parse_args()

    if args.dir:
        dicomList=readDirectory(args.dir)
        displayThumbnils(dicomList)
    else:
        usage()
        sys.exit(2)
