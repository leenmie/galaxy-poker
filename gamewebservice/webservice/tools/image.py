'''
Created on Sep 18, 2012

@author: leen
'''
from PIL import Image
#import ImageEnhance
#import ImageFilter
import random
sysrandom = random.SystemRandom()

def random_size(size):
    w, h = size
    return (sysrandom.randint(w,int(w*1.5)), sysrandom.randint(h,int(h*1.5)))

def mono_color(image):
    result = image.convert('1')
    #L,A = result.split()
    # a fully saturated band 
    #S, = Image.new('L', result.size, random.randint(0,255)).split()
    # re-combine the bands
    # this keeps tha alpha channel in the new image
    #result = Image.merge('RGBA', (S,L,L,A))  
    return result

import os
IMAGE_PATH = os.getcwd() + '/webservice/images' 

class CaptchaCardImage():
    
    def __init__(self, length=2):
        self._length = length
        self._values = []
        self._image = None
        self.generate_image()
        
    def generate_image(self):
        images = []
        values = []
        total_width = 0
        total_height = 0
        for _ in range(self._length):
            card_value = sysrandom.randint(0,51)
            image_name = '{}/{}.png'.format(IMAGE_PATH, card_value)
            im = Image.open(image_name)#.convert('RGBA')
            im = im.resize(random_size(im.size))
            #im = im.filter(ImageFilter.EMBOSS)
            im = im.rotate(sysrandom.randint(-45,45),expand=1)
            im = mono_color(im)
            im_width, im_height = im.size
            total_width += im_width
            total_height = max(total_height, im_height)
            images.append(im)
            values.append(card_value)
        blank_bg = (sysrandom.randint(0,100),sysrandom.randint(0,100),sysrandom.randint(0,100),255)
        blank = Image.new("RGBA",(total_width, total_height),blank_bg)
        current_x = 0
        for _i in range(self._length):
            blank.paste(images[_i],(current_x,0),images[_i])
            w,h = images[_i].size
            current_x += w
        blank = blank.resize((100*self._length,100))
        self._image = blank
        self._values = values 
        #blank.save(self._filename)
    def get_image(self):
        return self._image
    
    def get_encode_string_values(self):
        return '|'.join([str(v) for v in self._values])
            

#image1_name = 'images/{}.png'.format(random.randint(0,51))
#im1 = Image.open(image1_name)#.convert('RGBA')
#im1 = im1.resize(random_size(im1.size))
##im1 = im1.filter(ImageFilter.EMBOSS)
#im1 = im1.rotate(random.randint(-45,45),expand=1)
#im1 = mono_color(im1)
#im1_width, im1_height = im1.size
#
#
#image2_name = 'images/{}.png'.format(random.randint(0,51))
#im2 = Image.open(image2_name)
#im2 = im2.resize(random_size(im2.size))
##im2 = im2.filter(ImageFilter.EMBOSS)
#im2 = im2.rotate(random.randint(-45,45),expand=1)
#im2 = mono_color(im2)
#im2_width, im2_height = im2.size
#
#
#blank_bg = (random.randint(100,255),random.randint(0,255),random.randint(0,255),255)
#blank = Image.new("RGBA",(im1_width+im2_width,max(im1_height,im2_height)),blank_bg)
#blank.paste(im1,(0,0),im1)
#blank.paste(im2,(im1_width,0),im2)
#blank = blank.resize((200,100))
#blank.save('out.jpg')
if __name__ == '__main__':
    for k in range(1000):
        image = CaptchaCardImage(length=3)
        #image.generate_image() 
    #print image.get_encode_string_values()
