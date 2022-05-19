import json
import requests
import webbrowser
from PIL import Image
import glob

with open ("imagesnames.json" ,"r") as f:
    foodimages = json.load(f)
    
image_list = []
for filename in (\static\images): #assuming gif
    im=Image.open(filename)
    image_list.append(im)
print (image_list)