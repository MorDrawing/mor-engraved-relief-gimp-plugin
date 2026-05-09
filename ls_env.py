# SPDX-License-Identifier: GPL-2.0-or-later
#
# Antiquarian Etch Bevel — Bevel & Emboss layer style for GIMP 3.2
# Copyright (C) 2026 MoribundMurdoch
#
# Algorithm derived from Krita's kis_ls_bevel_emboss_filter.cpp
# Copyright (C) 2014 Dmitry Kazakov
# and the LayerFX GIMP plugin (2008) by Jonathan Stipe.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

"""
ls_env.py
---------
Manages the spatial context of a layer during effect processing.
Ported from KisLayerStyleFilterEnvironment (Dmitry Kazakov).

Responsible for:
  - Tracking layer bounds (offsets + dimensions)
  - Computing the "needed rect" — the expanded area required so
    blur/shadow effects are never clipped at layer edges
  - Providing a clean interface so ls_engine.py never has to
    touch GIMP geometry calls directly
"""

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp


class LSEnvironment:

    def __init__(self, drawable: Gimp.Drawable):
        """
        Captures the drawable's current bounds at construction time.
        Equivalent to KisLayerStyleFilterEnvironment storing layerBounds().
        """
        self.drawable = drawable

        # Gimp.Drawable.get_offsets() returns (x, y)
        offsets = drawable.get_offsets()
        self.x      = offsets[0]
        self.y      = offsets[1]
        self.width  = drawable.get_width()
        self.height = drawable.get_height()

    def needed_rect(self, expansion: int) -> tuple:
        """
        Returns (x, y, width, height) of the expanded processing area.

        'expansion' is the pixel radius of the largest effect being applied
        (e.g. the bevel size or shadow spread). We extend in all four
        directions unconditionally — matching Krita's rule that the rect
        should always expand regardless of effect position, to prevent
        any edge clipping.

        Equivalent to the neededRect / applyRect logic in
        kis_ls_bevel_emboss_filter.cpp.
        """
        return (
            self.x      - expansion,
            self.y      - expansion,
            self.width  + expansion * 2,
            self.height + expansion * 2,
        )

    def __repr__(self) -> str:
        return (
            f"LSEnvironment("
            f"x={self.x}, y={self.y}, "
            f"w={self.width}, h={self.height})"
        )