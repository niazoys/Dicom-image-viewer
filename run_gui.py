

import sys
import argparse
import numpy as np 
from numpy import  interp
from PIL import Image, ImageQt, ImageEnhance
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap,QIntValidator
from PyQt5.QtWidgets import QGridLayout, QMainWindow,QPushButton,QGroupBox,QWidget,QVBoxLayout,QApplication,QSlider,QLabel,QButtonGroup,QComboBox,QPushButton,QLineEdit


from readDicom import readDicom 
from VizMethod import VizMethod


class mainWindow(QWidget):
   def __init__(self,dicomData):
      super().__init__()
      
      # Set the Size and Title of the main window
      self.setWindowTitle("Dicom Viewer")
      
      self.y=200
      self.x=500
      self.width = 520
      self.height = 800
      self.setGeometry(self.x,self.y,self.width,self.height)
      #Create the necessary global variable 
      self.dicomFile=dicomData
      self.dicomData=np.array(dicomData.pixel_array)
      self.windowWidth=dicomData.WindowWidth
      self.windowCenter=dicomData.WindowCenter
      
      #Visualization  method object 
      self.vizMethod=VizMethod()

      #initialize the UI Components
      self.initializeUiComponents()
    
   def initializeUiComponents(self):
      '''Initializes the UI components for GUI'''
      #Create the layouts
      self.layout = QVBoxLayout()
      self.layout1 = QVBoxLayout()
      self.gridLayout = QGridLayout()

      #create the label for image
      self.imageCanvas=QLabel()
      self.imageCanvas.setMaximumHeight(self.dicomData.shape[0])
      self.imageCanvas.setMaximumWidth(self.dicomData.shape[1])
      self.imageCanvas.setAlignment(Qt.AlignCenter)
      self.showImage(np.uint8(self.vizMethod.naiveMethod(self.dicomData)))
      

      # Create  Labels 
      self.label1=QLabel("Contrast")
      self.label1.setAlignment(Qt.AlignCenter)
      self.label2=QLabel("Luminosity")
      self.label2.setAlignment(Qt.AlignCenter)
      self.labelW=QLabel("Width")
      self.labelC=QLabel("Center")
      WarningMessage3=QLabel("*** Calculation is different for Method 01 & 02.Visualization is Appreantly Same")
      WarningMessage3.setStyleSheet("background-color: red")    
 
      #Create Combo box
      self.chooseMethod = QComboBox()
      self.chooseMethod.addItem('Method 01 (Naive)')
      self.chooseMethod.addItem('Method 02 (MinMax)')
      self.chooseMethod.addItem('Method 03 (Windowing)')
      self.chooseMethod.activated[str].connect(self.changeVizMethod)
      
      #Create Update method button 
      self.buttonUpdate=QPushButton("Update")
      self.buttonUpdate.clicked.connect(self.updateImageForMethod03)
      self.buttonUpdate.setEnabled(False)
 
      # Creates the Sldiers for Contrast and luminosity control
      self.conSlider=self.mySlider()
      self.lumSlider=self.mySlider()

      #create the group box    
      self.groupBox = QGroupBox("Visualization Methods")
      self.groupBox2 = QGroupBox("Image Adjustment")
   
      #Create the input fields
      self.inputC = QLineEdit()
      self.inputW = QLineEdit()
      self.inputC.setEnabled(False)
      self.inputW.setEnabled(False)

      # Create the integer input validator
      self.onlyInt = QIntValidator()
      self.inputW.setValidator(self.onlyInt)
      self.inputC.setValidator(self.onlyInt)
      
      
      # Add the widgets into the Layout 
      self.layout.addWidget(self.imageCanvas)
      self.gridLayout.addWidget(self.chooseMethod,0,2,1,5)
      self.gridLayout.addWidget(self.labelW,1,1)
      self.gridLayout.addWidget(self.inputW,1,2)
      self.gridLayout.addWidget(self.labelC,1,3)
      self.gridLayout.addWidget(self.inputC,1,4)
      self.gridLayout.addWidget(self.buttonUpdate,1,5)
      self.layout1.addWidget(self.label1)
      self.layout1.addWidget(self.conSlider)
      self.layout1.addWidget(self.label2)
      self.layout1.addWidget(self.lumSlider)
      
   
      #set the layout to groupbox
      self.groupBox.setLayout(self.gridLayout)
      self.groupBox2.setLayout(self.layout1)
      
      #add the groupbox to main layout
      self.layout.addWidget(self.groupBox)
      self.layout.addWidget(self.groupBox2)
      self.layout.addWidget(WarningMessage3)
      # Conncet the signal with trigger methods  
      self.inputW.textChanged.connect(self.valChangedW)
      self.inputW.textChanged.connect(self.valChangedC)
      self.lumSlider.valueChanged.connect(self.lumChange)
      self.conSlider.valueChanged.connect(self.conChange)
 
      self.setLayout(self.layout)

   def updateImageForMethod03(self):
      self.changeVizMethod("Method 03 (Windowing)")
   
   def enableInputFields(self,switch):
      '''enable or disable the center and width related input fields'''

      self.inputC.setEnabled(switch)
      self.inputW.setEnabled(switch)
      self.buttonUpdate.setEnabled(switch)

   def showImage(self,image):
        '''convert it into pillow image '''
        img = Image.fromarray(image)
        qt_img = ImageQt.ImageQt(img)
        self.imageCanvas.setPixmap(QtGui.QPixmap.fromImage(qt_img))

   def changeVizMethod(self,method):
      ''' Selects between the different visualization method'''
      temp=self.dicomData.copy()
      print(method)
      if method =="Method 01 (Naive)":
         data=self.vizMethod.naiveMethod(temp)
         self.showImage(data.astype('uint8'))
         self.enableInputFields(False)
         
      elif method=="Method 02 (MinMax)":
         data=self.vizMethod.minMaxMethod(temp)
         self.showImage(data.astype('uint8'))
         self.enableInputFields(False)
      elif method =="Method 03 (Windowing)":
         data=self.vizMethod.windowingMethod(temp,int(self.windowCenter),int(self.windowWidth))
         self.showImage(data.astype('uint8'))
         self.enableInputFields(True)
      else:
         print ("Wrong Method Selected")

   def valChangedW(self,value):
      self.windowWidth=value
      

   def valChangedC(self,value):
      self.windowCenter=value
      
   def conChange(self,static_canvas):
      '''Changes the Conrast of the image'''

      #take the value from slider
      conVal = self.conSlider.value()

      #crete a local copy just for safty
      image=self.dicomData.copy()
      
      #rescale the pixel values
      image = (image - np.min(image)) * ((255 - 0) / (np.max(image) - np.min(image))+0.00001) + 0
      
      #convert the pixels into uint8
      tempPixels=np.uint8(image)      
      
      #Rescale the contrast adjustment factor
      conFactor = np.array(interp(conVal,[1,100],[0,15]))

      #adjust the contrast
      imageChanged = ImageEnhance.Contrast(Image.fromarray(tempPixels)).enhance(conFactor)

      self.showImage(np.array(imageChanged))
    
   def lumChange(self):
      '''Changes the luminosity of the image'''

      #take the value from slider
      lumVal=self.lumSlider.value()
      
      #crete a local copy just for safty
      modifiedPixels=self.dicomData.copy()
      
      #Rescale the pixel values
      modifiedPixels=np.interp(modifiedPixels,[np.min(modifiedPixels),np.max(modifiedPixels)],[0,255])
      
      #Rescale the additive factor
      lumFactor = np.array(interp(lumVal,[1,100],[-255,255]))
      
      #Modify the pixel values
      modifiedPixels=modifiedPixels+lumFactor
      
      #clip the modified value to keep in range
      modifiedPixels=np.clip(modifiedPixels,0,255)     
      
      self.showImage(modifiedPixels.astype('uint8'))

   def mySlider(self):
      '''This method builds Slider with specified parameters and returns the slider widget object'''

      mySlider= QSlider(Qt.Horizontal)
      mySlider.setMinimum(0)
      mySlider.setMaximum(100)
      mySlider.setValue(50)
      mySlider.setTickInterval(10)
      mySlider.setTickPosition(QSlider.TicksAbove)
      return mySlider


def usage():
    print ("<program name.py> -f file name | -h help")
		
def main():
    #Create a Argparser object
    parser=argparse.ArgumentParser()
    #Define the arguments 
    parser.add_argument("-f","--file", help="Please Enter the Dicom Directory in following format <program name.py> -d directory \n" )
    # Read arguments from the command line
    args = parser.parse_args()

    if args.file:
        reader=readDicom()
        dicomData=reader.readFile(args.file)
        app = QApplication(sys.argv)
        ex = mainWindow(dicomData)
        ex.show()  
    else:
        usage()
        sys.exit(2)
    sys.exit(app.exec_()) 

if __name__ == '__main__':
   main()