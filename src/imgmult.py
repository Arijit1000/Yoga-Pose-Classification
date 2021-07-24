#for dir in `ls`;do echo $dir;cd $dir;python ~/proj/capstone/scripts/imgmult.py "sizenormed_*.png";cd ..;done

import sys
import random
import glob
from PIL import Image, ImageFilter

path = sys.argv[1]
#print path
#exit(-1)

images = glob.glob(path)
print(images)

for imgpath in images:
  print(imgpath)

  img = Image.open(imgpath)

  #grey scale
  imgcopy = img.copy().convert("L")
  imgcopy.save("tran_greyscale_"+str(imgpath), "PNG")

  #gaussian blur
  imgcopy = img.copy().filter(ImageFilter.GaussianBlur(2))
  imgcopy.save("tran_blur_"+str(imgpath), "PNG")

  #flip
  imgcopy = img.copy().transpose(Image.FLIP_LEFT_RIGHT)
  imgcopy.save("tran_flip_"+str(imgpath), "PNG")

  #flip & blur
  imgcopy = img.copy().transpose(Image.FLIP_LEFT_RIGHT)
  imgcopy = imgcopy.copy().filter(ImageFilter.GaussianBlur(2))
  imgcopy.save("tran_flipblur_"+str(imgpath), "PNG")
