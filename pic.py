import cv2
import sys
import random as rand
import numpy as np #this is a big library so for size requirements later I may want to optimize
import constants.py as constants

def calc_mask(color, image):
	lower = np.array([int(color[0]), 50, 50])
	upper = np.array([int(color[1]), 255, 255])
	return cv2.inRange(image, lower, upper)

def get_black_mask(image):
	return cv2.bitwise_xor(image, image)

def size(image):
	return sys.getsizeof(image)

def read(image, flag=-1):
	return cv2.imread(image, flag)	

def display(image):
	cv2.imshow('image', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def parse_setting():
	if sys.argv[2] == "colorfill":
		return 0
	elif sys.argv[2] == "lineart":
		return 1
	else:
		error("Setting not supported")

def parse_scheme():
	if sys.argv[3] == "BGR":
		return 2
	elif sys.argv[3] == "ROY":
		return 3
	else:
		error("Scheme not supported")	


def lineart(image):
	#greyscale, canny edge detection, potentially invert image
	apt = (size(image) % 5000000)
	switch = {0:7, 1:5, 2:3}
	apt = switch[apt] if apt < 3 else 3	
	#print(apt)	
	img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	img = cv2.blur(img,(apt, apt))
	img = cv2.Canny(img, 100, 200, apt)
	img = cv2.bitwise_not(img)
	return img

def colorfill(image, color_scheme):
	#color block? maybe make the pic look pixelated?
	img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	#basically I think what I want is a mask of each color, and then add them all together. okay cool. i got this. 
	masks = {}
	scheme_colors = constants.rgb_colors[:]
	if color_scheme == "ROY":
		scheme_colors = constants.roy_colors[:]
	for color in scheme_colors:
		masks[color] = cv2.bitwise_and(image, image, mask=calc_mask(constants.thresholds[color], img))
	combined_image = get_black_mask(image)
	for color in scheme_colors:
		combined_image = cv2.bitwise_or(combined_image, masks[color])	
	return combined_image

def main():
	#img = Image.open('//home//holden//Downloads//Sapphire-2-2048x2048.jpg')
	#webbrowser.open('//home//holden//Downloads//Sapphire-2-2048x2048.jpg')
	#img.show()
	img2 = '/home/holden/Downloads/Sapphire-2-2048x2048.jpg'
	img1 = '/home/holden/Downloads/citrus-citrus-fruit-delicious-2294477.jpg'
	#img3 = '/home/holden/Downloads/rainbow.jpg'
	#img = img1 if rand.randint(0, 2) == 1 else img2
	#options = {}
	#options[s] = error("Please supply an image path") #argv[1] is the image path
	#options[c] = display(colorfill(image, "RGB"))
	#ptions[l] = parse_setting() #argv[2] is the setting

	#execute = options[len(sys.argv)]
	pattern = re.compile("\-[scl]+")
	if len(sys.argv) < 2:
		error("No Image Path Provided")
	if len(sys.argv) == 2:
		image = read(sys.argv[1])
		display(colorfill(image, "BGR"))
	elif re.match(sys.argv[2], pattern):
		image = read(sys.argv[1])
		display(lineart(image))
		
	else:
		error("Bad Setting: " + argv[2] + " is not supported. Usage: \n \n -s \t color scheme \t 'ROY' 'BGR'\n" +
			"-c \t color list \t [r, o, y, g, b, i, v] or [r, y, g, c, b, m]\n" + 
			"-l \n lineart \t this is just a flag, no parameters needed\n")
		

if __name__ == "__main__":
	main()