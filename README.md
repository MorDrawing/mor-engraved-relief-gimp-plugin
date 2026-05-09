# mor-engraved-relief-gimp-plugin

A Moribund Institute GIMP 3 plug-in for creating engraved relief and intaglio-style bevel effects.

**Mor Engraved Relief** adds a clean raised-relief / engraved-bevel effect to RGBA layers. It is useful for text, logos, icons, ornamental shapes, faux engraved plates, cameo-like relief, and other MorDrawing whatnot.

The plug-in appears in GIMP under:

```text
Filters > Layer Styles > Mor Engraved Relief...
```

## Features

- Creates a raised relief / engraved bevel effect for the selected layer.
- Uses a smooth Euclidean distance transform for the height map.
- Computes surface normals from Sobel gradients.
- Uses a configurable light angle and altitude.
- Creates highlight and shadow passes using Screen and Multiply layer modes.
- Merges the result into a tidy `mor-engraved-relief` layer.
- Preserves the original source layer.
- Written as a GIMP 3 Python plug-in.

## Requirements

- GIMP 3.2 or newer
- Python support for GIMP 3
- NumPy
- SciPy

## Installation for regular users

### Linux

Install NumPy and SciPy first.

Arch Linux / Manjaro:

```bash
sudo pacman -S --needed python-numpy python-scipy
```

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install python3-numpy python3-scipy
```

Fedora:

```bash
sudo dnf install python3-numpy python3-scipy
```

Then copy the plug-in folder into your GIMP plug-ins directory:

```bash
mkdir -p ~/.config/GIMP/3.2/plug-ins/mor_engraved_relief_plugin
cp *.py ~/.config/GIMP/3.2/plug-ins/mor_engraved_relief_plugin/
chmod +x ~/.config/GIMP/3.2/plug-ins/mor_engraved_relief_plugin/mor_engraved_relief_plugin.py
```

Restart GIMP.

The plug-in should appear under:

```text
Filters > Layer Styles > Mor Engraved Relief...
```

### Windows 11

For normal users, install from a release package when one is available.

To find the correct plug-ins folder, open GIMP and go to:

```text
Edit > Preferences > Folders > Plug-ins
```

Copy the plug-in folder into the user plug-ins folder listed there, then restart GIMP.

### macOS

For normal users, install from a release package when one is available.

To find the correct plug-ins folder, open GIMP and go to:

```text
GIMP > Settings > Folders > Plug-ins
```

or:

```text
Edit > Preferences > Folders > Plug-ins
```

depending on your GIMP build.

## Installation for developers

Clone the repository:

```bash
git clone https://github.com/MorDrawing/mor-engraved-relief-gimp-plugin.git
cd mor-engraved-relief-gimp-plugin
```

Or with SSH:

```bash
git clone git@github.com:MorDrawing/mor-engraved-relief-gimp-plugin.git
cd mor-engraved-relief-gimp-plugin
```

For local Linux testing:

```bash
mkdir -p ~/.config/GIMP/3.2/plug-ins/mor_engraved_relief_plugin
cp *.py ~/.config/GIMP/3.2/plug-ins/mor_engraved_relief_plugin/
chmod +x ~/.config/GIMP/3.2/plug-ins/mor_engraved_relief_plugin/mor_engraved_relief_plugin.py
```

Restart GIMP after copying files.

## Usage

1. Open an image in GIMP.
2. Select the layer you want to bevel.
3. Make sure the layer has transparency / alpha where the relief should be computed.
4. Go to:

```text
Filters > Layer Styles > Mor Engraved Relief...
```

5. Adjust the settings:
   - **Size**: bevel radius in pixels.
   - **Soften**: edge softness.
   - **Depth (%)**: bump intensity.
   - **Angle**: light direction in degrees.
   - **Altitude**: light height in degrees.
   - **Highlight Opacity**: strength of the highlight pass.
   - **Shadow Opacity**: strength of the shadow pass.
6. Click **OK**.

The plug-in creates a new merged effect layer named:

```text
mor-engraved-relief
```

## Repository layout

```text
.
├── LICENSE
├── README.md
├── mor_engraved_relief_plugin.py
├── ls_engine.py
├── ls_env.py
├── ls_utils.py
└── .gitignore
```

## Rename notes

Older local versions of this project used names such as `intaglio-bevel`, `intaglio_bevel_plugin.py`, and `python-fu-intaglio-bevel`.

The public repository name is now:

```text
mor-engraved-relief-gimp-plugin
```

The user-facing GIMP menu name is now:

```text
Mor Engraved Relief...
```

The GIMP procedure name is now:

```text
python-fu-mor-engraved-relief
```

## Credits

Algorithm derived from Krita's `kis_ls_bevel_emboss_filter.cpp` by Dmitry Kazakov and the LayerFX GIMP plug-in by Jonathan Stipe.

## License

GPL-2.0-or-later. See `LICENSE`.
