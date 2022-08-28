import os
import json
import subprocess
from random import randint
from time import sleep

source_colors = {
    # Source color: palette key
    
    "black": "bg",
    'red': "accent",
    'blue': "com_bg"
}

def colorize(input: str, img_plt: dict, output: str) -> None:
    
    global source_colors
    temp = randint(0, 100000000)
    cur = input
    
    for color, key in source_colors.items():
        subprocess.call(['convert', cur, '-fill', img_plt[key], '-opaque', color, f'/tmp/{temp}.png'])
        
        sleep(0.4) # wait for image to generate
        cur = f'/tmp/{temp}.png'
    
    subprocess.call(['mv', cur, output])

# colorize('./images/mars_source.jpg', json.load(open('current.json', 'r')), 'test.jpg')