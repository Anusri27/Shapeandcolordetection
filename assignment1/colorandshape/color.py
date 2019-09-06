from scipy.spatial import distance as dist
#scipy -scientific operations , distance here euclidean distance ke liye
from collections import OrderedDict
#OrderedDict preserves the order in which the keys are inserted.
import numpy as np
import cv2
class color:
	def __init__(self):
        #same order will be maintained
		colors = OrderedDict({
			"red": (255, 0, 0),
			"green": (0, 255, 0),
			"blue": (0, 0, 255)})

		#lab image, l-intensity/light a-green se magenta, b-blue se yellow
        #if light and dark image of same object is taken in rbg toh values for rbg all will change 
        #but for lab , a and b will be same only l-intelsity will change
		self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
		self.Names = []

		for (i, (name, rgb)) in enumerate(colors.items()):
			self.lab[i] = rgb
			self.Names.append(name)
		self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)
        #converted rgb to lab image
		
	def label(self, image, c):
        #creating mask of h*w
		mask = np.zeros(image.shape[:2], dtype="uint8")
        #contour-curve joining cont. pts
        #arg1-src img, arg2-contour passed as py list,arg3- index of contour(-1 fr all contours)
        #arg4-color, arg5-thickness 
		cv2.drawContours(mask, [c], -1, 255, -1)
        #erode discards near boundary of foreground image
		mask = cv2.erode(mask, None, iterations=2)
        #mean of each color channel
		mean = cv2.mean(image, mask=mask)[:3]
        #min dist till now
        #inf -floating pt rep of infinity
		minDist = (np.inf, None)
		for (i, row) in enumerate(self.lab):
			#current value and mean ke beech ka dist
			d = dist.euclidean(row[0], mean)
			if d < minDist[0]:
				minDist = (d, i)
		# name of the color with the least distance
		return self.Names[minDist[1]]


