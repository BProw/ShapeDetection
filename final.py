# CS 3150 - Image Processing & Computer Vision - Fall 2020 - Final Project
# Detect basic shapes from a test image containing 11 shapes. 
# OpenCV functions that threshold, contour, and approximate contour vertices.
# Detailed source/reference info in project directory/presentation pdf.
# Author: Brian LeProwse
# 12.08.2020


import random
import cv2 
import numpy as np
from matplotlib import pyplot as plt
import os              # Voice output shape detected (not used in submission).

shapesImg = cv2.imread('images/shapes.jpg', cv2.COLOR_RGB2BGR)

plt.figure("1")
plt.title("Original Shapes Image")
plt.imshow(shapesImg, cmap='gray', vmin = 0, vmax = 255)
plt.show()

# Convert to grayscale to process.
gray = cv2.cvtColor(shapesImg, cv2.COLOR_BGR2GRAY)


# Determine values < threshold value.  
# Inverse of the binary threshold keeps outter boundary from being detected.
_, thresh = cv2.threshold(gray, 150, 200, cv2.THRESH_BINARY_INV)


# Determine joined curves within shapes at continuous points.
# Each shape contour added to contours array.
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 
                                cv2.CHAIN_APPROX_SIMPLE)


# "Outline" curves/contours found. Negative index value finds all contours.
# Color at medium thickness (3) to clearly highlight outline. 
contourAllShapes = cv2.drawContours(shapesImg, contours, -1, (0, 0, 255), 3)

plt.figure("1.5")
plt.title("Contours Found")
plt.imshow(contourAllShapes, cmap = 'gray', vmin = 0, vmax = 255)
plt.show()

# Indices of the 11 countour shapes in the test image.
indexList = [0,1,2,3,4,5,6,7,8,9,10]
# Select random contour from list.
index = random.choice(indexList)
# print("INDEX: ", index)

# Set the specific shape contour to anaylze. 
singleShape = [contours[index]]
# print(len(contours))

# Fill in contour shape with yellow color. Negative value is applied to
# thickness param will fill the interior of the shape making it easier
# to extract. 
contourSingleShape = cv2.drawContours(shapesImg, singleShape, 
                                        0, (255, 255, 0), -1)


# Output filled in w/ color shape with prompt question as title. 
plt.figure("2")
plt.title("What shape is colored in?")
plt.imshow(contourSingleShape, cmap = 'gray', vmin = 0, vmax = 255)
plt.show()

# Find the rough vertices of each shape contour. 
# Vertice value determines the shape in question.
# (Implements Douglas-Peucker algorithm, not used in project submission).
#
shapeVertices = cv2.approxPolyDP(contours[index], 
                            0.05 * cv2.arcLength(contours[index], True), True)

# Test vertice approximation value (Future implementation).
# print("# vertices ",len(shapeVertices))


# Extract single shape using color value (hardcoded for project).
extractShape = cv2.cvtColor(contourSingleShape, cv2.COLOR_BGR2GRAY)
length, width = extractShape.shape

for i in range(length):
    for j in range(width):
        if extractShape[i][j] != 179:  
            extractShape[i][j] = 0

max_pixel = np.amax(extractShape)
print("MAX PIXEL: ", max_pixel)

plt.figure("3")
plt.title("Shape Extracted (before filtering)")
plt.imshow(extractShape, cmap = 'gray', vmin = 0, vmax = 255)
plt.show()


# Smooth image with 3x3 neighborhood median filter to remove excess contours.
medianBlurShape = np.ones((length, width), dtype = float)
for i in range(1,length-2):
        for j in range(1,width-2):
            sorted_pixels = sorted(
                np.ndarray.flatten(extractShape[i-1:i+2,j-1:j+2]))
            medianBlurShape[i][j] = sorted_pixels[4] 


# Function works better with vertex approximations. 
# medianBlurShape = cv2.medianBlur(extractShape, 3)

plt.figure("3.5")
plt.title("Shape Extracted (after filtering)")
plt.imshow(medianBlurShape, cmap = 'gray', vmin = 0, vmax = 255)
plt.show()

# Image needs to be cast to replace color in shape. 
convertImgType = np.float32(medianBlurShape)
# Re-colorize extracted shape.
replaceColor = cv2.cvtColor(convertImgType, cv2.COLOR_GRAY2RGB)

length, width, channel = replaceColor.shape
im = replaceColor
for i in range(length):
    for j in range(width):
        for k in range(channel):
            if replaceColor[i][j][k] == max_pixel:
                # Replace color pixel vals w/ those from shape extract.
                replaceColor[i][j][k] = contourSingleShape[i][j][k]


# startRow = 129
# startCol = 0
# endRow = 280
# endCol = 130

# cropped = replaceColor[startCol:endCol, startRow:endRow]
# plt.imshow(cropped)



#______________________________________________________________________________
#       "game" aspect of program (not used in project, future implementation).

# correct = len(approx)
# guess = input("Which shape is colored in?\n")

# Values (Hardcoded for project) apply to 6 of the 11 shapes in original image.
# (Conditionals and text output borrowed from YouTube video. See source (4))
# (os system statements Mac only. Not used in project submission Source (6)).
# Median filter implementation also alters vertice approximations. 
# if len(shapeVertices) == 7:
#     # os.system("say 'Arrow'")
#     cv2.putText(replaceColor, "Arrow", (10, 410), 
#                 cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 0))
# elif len(shapeVertices) >= 15:
#     # os.system("say 'Circle'")
#     cv2.putText(replaceColor, "Circle", (10, 410), 
#                 cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 0))
# elif len(shapeVertices) == 10:
#     # os.system("say 'Star'")
#     cv2.putText(replaceColor, "Star", (10, 410), 
#                 cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 0))
# elif len(shapeVertices) == 11:
#      # os.system("say 'Lightning Bolt'")
#     cv2.putText(replaceColor, "Lightning Bolt", (10, 410), 
#                 cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 0))
# elif len(shapeVertices) == 3:
#     # os.system("say 'Triangle'")
#     cv2.putText(replaceColor, "Triangle", (10, 410), 
#                 cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 0))
# elif len(shapeVertices) == 4:
#     # os.system("say 'Square'")
#     cv2.putText(replaceColor, "Square", (10, 410), 
#                 cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 0))
#______________________________________________________________________________

plt.figure("4")
plt.title("Extracted Shape Re-Colorized")
plt.imshow(replaceColor.astype('uint8'))
plt.show()

plt.show()
cv2.waitKey(7000)
cv2.destroyAllWindows()
