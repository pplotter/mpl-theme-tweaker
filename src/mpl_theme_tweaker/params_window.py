import os
import platform
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from cycler import cycler
from imgui_bundle import (
    hello_imgui,  # type: ignore
    icons_fontawesome_6,
    imgui,
    imgui_toggle,  # type: ignore
)
from matplotlib.font_manager import _load_fontmanager, fontManager  # type: ignore

from mpl_theme_tweaker.app_state import get_app_key, set_app_key
from mpl_theme_tweaker.app_utils import get_downloads_folder
from mpl_theme_tweaker.mpl_entry.section import (
    AxesSection,
    BoxplotSection,
    FigureSection,
    ImageSection,
    LegendSection,
    LinesSection,
    Section,
    TextSection,
    TicksSection,
)
from mpl_theme_tweaker.translation import _t, set_language

_TABLE_FLAGS = imgui.TableFlags_.borders + imgui.TableFlags_.resizable
_FONT_NAMES = ["None"] + sorted(set(fontManager.get_font_names()))
_TITLE_FONT_ = None


def is_valid_filename(filename: str) -> bool:
    if not filename or filename.strip() == "":
        return False

    if platform.system() == "Windows":
        illegal_chars = {"<", ">", ":", '"', "/", "\\", "|", "?", "*"}
        reserved_names = {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        }
        name_without_ext = Path(filename).stem.upper()
        if name_without_ext in reserved_names:
            return False
        if any(char in illegal_chars for char in filename):
            return False
        if filename.strip()[-1] in (" ", "."):
            return False
    else:
        if "/" in filename or "\0" in filename:
            return False

    try:
        temp_path = Path(os.path.join(os.getenv("TEMP", "/tmp"), filename))
        temp_path.resolve(strict=False)
        return temp_path.name == filename
    except (OSError, ValueError):
        return False


def is_valid_file_path(file_path: str) -> bool:
    if not file_path:
        return False
    try:
        Path(file_path).resolve(strict=False)
        return True
    except (OSError, ValueError, TypeError):
        return False


def _title(title: str) -> None:
    imgui.push_font(_TITLE_FONT_, _TITLE_FONT_.legacy_size)  # type: ignore
    imgui.separator_text(_t(title))
    imgui.pop_font()
    return


def _recache_font() -> None:
    _load_fontmanager(try_read_cache=False)


