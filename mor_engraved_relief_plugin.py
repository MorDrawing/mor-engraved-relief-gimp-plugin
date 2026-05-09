#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
#
# Mor Engraved Relief — GIMP 3.2 layer-style plug-in
# Copyright (C) 2026 Moribund Institute
#
# Algorithm derived from Krita's kis_ls_bevel_emboss_filter.cpp
# Copyright (C) 2014 Dmitry Kazakov
# and the LayerFX GIMP plugin (2008) by Jonathan Stipe.

import gi
import os
import sys
import traceback

gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gegl', '0.4')
from gi.repository import Gimp, GimpUi, GObject, GLib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LOG = os.path.expanduser("~/.config/GIMP/3.2/mor_engraved_relief_debug.log")


def log(msg):
    with open(LOG, "a") as f:
        f.write(msg + "\n")


from ls_engine import apply_bevel_emboss


class MorEngravedReliefPlugin(Gimp.PlugIn):
    def do_set_i18n(self, name):
        return False, None, None

    def do_query_procedures(self):
        return ["python-fu-mor-engraved-relief"]

    def do_create_procedure(self, name):
        proc = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self._run)
        proc.set_image_types("*")
        proc.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE)
        proc.set_menu_label("Mor Engraved Relief...")
        proc.add_menu_path("<Image>/Filters/Layer Styles")
        proc.set_documentation(
            "Mor Engraved Relief",
            "Smooth raised-relief / engraved bevel effect for GIMP.",
            name
        )
        proc.set_attribution(
            "Moribund Institute / Krita and LayerFX-derived Python port",
            "GPL-2.0-or-later",
            "2026"
        )
        proc.add_int_argument("size", "Size", "Bevel radius in pixels", 1, 100, 21, GObject.ParamFlags.READWRITE)
        proc.add_int_argument("soften", "Soften", "Edge softness", 0, 100, 0, GObject.ParamFlags.READWRITE)
        proc.add_int_argument("depth", "Depth (%)", "Bump intensity", 1, 100, 100, GObject.ParamFlags.READWRITE)
        proc.add_double_argument("angle", "Angle", "Light azimuth degrees", 0.0, 360.0, 120.0, GObject.ParamFlags.READWRITE)
        proc.add_double_argument("altitude", "Altitude", "Light elevation degrees", 0.0, 90.0, 30.0, GObject.ParamFlags.READWRITE)
        proc.add_double_argument("highlight_opacity", "Highlight Opacity", "Screen pass opacity 0-1", 0.0, 1.0, 0.75, GObject.ParamFlags.READWRITE)
        proc.add_double_argument("shadow_opacity", "Shadow Opacity", "Multiply pass opacity 0-1", 0.0, 1.0, 0.75, GObject.ParamFlags.READWRITE)
        return proc

    def _run(self, procedure, run_mode, image, drawables, config, run_data=None):
        log("_run called")
        if run_mode == Gimp.RunMode.INTERACTIVE:
            GimpUi.init("python-fu-mor-engraved-relief")
            dialog = GimpUi.ProcedureDialog.new(procedure, config, "Mor Engraved Relief")
            dialog.fill(["size", "soften", "depth", "angle", "altitude", "highlight_opacity", "shadow_opacity"])
            if not dialog.run():
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, GLib.Error())
            dialog.destroy()

        if len(drawables) != 1:
            return procedure.new_return_values(
                Gimp.PDBStatusType.CALLING_ERROR,
                GLib.Error("Requires exactly one drawable.")
            )

        drawable = drawables[0]
        cfg = {
            "size":              config.get_property("size"),
            "soften":            config.get_property("soften"),
            "depth":             config.get_property("depth"),
            "angle":             config.get_property("angle"),
            "altitude":          config.get_property("altitude"),
            "highlight_opacity": config.get_property("highlight_opacity"),
            "shadow_opacity":    config.get_property("shadow_opacity"),
        }

        log(f"config: {cfg}")
        image.undo_group_start()

        try:
            apply_bevel_emboss(drawable, cfg)
            log("apply_bevel_emboss completed OK")
        except Exception as e:
            image.undo_group_end()
            log("FAILED: " + traceback.format_exc())
            return procedure.new_return_values(Gimp.PDBStatusType.EXECUTION_ERROR, GLib.Error(str(e)))

        image.undo_group_end()
        Gimp.displays_flush()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


Gimp.main(MorEngravedReliefPlugin.__gtype__, sys.argv)
