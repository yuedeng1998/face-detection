from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc
import matplotlib.pyplot as plt

def MakePyramid(image, minisize):
    """
    Make a pyramid for a image with different sizes which all bigger than the minisize

    Inputs:
    ----------------

    image       The PIL image.

    minisize    a pair of integer

    Output:
    ----------------
    pyramid     a array with different size of images scaled with 0.75 each level

    """   
    pyramid = []    
    resize_index = 0.75   
    wid, hei = image.size
    width, height = minisize
    while (wid>=width) and (hei>= height):
        #if the next resize image not smaller than minsize
        #we store it to pyramid
    	pyramid.append(image)
    	wid, hei = int(wid*resize_index),int(hei*resize_index)
        #update the agruments
        image = image.resize((wid,hei), Image.BICUBIC)
        #resize the image
    return pyramid






def ShowPyramid(pyramid):
        """
    Show all the levels of images in one big image

    Inputs:
    ----------------

    pyramid     a array with different size of images scaled with 0.75 each level

    Output:
    ----------------
    Show the created image in a window
    """ 
	im = pyramid[0]
	width, height = im.size
	for i in pyramid:
		height += i.height
        #count the total height needed to paste all the images 
	image = Image.new("L", (width, height), color = 'white')
    #create a big image to be pasted with white background
	offset_x,offset_y = 0, 0
	for i in pyramid:
		image.paste(i,(offset_x,offset_y))
		x,y = i.size
		offset_y = offset_y + y
        #update the offset where to plcae the next image
	plt.imshow(image)
	plt.show()


def FindTemplate(pyramid, template, threshold):
    """
    check where the template image is in the original image
    just reserve points above the threshold

    Inputs:
    ----------------

    pyramid     a array with different size of images scaled with 0.75 each level

    template    The template. A PIL image.  Elements cannot all be equal.

    threshold   a float

    Output:
    ----------------
    show the all places of templete found from the original image with red rectangles

    """
    im = pyramid[0]
    tw,th = template.size
    clistx =[]
    clisty =[]
    temp = template.resize((int(15), int(th* 15/tw)))
    #resize the template to 15 pixel
    tw,th = temp.size
    for i in range(len(pyramid)):
    	c = ncc.normxcorr2D(pyramid[i], temp)
        #check the correlation for the image
        center = np.where(c > threshold)
        #find where the ncc is bigger than then threshold
        times = (1/(pow(0.75,i)))
        #the mutiplyer we need to convert the point back to original image
        listx = center[1]
        listy = center[0]
        #listx/y store all the selected points' x/y value
        clistx = [x*times for x in listx]
        clisty = [y*times for y in listy]
        #copy them to gloabl array clistx and clisty
        im = im.convert('RGB')
      	draw = ImageDraw.Draw(im)
        #convert the image to draw red lines
      	for m in range(len(clisty)):
        	x1 = clistx[m] - tw * times/2
        	x2 = clistx[m] + tw * times/2
        	y1 = clisty[m] + th * times/2
        	y2 = clisty[m] - th * times/2
            #find the 4 values need to draw the red lines and set the template back size
        
        	draw.line((x1,y1,x2,y1),fill="red",width=2)
        	draw.line((x1,y1, x1, y2),fill="red",width=2)
        	draw.line((x2,y1, x2,y2),fill="red",width=2)
        	draw.line((x1, y2, x2, y2),fill="red",width=2)
        
    	del draw

    im.show()
    
        

    
def main():
    
    template = Image.open('faces/template.jpg')
    im = Image.open('faces/judybats.jpg')
    im2 = Image.open('faces/students.jpg')
    im3 = Image.open('faces/fans.jpg')
    im4 = Image.open('faces/family.jpg')
    im5 = Image.open('faces/sports.jpg')
    im6 = Image.open('faces/tree.jpg')

    threshold = 0.53
    pyramid = MakePyramid(im,(15, 15))
    FindTemplate(pyramid, template, threshold)
    pyramid2 = MakePyramid(im2,(15, 15))
    FindTemplate(pyramid2, template, threshold)
    pyramid3 = MakePyramid(im3,(15, 15))
    FindTemplate(pyramid3, template, threshold)
    pyramid4 = MakePyramid(im4,(15, 15))
    FindTemplate(pyramid4, template, threshold)
    pyramid5 = MakePyramid(im5,(15, 15))
    FindTemplate(pyramid5, template, threshold)
    pyramid6 = MakePyramid(im6,(15, 15))
    FindTemplate(pyramid6, template, threshold)


    
    ShowPyramid(pyramid)
    
    
    
main()   
             
    