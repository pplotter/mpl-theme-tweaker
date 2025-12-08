"""
让其动态化加载
    1. 可以使用imgui的log
    2. 可以动态切换语言

注意: 要附加中文字体
"""

__all__ = ["_t", "set_language"]

import gettext

from imgui_bundle import hello_imgui

from mpl_theme_tweaker.app_utils import assetsPath

locale_path = assetsPath() / "locale"
_T = gettext.gettext


def set_language(lang: str) -> None:
    global _T
    try:
        trans = gettext.translation("messages", locale_path, [lang])
        _T = trans.gettext
        hello_imgui.log(hello_imgui.LogLevel.info, f"Language <{lang}> load succeed")
    except FileNotFoundError:
        hello_imgui.log(
            hello_imgui.LogLevel.error,
            f"Language <{lang}> load failed, use English instead.",
        )
        _T = gettext.gettext
    return


def _t(msg: str) -> str:
    return _T(msg)