@dataclass
class Preferences:
    __SUPPORTED_LANGUAGES = {
        "English": "en",
        "中文": "zh_CN",
    }

    trans_callback: Callable[[], None]
    style_name: str = ""
    duplicate_name_policy: Literal["overwrite", "numeric suffix"] = "numeric suffix"
    download_directory: str = ""
    custom_style_directory: str = ""
    target_directory: str = ""
    download_to_target: bool = False
    reset_default_before_apply_new: bool = False
    language: Literal["English", "中文"] = "English"

    def set_language(self, lang: str | None = None) -> None:
        lang = lang or self.language
        if lang not in self.__SUPPORTED_LANGUAGES:
            lang = "English"
        lang_id = self.__SUPPORTED_LANGUAGES[lang]
        set_language(lang_id)
        if hasattr(self, "trans_callback"):
            self.trans_callback()
        return

    def to_dict(self) -> dict[str, Any]:
        return {
            "style_name": self.style_name,
            "duplicate_name_policy": self.duplicate_name_policy,
            "download_directory": self.download_directory,
            "custom_style_directory": self.custom_style_directory,
            "target_directory": self.target_directory,
            "download_to_target": self.download_to_target,
            "reset_default_before_apply_new": self.reset_default_before_apply_new,
            "language": self.language,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        self.style_name = data.get("style_name", "")

        policy = data.get("duplicate_name_policy", "numeric suffix")
        if policy not in ["overwrite", "numeric suffix"]:
            policy = "numeric suffix"
        self.duplicate_name_policy = policy  # type: ignore

        directory = data.get("download_directory", "")
        if directory:
            self.download_directory = directory
        else:
            self.download_directory = get_downloads_folder().as_posix()

        self.custom_style_directory = data.get("custom_style_directory", "")
        self.target_directory = data.get("target_directory", "")
        self.download_to_target = bool(data.get("download_to_target", False))
        self.reset_default_before_apply_new = bool(
            data.get("reset_default_before_apply_new", False)
        )

        language = data.get("language", "English")
        if language not in self.__SUPPORTED_LANGUAGES:
            language = "English"
        self.language = language

        return

    def get_write_path(self) -> Path:
        filename = self.style_name if self.style_name else "matplotlibrc"

        if self.download_to_target:
            return Path(self.target_directory) / filename
        else:
            return Path(self.download_directory) / filename

    def gui(self) -> None:
        global _TITLE_FONT_
        if _TITLE_FONT_ is None:
            _TITLE_FONT_ = get_app_key("title_font")

        _title("Style Name")
        _, style_name = imgui.input_text_with_hint(
            _t("Style Name"), "matplotlibrc", self.style_name
        )
        if is_valid_filename(style_name):
            self.style_name = style_name

        _title("Duplicate name policy")
        if imgui.radio_button(
            _t("Ovewrite"), self.duplicate_name_policy == "overwrite"
        ):
            self.duplicate_name_policy = "overwrite"
        imgui.same_line()
        if imgui.radio_button(
            _t("Numeric suffix"), self.duplicate_name_policy == "numeric suffix"
        ):
            self.duplicate_name_policy = "numeric suffix"

        _title("Default Directory")
        _, self.download_directory = imgui.input_text_with_hint(
            _t("Download"),
            "C:\\Users\\username\\Downloads",
            self.download_directory,
        )

        changed, custom_style_directory = imgui.input_text_with_hint(
            _t("Custom Style"),
            "C:\\Users\\username\\Documents\\matplotlib\\style",
            self.custom_style_directory,
        )
        if changed:
            if Path(custom_style_directory).is_dir():
                self.custom_style_directory = custom_style_directory
                _func = get_app_key("StyleManager.set_path")
                _func(custom_style_directory)
                hello_imgui.log(
                    hello_imgui.LogLevel.info,
                    f"Custom style directory set to {custom_style_directory}.",
                )
            else:
                hello_imgui.log(
                    hello_imgui.LogLevel.error,
                    f"`{custom_style_directory}` is not a directory.",
                )

            # self.custom_style_directory = custom_style_directory

        _, self.target_directory = imgui.input_text_with_hint(
            _t("Target"),
            "C:\\Users\\username\\Desktop\\workspace",
            self.target_directory,
        )
        toggle_config = imgui_toggle.ios_style(size_scale=0.2)
        _, self.download_to_target = imgui_toggle.toggle(
            _t("Download to Target"),
            self.download_to_target,
            config=toggle_config,
        )

        _title("Misc")
        toggle_config = imgui_toggle.ios_style(size_scale=0.2)
        _, self.reset_default_before_apply_new = imgui_toggle.toggle(
            _t("Reset Default Before Apply New Style"),
            self.reset_default_before_apply_new,
            config=toggle_config,
        )

        if not hasattr(self, "languages"):
            self.languages = list(Preferences.__SUPPORTED_LANGUAGES.keys())
        lang_idx = self.languages.index(self.language)
        changed, lang_idx = imgui.combo(_t("Language"), lang_idx, self.languages)
        if changed:
            self.language = self.languages[lang_idx]  # type: ignore
            self.set_language(self.language)

        return


@dataclass
class _Font:
    index: int = 0
    name: str = "None"


@dataclass
class _FontFamilyManager:
    family_names: list[str] = field(
        default_factory=lambda: [
            "serif",
            "sans-serif",
            "cursive",
            "fantasy",
            "monospace",
        ]
    )
    N: int = 5
    fonts: dict[str, list[_Font]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        for family in self.family_names:
            self.fonts[family] = [_Font() for _ in range(self.N)]

    def to_str(self) -> str:
        texts = ["## Font"]
        for family_name, fonts in self.fonts.items():
            font_family_name = f"font.{family_name}:"
            text = f"{font_family_name:<18} "
            text += ", ".join([font.name for font in fonts if font.name != "None"])
            texts.append(text)

        return "\n".join(texts)

    def gui(self) -> None:
        if imgui.begin_table("Font", 5, _TABLE_FLAGS):
            imgui.table_headers_row()

            title_font = get_app_key("title_font")
            imgui.push_font(title_font, title_font.legacy_size)
            for j, family_name in enumerate(self.family_names):
                imgui.table_set_column_index(j)
                imgui.text(family_name)
            imgui.pop_font()

            for i in range(self.N):
                imgui.table_next_row()
                for j, family_name in enumerate(self.family_names):
                    imgui.table_set_column_index(j)
                    current_font = self.fonts[family_name][i]

                    imgui.push_item_width(-1)
                    changed, new_index = imgui.combo(
                        f"##font_{i}_{j}", current_font.index, _FONT_NAMES
                    )
                    if changed:
                        current_font.index = new_index
                        current_font.name = _FONT_NAMES[new_index]
                    imgui.pop_item_width()

            imgui.end_table()

        if imgui.button("Apply##font", [-1, 0]):
            self.apply()
        return

    def apply(self) -> None:
        for key, fonts in self.fonts.items():
            font_names = [font.name for font in fonts if font.name != "None"]
            plt.rcParams[f"font.{key}"] = font_names

        replot_func = get_app_key("FigureWidow.replot_func")
        if replot_func is not None:
            replot_func()
        return

    def reset_by_rcParams(self) -> None:
        for family_name in self.family_names:
            font_names = plt.rcParams[f"font.{family_name}"]
            row = 0
            for _, font_name in enumerate(font_names):
                if row >= self.N:
                    break
                if font_name in _FONT_NAMES:
                    index = _FONT_NAMES.index(font_name)
                    self.fonts[family_name][row].index = index
                    self.fonts[family_name][row].name = font_name
                    row += 1
        return


class _ColorCycleManager:
    def __init__(self):
        self.N = 10
        self.colors: list[list[float]] = [[1.0, 1.0, 1.0, 1.0]] * self.N

    def to_str(self) -> str:
        color_hex = [mcolors.to_hex(color, keep_alpha=True) for color in self.colors]  # type: ignore
        color_cycler = cycler(color=color_hex)
        return f"## Color Cycle\naxes.prop_cycle:{str(color_cycler)}"

    def gui(self) -> None:
        if imgui.begin_table("Color", 2, _TABLE_FLAGS):
            imgui.table_headers_row()
            title_font = get_app_key("title_font")
            imgui.push_font(title_font, title_font.legacy_size)
            imgui.table_set_column_index(0)
            imgui.text("Index")
            imgui.table_set_column_index(1)
            imgui.text("Color")
            imgui.pop_font()

            for i in range(self.N):
                imgui.table_next_row()

                imgui.table_set_column_index(0)
                imgui.text(f"C{i}")

                imgui.table_set_column_index(1)
                changed, new_color = imgui.color_edit4(
                    f"##color_{i}",
                    self.colors[i],
                    imgui.ColorEditFlags_.default_options_,
                )
                if changed:
                    self.colors[i] = list(new_color)

            imgui.end_table()
        if imgui.button("Apply##color_cycle", [-1, 0]):
            self.apply()
        return

    def apply(self) -> None:
        color_hex = [mcolors.to_hex(color, keep_alpha=True) for color in self.colors]  # type: ignore
        color_cycler = cycler(color=color_hex)
        plt.rcParams["axes.prop_cycle"] = color_cycler

        replot_func = get_app_key("FigureWidow.replot_func")
        if replot_func is not None:
            replot_func()
        return

    def reset_by_rcParams(self) -> None:
        cycler = plt.rcParams["axes.prop_cycle"]
        if "color" not in cycler.by_key():
            return

        colors = cycler.by_key()["color"]
        for i, color in enumerate(colors):
            if i >= self.N:
                break
            self.colors[i] = list(mcolors.to_rgba(color))
        return


class ParamsWindow:
    def __init__(self, callback: Callable):
        self.callback: Callable = callback
        self.font_family_manager = _FontFamilyManager()
        self.color_cycle_manager = _ColorCycleManager()
        self.preferences = Preferences(self.trans_label)

        self.sections: list[Section] = [
            FigureSection(),
            AxesSection(),
            TicksSection(),
            LinesSection(),
            LegendSection(),
            TextSection(),
            BoxplotSection(),
            ImageSection(),
        ]

        self.reset_by_default(call_callback=False)
        set_app_key("ParamsWindow.reset_by_rcParams", self.reset_by_rcParams)

    def gui(self) -> None:
        font_cn = get_app_key("cn_font")
        imgui.push_font(font_cn, font_cn.legacy_size)

        if imgui.begin_tab_bar("RcParams"):
            if imgui.begin_tab_item(_t("Preferences"))[0]:
                self.preferences.gui()
                imgui.end_tab_item()

            for section in self.sections:
                sec_name = _t(section.get_name())
                if imgui.begin_tab_item(sec_name)[0]:
                    section.gui()
                    imgui.end_tab_item()

            if imgui.begin_tab_item(_t("List"))[0]:
                _title("Font")
                self.font_family_manager.gui()
                _title("Color")
                self.color_cycle_manager.gui()
                imgui.end_tab_item()
            imgui.end_tab_bar()

        imgui.pop_font()
        self.update_check()
        return

    def update_check(self):
        need_update = [section.need_update() for section in self.sections]
        if any(need_update):
            self.callback()
            for section in self.sections:
                section.update()
        return

    def reset_by_rcParams(self, call_callback: bool = True) -> None:
        for section in self.sections:
            section.reset_by_rcParams()

        self.font_family_manager.reset_by_rcParams()
        self.color_cycle_manager.reset_by_rcParams()

        if call_callback:
            self.callback()
        return

    def reset_by_default(self, call_callback: bool = True) -> None:
        plt.style.use("default")
        self.reset_by_rcParams(call_callback)
        return

    def reset_by_style(self, style_name: str) -> None:
        if self.preferences.reset_default_before_apply_new:
            plt.style.use("default")
        plt.style.use(style_name)
        self.reset_by_rcParams()
        return

    def save2matplotlibrc(self, filepath: str) -> None:
        hello_imgui.log(hello_imgui.LogLevel.info, "# Not Implemented Yet")
        return

    def get_style_str(self) -> str:
        text = "## written by mpl-theme-tweaker, version 0.1.0\n"
        for section in self.sections:
            text += section.to_str() + "\n\n"

        text += "\n\n" + self.font_family_manager.to_str()
        text += "\n\n" + self.color_cycle_manager.to_str()
        return text

    def gui_app_menu(self) -> None:
        # imgui.menu_item(f"{icons_fontawesome_6.ICON_FA_FILE} Load", "", False)
        # imgui.separator()
        # ======================== Save =====================
        # save_clicked, _ = imgui.menu_item(
        #     f"{icons_fontawesome_6.ICON_FA_FLOPPY_DISK} Save", "", False
        # )
        # # ====================== Save As ====================
        # saveas_clicked, _ = imgui.menu_item(
        #     f"{icons_fontawesome_6.ICON_FA_FILE_EXPORT} Save As", "", False
        # )
        # ===================== Download ====================
        download_clicked, _ = imgui.menu_item(
            f"{icons_fontawesome_6.ICON_FA_FILE_ARROW_DOWN} Download", "", False
        )
        if download_clicked:
            filepath = self.preferences.get_write_path()
            directory = filepath.parent
            if not directory.exists():
                hello_imgui.log(
                    hello_imgui.LogLevel.error,
                    f"Downloads folder ``{directory}`` does not exist",
                )
                return

            if (
                filepath.exists()
                and self.preferences.duplicate_name_policy == "numeric suffix"
            ):
                n = 1
                while True:
                    new_filepath = filepath.with_name(
                        f"{filepath.stem}({n}){filepath.suffix}"
                    )
                    if not new_filepath.exists():
                        filepath = new_filepath
                        break
                    n += 1
            style_str = self.get_style_str()
            filepath.write_text(style_str)
            hello_imgui.log(hello_imgui.LogLevel.info, f"Style saved to ``{filepath}``")

        # ================ Copy to Clipboard ================
        copy_clicked, _ = imgui.menu_item(
            f"{icons_fontawesome_6.ICON_FA_COPY} Copy to Clipboard", "", False
        )
        if copy_clicked:
            style_str = self.get_style_str()
            imgui.set_clipboard_text(style_str)

        imgui.separator()
        # ================== Recache Font ==================
        recache_font_clicked, _ = imgui.menu_item(
            f"{icons_fontawesome_6.ICON_FA_FONT} Recache Font", "", False
        )
        if recache_font_clicked:
            threading.Thread(target=_recache_font, daemon=True).start()
        # shortcut must be put in main loop or gui always show
        # if imgui.is_key_chord_pressed(imgui.Key.mod_ctrl | imgui.Key.s):
        #     print("Ctrl + S pressed")

        # clicked, _ = imgui.menu_item("A Custom app menu item", "", False)
        # if clicked:
        #     print("Clicked on A Custom app menu item")
        #     hello_imgui.log(
        #         hello_imgui.LogLevel.info, "Clicked on A Custom app menu item"
        #     )
        return

    def get_app_settings(self) -> dict[str, Any]:
        return self.preferences.to_dict()

    def load_app_settings(self, settings: dict) -> None:
        self.preferences.from_dict(settings)
        self.preferences.set_language()
        self.trans_label()
        return

    def trans_label(self) -> None:
        for section in self.sections:
            section.trans_label()
        return
