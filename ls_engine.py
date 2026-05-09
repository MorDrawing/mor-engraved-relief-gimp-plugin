# SPDX-License-Identifier: GPL-2.0-or-later
#
# Intaglio Bevel — Smooth raised-relief Bevel & Emboss for GIMP 3.2
# Copyright (C) 2026 MoribundMurdoch
#
# Algorithm derived from Krita's kis_ls_bevel_emboss_filter.cpp
# Copyright (C) 2014 Dmitry Kazakov
# and the LayerFX GIMP plugin (2008) by Jonathan Stipe.
"""
ls_engine.py — Smooth Bevel & Emboss

Height map: smooth Euclidean distance transform (sub-pixel accurate).
Layers:     pure white (Screen) and pure black (Multiply) with the
            lighting carried in alpha. Source pixels are preserved
            wherever the slope is zero. Both layers merged into a
            single 'bevel' layer at the end for tidy layer panel.
"""
import gi, math
gi.require_version('Gimp', '3.0')
gi.require_version('Gegl', '0.4')
from gi.repository import Gimp, Gegl

import numpy as np
from scipy.ndimage import gaussian_filter, sobel, distance_transform_edt

LOG = __import__('os').path.expanduser("~/.config/GIMP/3.2/intaglio_debug.log")
def log(msg):
    with open(LOG, "a") as f:
        f.write(msg + "\n")

# ---------------------------------------------------------------------------
# GEGL buffer ↔ numpy
# ---------------------------------------------------------------------------

def buf_to_numpy(buf, w, h):
    rect = Gegl.Rectangle()
    rect.x, rect.y, rect.width, rect.height = 0, 0, w, h
    data = buf.get(rect, 1.0, "R'G'B'A u8", Gegl.AbyssPolicy.NONE)
    return np.frombuffer(bytes(data), dtype=np.uint8).reshape(h, w, 4).copy()

def numpy_to_buf(arr, buf, w, h):
    rect = Gegl.Rectangle()
    rect.x, rect.y, rect.width, rect.height = 0, 0, w, h
    buf.set(rect, "R'G'B'A u8", arr.astype(np.uint8).tobytes())

# ---------------------------------------------------------------------------
# Bevel computation
# ---------------------------------------------------------------------------

def compute_bevel(rgba, size, soften, angle, altitude, depth,
                  hi_opacity, sh_opacity):
    h, w = rgba.shape[:2]
    alpha = rgba[:, :, 3].astype(np.float32) / 255.0

    mask = alpha > 0.5
    dist = distance_transform_edt(mask).astype(np.float32)
    height = np.clip(dist / float(size), 0.0, 1.0)

    if soften > 0:
        height = gaussian_filter(height, sigma=float(soften) / 2.0)

    depth_scale = depth / 50.0
    gx = sobel(height, axis=1) * depth_scale
    gy = sobel(height, axis=0) * depth_scale
    denom = np.sqrt(gx**2 + gy**2 + 1.0)
    nx, ny, nz = gx/denom, gy/denom, 1.0/denom

    az  = math.radians(angle)
    alt = math.radians(altitude)
    lx  =  math.cos(az) * math.cos(alt)
    ly  = -math.sin(az) * math.cos(alt)
    lz  =  math.sin(alt)

    lighting = np.clip(nx*lx + ny*ly + nz*lz, 0.0, 1.0) * alpha

    hi_alpha = np.clip((lighting - 0.5) * 2.0, 0.0, 1.0) * hi_opacity * alpha
    sh_alpha = np.clip((0.5 - lighting) * 2.0, 0.0, 1.0) * sh_opacity * alpha

    hi_rgba = np.empty((h, w, 4), dtype=np.float32)
    hi_rgba[:, :, 0:3] = 1.0
    hi_rgba[:, :, 3]   = hi_alpha

    sh_rgba = np.empty((h, w, 4), dtype=np.float32)
    sh_rgba[:, :, 0:3] = 0.0
    sh_rgba[:, :, 3]   = sh_alpha

    return ((hi_rgba * 255).astype(np.uint8),
            (sh_rgba * 255).astype(np.uint8))

# ---------------------------------------------------------------------------
# Plugin entry
# ---------------------------------------------------------------------------

def apply_bevel_emboss(drawable, config):
    log("started")
    Gegl.init(None)

    size       = int(config['size'])
    soften     = int(config['soften'])
    angle      = float(config['angle'])
    altitude   = float(config['altitude'])
    depth      = int(config['depth'])
    hi_opacity = config['highlight_opacity']
    sh_opacity = config['shadow_opacity']

    image     = drawable.get_image()
    w         = drawable.get_width()
    h         = drawable.get_height()
    _, ox, oy = drawable.get_offsets()
    pos       = image.get_item_position(drawable)

    rgba = buf_to_numpy(drawable.get_buffer(), w, h)
    log("pixels read: %dx%d" % (w, h))

    hi_arr, sh_arr = compute_bevel(rgba, size, soften, angle, altitude, depth,
                                    hi_opacity, sh_opacity)
    log("bevel computed")

    # Highlight layer (Screen) — placed first
    hi_layer = Gimp.Layer.new(image, "bevel-hi", w, h,
                              Gimp.ImageType.RGBA_IMAGE, 100.0,
                              Gimp.LayerMode.SCREEN)
    image.insert_layer(hi_layer, None, pos)
    hi_layer.set_offsets(ox, oy)
    numpy_to_buf(hi_arr, hi_layer.get_buffer(), w, h)
    hi_layer.update(0, 0, w, h)

    # Shadow layer (Multiply) — placed above hi
    sh_layer = Gimp.Layer.new(image, "bevel-sh", w, h,
                              Gimp.ImageType.RGBA_IMAGE, 100.0,
                              Gimp.LayerMode.MULTIPLY)
    image.insert_layer(sh_layer, None, pos)
    sh_layer.set_offsets(ox, oy)
    numpy_to_buf(sh_arr, sh_layer.get_buffer(), w, h)
    sh_layer.update(0, 0, w, h)

    # Merge sh_layer down into hi_layer → single "bevel" layer
    merged = image.merge_down(sh_layer, Gimp.MergeType.EXPAND_AS_NECESSARY)
    merged.set_name("bevel")
    log("merged into single bevel layer")

    Gimp.displays_flush()
    log("done")
