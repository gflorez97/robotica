# Autores:
# Luciano Garcia Giordano - 150245
# Gonzalo Florez Arias - 150048
# Salvador Gonzalez Gerpe - 150044
 
import pygame
import numpy as np
import cv2
from sklearn.neighbors.nearest_centroid import NearestCentroid
import config

hsImages = np.memmap('hsImages.driver', dtype='uint8', mode='r', shape=(config.numberOfImages, config.imageShape['height'], config.imageShape['width'], 2))
markedImages = np.memmap('markedImages.driver', dtype='uint8', mode='r', shape=(config.numberOfImages, config.imageShape['height'], config.imageShape['width'], 3))

hsVector = hsImages.reshape((config.numberOfImages*config.imageShape['height']*config.imageShape['width'],2))
markedVector = markedImages.reshape((config.numberOfImages*config.imageShape['height']*config.imageShape['width'],3))

hsExpanded = np.zeros((config.numberOfImages*config.imageShape['height']*config.imageShape['width'],3), dtype='uint8')
hsExpanded[:,:-1] = hsVector

for i in range(hsExpanded.shape[0]):
    pixel = markedVector[i]
    if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 255: # linea
        pixelClass = 1
    elif pixel[0] == 0 and pixel[1] == 255 and pixel[2] == 0: # suelo
        pixelClass = 2
    elif pixel[0] == 255 and pixel[1] == 0 and pixel[2] == 0: # marca
        pixelClass = 3
    else:
        pixelClass = 0
        
    hsExpanded[i,2] = pixelClass

shapeD = hsExpanded[hsExpanded[:,2] != 0].shape
dataset = np.memmap('dataset.driver', dtype=np.uint8, mode='w+', shape=shapeD)

dataset[:] = hsExpanded[hsExpanded[:,2] != 0]
dataset.flush()

# imagenes con pixeles en RGB
# |H|S|Clase|



