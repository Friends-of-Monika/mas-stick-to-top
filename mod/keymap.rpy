init -100 python in _fom_stt_keymap:
    import store

    def toggle_stick():
        try:
            handle = store._fom_stt_windows.WindowHandle.get_platform_handle()
            handle.set_mas_foreground(not handle.is_on_top)
            if handle.is_on_top:
                renpy.notify(_("The game window is now always on top."))
            else:
                renpy.notify(_("The game window will no longer be always on top."))
        except NotImplementedError:
            renpy.notify(_("Stick to Top is unsupported on this platform."))

    renpy.config.keymap["_fom_stt_toggle_stick"] = ["ctrl_noshift_K_RETURN"]
    renpy.config.underlay.append(renpy.Keymap(_fom_stt_toggle_stick=toggle_stick))
