init -990 python:
    store.mas_submod_utils.Submod(
        author="Friends of Monika",
        name="Stick to Top",
        description=_("A small submod that allows you to stick Monika After Story to top, over any other windows.\n"
                      "Inspired by GeneTechnician's AutoHotkey tutorial."),
        version="1.0.0",
        settings_pane="fom_stt_settings"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Stick to Top",
            user_name="friends-of-monika",
            repository_name="mas-stick-to-top",
            extraction_depth=2
        )
