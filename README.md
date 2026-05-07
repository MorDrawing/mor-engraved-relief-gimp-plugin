# Intaglio Bevel

A GIMP 3.2 plugin that adds a clean, raised-relief Bevel & Emboss layer effect to RGBA layers — flat angular planes with smooth slopes, suited to cameo, engraving, and lapidary work. Appears under Filters > Layer Styles > Intaglio Bevel...

The bevel is computed in pure Python with NumPy and SciPy. The height map is built from a Euclidean distance transform (sub-pixel accurate, no staircase artifacts), surface normals from Sobel gradients, lighting via dot product against the configured light vector. The result is split into a highlight layer (Screen blend, pure white) and a shadow layer (Multiply blend, pure black), so the source layer is preserved everywhere the slope is zero.

A sister project, antiquarian-etch-bevel-gimp, uses iterative integer erosion for an aggressive scratched/etched look. This one is the polished alternative.

## Install

Requires GIMP 3.2+, numpy, scipy.

On Arch: sudo pacman -S python-numpy python-scipy
Otherwise: pip install numpy scipy --break-system-packages

Then:
mkdir -p ~/.config/GIMP/3.2/plug-ins/intaglio_bevel_plugin
cp *.py ~/.config/GIMP/3.2/plug-ins/intaglio_bevel_plugin/
chmod +x ~/.config/GIMP/3.2/plug-ins/intaglio_bevel_plugin/intaglio_bevel_plugin.py

Restart GIMP. The filter appears under Filters > Layer Styles > Intaglio Bevel...

## Credits

Algorithm derived from Krita's kis_ls_bevel_emboss_filter.cpp by Dmitry Kazakov, gimp_bump_map.cpp (Federico Mena Quintero, Jens Lautenbacher, Sven Neumann, 1997), and the LayerFX GIMP plugin by Jonathan Stipe (2008).

## License

GPL-2.0-or-later — same as Krita. See LICENSE.
