init 100 python in _fom_stt_windows:
    from store.mas_submod_utils import functionplugin, submod_log
    from store import persistent

    class WindowHandle(object):
        SINGLETON = None

        def __init__(self):
            self.is_on_top = False

        @classmethod
        def get_platform_handle(cls):
            if cls.SINGLETON is None:
                submod_log.debug("[Stick to Top] [WindowHandle] Getting platform-specific WindowHandle implementation.")
                if renpy.windows:
                    submod_log.debug("[Stick to Top] [WindowHandle] Using WindowsWindowHandle.")
                    cls.SINGLETON = WindowsWindowHandle()

            if cls.SINGLETON is None:
                submod_log.debug("[Stick to Top] [WindowHandle] No supported implementations.")
                raise NotImplementedError()

            return cls.SINGLETON

        def set_mas_foreground(self, stick):
            raise NotImplementedError()

    class WindowsWindowHandle(WindowHandle):
        def __init__(self):
            super(WindowsWindowHandle, self).__init__()

        def set_mas_foreground(self, stick):
            HWND_TOPMOST   = -1
            HWND_NOTOPMOST = -2

            if stick:
                submod_log.info("[Stick to Top] [WindowsWindowHandle] Setting MAS window as always on the foreground.")
                insert_hwnd = HWND_TOPMOST
            else:
                submod_log.info("[Stick to Top] [WindowsWindowHandle] Unsetting MAS window as always on the foreground.")
                insert_hwnd = HWND_NOTOPMOST

            win_hwnd = self.get_mas_window_hwnd()
            self.set_user32_window_hwnd(win_hwnd, insert_hwnd)
            self.is_on_top = stick

        def set_user32_window_hwnd(self, win_hwnd, insert_hwnd):
            from ctypes import wintypes
            import ctypes

            SWP_NOMOVE     = 0x0002 # Do not move existing window
            SWP_NOSIZE     = 0x0001 # Do not resize existing window
            SWP_NOACTIVATE = 0x0010 # Do not focus

            user32 = ctypes.WinDLL("user32", use_last_error=True)
            user32.SetWindowPos.argtypes = [
                wintypes.HWND, # Window handle
                wintypes.HWND, # Handle to insert after
                wintypes.INT,  # X position
                wintypes.INT,  # Y position
                wintypes.INT,  # Width
                wintypes.INT,  # Height
                wintypes.UINT  # Flags
            ]

            user32.SetWindowPos.restype = wintypes.BOOL
            if not user32.SetWindowPos(win_hwnd, insert_hwnd, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE):
                raise ctypes.WinError(ctypes.get_last_error())

        def get_mas_window_hwnd(self):
            from store import mas_windowutils
            getMASWindowHWND = get_mangled(mas_windowutils, "getMASWindowHWND")
            return getMASWindowHWND()

    def get_mangled(module, name):
        for k, v in module.__dict__.items():
            if k.endswith("__" + name):
                return v
        raise KeyError(name)

init 101 python in _fom_stt_windows:
    @functionplugin("ch30_preloop")
    def on_startup():
        def on_startup_task():
            try:
                if persistent._fom_stt_config["stick_on_startup"]:
                    handle = WindowHandle.get_platform_handle()
                    handle.set_mas_foreground(True)
            except Exception as e:
                submod_log.error("[Stick to Top] [ch30_preloop] Failed to apply on startup.")
                submod_log.error(repr(e))

        submod_log.debug("[Stick to Top] [ch30_preloop] Deferring ch30_preloop task by 1 second.")
        renpy.show_screen("fom_stt_windows_timer", 1.0, on_startup_task)

screen fom_stt_windows_timer(delay, func, *args, **kwargs):
    timer delay action [Function(func, *args, **kwargs), Hide("fom_stt_windows_timer")]
