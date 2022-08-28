#!/usr/bin/python3

import os
import sys
import json
import threading
import subprocess
import images_theme
from random import randint
from time import sleep, time

# ============================================ Settings ======================================================= #
DIR = '/home/egsagon/colored'                                   # This dir                                      #
APPS = os.listdir(f'{DIR}/apps')                                # Apps dir                                      #
PLTS = os.listdir(f'{DIR}/palettes')                            # Palettes dir                                  #
KEYS = ['com_fg', 'fg', 'com_acc', 'accent', 'com_bg', 'bg']    # Palettes color keys                           #
colorize_images = True                                          # Do take care of images                        #
desk_widgets = ['desk', 'bar']                                  # Present widgets on root                       #
use_hider = True                                                # Use a hide popup                              #
wait_for_images = False                                         # Do wait for images to be painted              #
min_wait_time = 2.5 #4.5                                        # Minimum time to wait (for cool gif in hider)  #
# ============================================================================================================= #

# Check wether the desk_widgets are open so they aren't opened by mistake
opened = [l.replace('*', '').rstrip() for l in os.popen('eww windows').readlines() if '*' in l]
desk_widgets = [w for w in desk_widgets if w in opened]

# Get the palette name
if len(sys.argv) >= 2:
    if sys.argv[1] == '-list':
        print(json.dumps([p.split('.')[0] for p in PLTS]))
        exit()
    
    elif sys.argv[1] == '-rand': name = PLTS[randint(0, len(PLTS) - 1)]
    
    else: name = sys.argv[1] + '.json'

else: name = subprocess.run(["gum", "choose"] + PLTS, stdout=subprocess.PIPE, text=True).stdout.strip()

raw = open(f'{DIR}/palettes/{name}', 'r').read()
PLT = json.loads(raw)
print(f'[PLTS] Loaded palette {name}')

# Save the palette as current
old = json.load(open(f'{DIR}/current.json', 'r'))
open(f'{DIR}/current.json', 'w').write(raw)
print(f'[PLTS] Overwrote current palette')

# Hide screen
start = time()
if use_hider:
    # Quick fix because im tired of eww widgets staying on top of all windows
    subprocess.call(['eww', 'close'] + desk_widgets)
    
    # Open hider popup to hide the mess
    subprocess.call(['eww', 'update', 'show-hider=false'])
    subprocess.call(['eww', 'open', 'hider'])
    subprocess.call(['eww', 'update', 'show-hider=true'])
    sleep(0.1)

# Execute change for each application
print(f'[APPS] Changing theme of apps...')
for name in APPS:
    # Load the app
    app = json.load(open(f'{DIR}/apps/{name}', 'r'))
    if not app['active']: continue
    print(f"[APPS] > {app['name']}")
    
    if app['type'] == 'command':
        # Execute add command
        for cmd in app['commands']: os.popen(cmd)
    
    elif app['type'] == 'ow-all':
        # Overwrite the whole file
        
        data = app['value']
        
        for key in KEYS: data = data.replace(f'@{key}', PLT[key])
        data = data.replace('@theme', PLT['theme'].capitalize())
        
        open(app['path'], 'w').write(data)
    
    elif app['type'] == 'ow-line':
        # Overwrite a line in the file
        
        lines = open(app['path'], 'r').readlines()
        
        for n, rule in app['lines'].items():
            for key in KEYS: rule = rule.replace(f'@{key}', PLT[key])
            rule = rule.replace('@theme', PLT['theme'].capitalize())
            lines[int(n) - 1] = rule
        
        open(app['path'], 'w').writelines(lines)
    
    elif app['type'] == 'images' and colorize_images:
        
        for source, path in app['data'].items():
            
            exe = lambda: images_theme.colorize(source, PLT, path)
            
            if wait_for_images: exe()
            else: threading.Thread(target = exe).start()
            
            print(f'[IMGS] Recolored {source}')
    
    # Execute end command if there is one
    if 'done' in app.keys(): subprocess.call(app['done'].split())

print(f'[APPS] Finished process in {round(time() - start, 3)}s.')

# Sleep for the left time b4 min_wait_time
left = min_wait_time - (time() - start)
if left > 0: sleep(left)

# Unhide popup
if use_hider:
    # Hide
    subprocess.call(['eww', 'update', 'show-hider=false'])
    
    # Wait for animation to finish
    sleep(0.5)
    
    # Close window
    subprocess.call(['eww', 'close', 'hider'])
    subprocess.call(['eww', 'open-many'] + desk_widgets)