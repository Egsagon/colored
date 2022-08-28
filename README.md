# colored
Script to change the color palette of the current rice.

## Usage

Call `PLT.py`, which will ask you to select a scheme and will apply it.
There are also options to implement it in another application, like `eww` (see the eww directory).

You can add your own palettes in `./colored/palettes/` and your own apps in `./colored/apps/`

Note: I doubt anyone will be using this masterpiece, so the following docs are pretty much just for me to remenber the f*ck i've done here.

## Structure

```sh
.
├── bain
│   ├── bain            # Script to dispay battery
│   ├── colors.sh       # Colors for bain
│   └── images/*.png    # Images used by bain
├── colored
│   ├── apps/*.json     # Data on how to rice each app
│   ├── palettes/*.json # Color palettes
│   ├── images/*.png    # Source for the images to color
│   ├── current.json    # Current used palette
│   ├── images_theme.py # Script for changing images colors
│   ├── imgize.py       # Script for creating palettes images
│   └── PLT.py          # Main script for changing colors
└── eww
    ├── eww.scss        # EWW style
    ├── eww.yuck        # EWW bar
    └── hider.yuck      # Popup for hiding when changing scheme

7 directories, 52 files
```

## Scripts

### `PLT.py` - Applies a given color palette from the list in ./colored/palettes.
Each mofication is represented by a json file in the ./colored/apps directory, and can have 3 modes:
```
  - command:  execute a list of bash commands;
  - ow-all:   overwrite the content of a file. Placeholder for palette colors can be used (@bg, @fg, etc.);
  - ow-line:  same as ow-line, but for large files, were you only want to modify a small number of lines.
```

<details><summary>See format</summary>
<p>

```jsonc
{
  "name": "...",    // A custom name (used only in debug).
  "active": true,   // Wether to authorize the modifications or not.
  "type": "...,"    // Type of the modification. Value can be command (execute bash lines),
                    // ow-all (modify the content of a file), or ow-line (modify file line-per-line).
  
  "commands": [],   // On command mode, a list of strings to be executed by bash.
  
  "path": "...",    // On ow-* mode, the path of the file to modify.
  "value": "...",   // On ow-all mode, the content of the file to overwrite.
  "lines": {},      // On ow-lines mode, a dict containing the number of the line as the key and the
                    // string to replace the line with.
  "done": "..."     // A bash command to execute when scheme has be applied for the app.
}
```
</p></details>

<details><summary>Example for rofi</summary>
<p>

```jsonc
{
    "name": "Rofi",
    "active": true,
    "type": "ow-all",

    "path": "/home/egsagon/.config/rofi/colors.rasi",
    "value": "*{al:@bg;bg:@com_acc;se:@com_acc;fg:@com_fg;ac:@bg;}"
}
```
</p></details>

### `images_theme.py` - Colorize a given image 

\#TODO

### `imgsize.py` - Create an image of a color palette

This script will create a png representation of a json palette from ./colored/palettes for
application like eww to visualize (see eww section).

```sh
python3 imgsize <palette_name> <output_path>
```

### Dependencies

- `gum`
- python PIL
