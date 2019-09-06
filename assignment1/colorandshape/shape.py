import cv2

class shape:
	def __init__(self):
		pass
	def detect(self, c):
		shape="unidentified"
		peri = cv2.arcLength(c, True)
        #approx a poly curve with the specified precision
        #arg1-contour,arg2-dist btw contour and approximated contour,arg3-if curve is closed or not
        #2nd arg called epsilon 
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		if len(approx) == 3:
			shape = "triangle"
		elif len(approx) == 4:
			#boundingRect draws approx rect around binary image
            #x,y-mid pt
            #w-width,h-height
			(x, y, w, h) = cv2.boundingRect(approx)
            #aspect ratio- width and height ka ratio
			ar = w / float(h)
            #square-ar=1 , rect- arnot =1
			if ar >= 0.95 and ar <= 1.05:
				shape="square"
			else:
				shape="rectangle"  
		elif len(approx) == 5:
			shape ="pentagon"
		else:
			shape = "circle"
		return shape