# Autores:
# Luciano Garcia Giordano - 150245
# Gonzalo Florez Arias - 150048
# Salvador Gonzalez Gerpe - 150044

import numpy as np
import cv2
from matplotlib import pyplot as plt
import config
import math
import os
import time
import setup
import segmentLinesAndSymbolsFromImage
import consignaFromSegmentation

times = []

previousData = {
    "angle": 0,
    "distance": 0
}

try:
    while (setup.capture.isOpened()):
        beg = time.time()

        arrow, line, imageOnPaleta = segmentLinesAndSymbolsFromImage.fetchImageAndSegment(setup)

        speed, rotation, numberOfExits = consignaFromSegmentation.calculateConsignaFullProcess(line, arrow, imageOnPaleta, previousData, setup)

        shapeName = consignaFromSegmentation.predictShapeIfShape(arrow, setup)
        if (not (shapeName == None or shapeName == 'touches edges' or shapeName == 'nothing')) and numberOfExits <= 1:
            print(shapeName)

        end = time.time()
        times.append(end - beg)

        if setup.showSegmentedImage:
            cv2.imshow('segmented treated image', cv2.cvtColor(imageOnPaleta[0::setup.segmentedImageShrinkFactor,0::setup.segmentedImageShrinkFactor,:], cv2.COLOR_RGB2BGR))
        if setup.drawAndRecordSchematicSegmentation:
            setup.schematicsVideoOutput.write(cv2.cvtColor(imageOnPaleta, cv2.COLOR_RGB2BGR))

        times.append(time.time() - beg)

        cv2.waitKey(1)
    
except TypeError as a:
    print(a)
finally:
    # print(times)
    print(np.mean(np.array(times)), 'was the time per frame')