default persistent._fom_stt_config = None

init -1 python:
    if persistent._fom_stt_config is None:
        persistent._fom_stt_config = {
            "stick_on_startup": False
        }

screen fom_stt_settings():
    $ tooltip_disp = renpy.get_screen("submods", "screens").scope["tooltip"]

    python:
        try:
            handle = store._fom_stt_windows.WindowHandle.get_platform_handle()
            is_implemented = True
        except NotImplementedError:
            handle = None
            is_implemented = False

    vbox:
        style_prefix "check"
        xmaximum 800
        xfill True

        if is_implemented:
            text _("Stick to Top is {color=#84cc16}available{/color} on your system.")
        else:
            text _("Stick to Top is {color=#ef4444}not available{/color} on your system. {a=https://github.com/friends-of-monika/mas-stick-to-top?tab=readme-ov-file#-how-do-i-use-it}Why?{/a}")

        hbox spacing 10:
            textbutton _("Stick to top"):
                hovered SetField(tooltip_disp, "value", _("Click to stick/unstick window to foreground."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)

                if is_implemented:
                    action Function(handle.set_mas_foreground, not handle.is_on_top)

                selected is_implemented and handle.is_on_top
                sensitive is_implemented

            textbutton _("Apply on startup"):
                hovered SetField(tooltip_disp, "value", _("Click to stick window to foreground on every startup."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)

                action ToggleDict(persistent._fom_stt_config, "stick_on_startup")
                selected persistent._fom_stt_config["stick_on_startup"]
                sensitive is_implemented
