#for dir in `ls`;do echo $dir;cd $dir;python ~/proj/capstone/scripts/size_norm.py "*.png";cd ..;done
import sys
import random
import glob
from PIL import Image, ImageFilter

path = sys.argv[1]
#print path
#exit(-1)

final_size = (64,64)
images = glob.glob(path)
print(images)

for imgpath in images:
  #print(imgpath)

  img = Image.open(imgpath)
  max_sz = max(img.size)

  #make square
  #https://jdhao.github.io/2017/11/06/resize-image-to-square-with-padding/
  new_im = Image.new("RGB", (max_sz, max_sz))
  new_im.paste(img)
  new_im = new_im.resize(final_size, Image.ANTIALIAS)
  new_im.save("sizenormed_"+str(imgpath[:-3]+"png"), "PNG")


