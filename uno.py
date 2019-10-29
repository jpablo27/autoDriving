import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image, line_parameters):
	slope, intercept = line_parameters
	y1 = image.shape[0]
	y2 = int(y1*(3.0/5.0))
	print y2
	x1 = int((y1 - intercept)/slope)
	x2 = int((y2 - intercept)/slope)
	return np.array([x1,y1,x2,y2])

def average_slope_intercept(image, lines):
	left_fit = []
	right_fit =[]

	for line in lines:
		x1,y1,x2,y2 = line.reshape(4)
		parameters = np.polyfit((x1,x2),(y1,y2),1)

		slope = parameters[0]
		intercept = parameters[1]

		if slope < 0:
			left_fit.append((slope, intercept))
		else:
			right_fit.append((slope, intercept))

	left_fit_average = np.average(left_fit, axis =0)
	right_fit_average = np.average(right_fit, axis =0)
	
	left_line = make_coordinates(image, left_fit_average)
	right_line =  make_coordinates(image, right_fit_average)

	print(left_fit_average)
	print(right_fit_average)
	return np.array([left_line, right_line])


def canny(image):
    gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
    blur =  cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def roi(image):
	height = image.shape[0]
	mask = np.zeros_like(canny)
	triangle = np.array([[(200, height),(550, 250),	(1100, height),]], np.int32)
	cv2.fillPoly(mask, triangle, 255)
	masked_image = cv2.bitwise_and(image, mask)
	return masked_image

def display_lines(img,lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            x1, y1,x2,y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1),(x2,y2),(255,0,0),10)
    return line_image

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny =  canny(lane_image)
cropped_image = roi(canny)
lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180,100, np.array([]),minLineLength=40, maxLineGap=5)
avg_lines = average_slope_intercept(lane_image, lines)
line_image = display_lines(lane_image, avg_lines)
combo_image = cv2.addWeighted(lane_image, 0.8,line_image, 1, 1)

cv2.imshow("hey",line_image)
cv2.waitKey(0)

 