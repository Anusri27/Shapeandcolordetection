from colorandshape.shape import shape
from colorandshape.color import color
import argparse
#imutils for simple img processing
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
#arg1-image,arg2-kernel size,
blurred = cv2.GaussianBlur(resized, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
#threshold - grayscale ko binary img convert
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("Thresh", thresh)
# find contours in the thresh
#chainapproxsimple-compresses horizontal, vertical, and diagonal segments and leaves only their end points
#retr_external-retrieves only extreme outer contours
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#manage return signature according to version of cv2(doubt!!!)
cnts = imutils.grab_contours(cnts)
sd = shape()
cl = color()

for c in cnts:
	#Moment is weighted average of image pixel intensities with 
    #which we can find some specific propertie like radius, area, centroid 
	M = cv2.moments(c)
    #formula for centroid
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)
	color = cl.label(lab, c)

	
	c = c.astype("float")
    #multipling c with reize ratio
	c *= ratio
	c = c.astype("int")
    #output ka format
	text = "{} {}".format(color, shape)
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, text, (cX, cY),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	cv2.imshow("Image", image)
	cv2.waitKey(0)