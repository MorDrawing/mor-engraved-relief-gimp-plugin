# SPDX-License-Identifier: GPL-2.0-or-later
#
# Mor Engraved Relief — raised relief / intaglio-style bevel for GIMP 3.2
# Copyright (C) 2026 Moribund Institute

"""
ls_env.py — spatial context helpers for Mor Engraved Relief.
"""

import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp


class LSEnvironment:
    def __init__(self, drawable: Gimp.Drawable):
        self.drawable = drawable
        offsets = drawable.get_offsets()
        self.x = offsets[0]
        self.y = offsets[1]
        self.width = drawable.get_width()
        self.height = drawable.get_height()

    def needed_rect(self, expansion: int) -> tuple:
        return (
            self.x - expansion,
            self.y - expansion,
            self.width + expansion * 2,
            self.height + expansion * 2,
        )

    def __repr__(self) -> str:
        return f"LSEnvironment(x={self.x}, y={self.y}, w={self.width}, h={self.height})"
