import os
from importlib.resources import files  # noqa: F401
from pathlib import Path

import glfw
from imgui_bundle import glfw_utils, hello_imgui, imgui  # type: ignore
from PIL import Image

from mpl_theme_tweaker.app_state import set_app_key

glfw.init()


def rootPath() -> Path:
    return Path(files("mpl_theme_tweaker"))  # type: ignore


def assetsPath() -> Path:
    return rootPath() / "assets"


def projectPath() -> Path:
    return (rootPath() / "../..").resolve()


def set_window_icon() -> None:
    # get the main glfw window used by HelloImGui
    win = glfw_utils.glfw_window_hello_imgui()

    path = assetsPath() / "mpl-theme-tweaker.png"
    img = Image.open(path)
    imgs = [img]
    glfw.set_window_icon(win, 1, imgs)
    return


def setup_theme() -> None:
    # Apply default style
    hello_imgui.imgui_default_settings.setup_default_imgui_style()

    # Create a tweaked theme
    tweaked_theme = hello_imgui.ImGuiTweakedTheme()
    tweaked_theme.theme = hello_imgui.ImGuiTheme_.microsoft_style
    hello_imgui.apply_tweaked_theme(tweaked_theme)
    return


def load_fonts() -> None:
    hello_imgui.get_runner_params().callbacks.default_icon_font = (
        hello_imgui.DefaultIconFont.font_awesome6
    )
    hello_imgui.imgui_default_settings.load_default_font_with_font_awesome_icons()

    # title_font = hello_imgui.load_font_ttf_with_font_awesome_icons(
    #     "fonts/Roboto/Roboto-BoldItalic.ttf", 18
    # )

    # see issus196 https://github.com/pthom/imgui_bundle/issues/196
    title_font = hello_imgui.load_font_ttf_with_font_awesome_icons(
        "fonts/NotoSansSC-SemiBold.ttf", 24
    )
    set_app_key("title_font", title_font)

    font_loading_params = hello_imgui.FontLoadingParams()
    font_cn = hello_imgui.load_font(
        "fonts/NotoSansSC-Regular.ttf", 18.0, font_loading_params
    )
    set_app_key("cn_font", font_cn)
    return


def get_downloads_folder() -> Path:
    """跨平台获取用户的 Downloads 目录"""
    if os.name == "nt":  # Windows
        import winreg

        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                return Path(winreg.QueryValueEx(key, downloads_guid)[0])
        except Exception:
            # 回退到默认位置
            return Path.home() / "Downloads"
    else:  # macOS 和 Linux
        return Path.home() / "Downloads"


if __name__ == "__main__":
    print(get_downloads_folder())
