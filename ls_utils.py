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
ls_utils.py
-----------
Pure math helpers for the Layer Styles engine.
Ported from Krita's KisLsUtils (Dmitry Kazakov).

No GIMP or GEGL imports here — this module is framework-agnostic
so it can be unit-tested independently.
"""

import math


class LSUtils:

    @staticmethod
    def angle_to_light_vector(angle_degrees: float, altitude_degrees: float = 30.0) -> tuple:
        """
        Converts a PSD/Krita-style azimuth + altitude pair into a
        normalized 3D light direction vector.

        angle_degrees   : horizontal rotation (0–360), clockwise from top
        altitude_degrees: vertical tilt (0 = horizon, 90 = directly above)

        Returns (x, y, z) unit vector pointing FROM the light source.

        Equivalent to Krita's angleToVector logic in kis_ls_utils.cpp.
        """
        az  = math.radians(angle_degrees)
        alt = math.radians(altitude_degrees)

        x = math.cos(az) * math.cos(alt)
        y = math.sin(az) * math.cos(alt)
        z = math.sin(alt)
        return (x, y, z)

    @staticmethod
    def soften_radius(size: int, soften: int) -> float:
        """
        Translates the Bevel 'Size' and 'Soften' sliders into a
        Gaussian standard-deviation radius for the GEGL blur node.

        Matches Krita's balance between slope sharpness (size) and
        edge softness (soften). Minimum of 1.0 prevents a zero-radius
        blur that would be a no-op.
        """
        return max(1.0, (size + soften) / 3.0)

    @staticmethod
    def depth_to_scale(depth: int) -> float:
        """
        Converts the 1–100 'Depth' slider to a bump-map depth scale.
        Krita uses a 0.0–10.0 internal range; we mirror that here.
        """
        return max(0.1, depth / 10.0)