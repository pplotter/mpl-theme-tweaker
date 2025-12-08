from abc import ABC
from typing import Any

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from imgui_bundle import hello_imgui, imgui, imgui_toggle  # type: ignore

from mpl_theme_tweaker.app_state import get_app_key
from mpl_theme_tweaker.app_utils import assetsPath
from mpl_theme_tweaker.image_combo import ImageCombo, ImageComboOption, load_images
from mpl_theme_tweaker.translation import _t


class Entry(ABC):
    value: Any
    label: str
    key: str
    updated: bool

    def __init__(self, key: str, sameline: bool = False):
        self.key: str = key
        self.updated: bool = False
        self.sameline: bool = sameline
        self.label = f"{_t(self.key)}##{self.key}"

    def gui(self) -> None:
        if self.sameline:
            imgui.same_line()
        return

    def update_mpl_rcparams(self, value) -> None:
        plt.rcParams[self.key] = value
        self.value = value

        self.updated = True
        return

    def update(self) -> None:
        self.updated = False
        return

    def need_update(self) -> bool:
        return self.updated

    def reset_by_rcParams(self) -> None:
        self.value = plt.rcParams[self.key]
        return

    def __repr__(self) -> str:
        return f"{self.label}: {self.value}"

    def to_str(self) -> str:
        return f"{self.key}: {self.value}"

    def trans_label(self) -> None:
        self.label = f"{_t(self.key)}##{self.key}"
        return


class SeparatorEntry(Entry):
    def __init__(self, label: str):
        super().__init__(label)

        self.value = None

    def gui(self) -> None:
        title_font = get_app_key("title_font")
        imgui.push_font(title_font, title_font.legacy_size)
        imgui.separator_text(self.label)
        imgui.pop_font()
        return

    def update_mpl_rcparams(self, value) -> None:
        pass

    def reset_by_rcParams(self) -> None:
        pass

    def to_str(self) -> str:
        return ""


class BoolEntry(Entry):
    def __init__(self, key: str, value: bool = False, sameline: bool = False):
        super().__init__(key, sameline)
        self.value = value

    def gui(self) -> None:
        super().gui()

        # changed, new_value = imgui.checkbox(self.label, self.value)
        toggle_config = imgui_toggle.ios_style(size_scale=0.2)
        changed, new_value = imgui_toggle.toggle(
            self.label, self.value, config=toggle_config
        )
        if changed and new_value != self.value:
            self.update_mpl_rcparams(new_value)
        return


class IntEntry(Entry):
    """
    dict info should like:
    {
        "value": 0,
        "vmin": 0,
        "vmax": 100,
        "step": 1,
        "stepfast": 10,
    }
    """

    def __init__(
        self,
        key: str,
        info: dict[str, Any],
        sameline: bool = False,
    ):
        super().__init__(key, sameline)

        self.value = info.get("value", 0)
        self.vmin = info.get("vmin")
        self.vmax = info.get("vmax")
        self.step = info.get("step", 1)
        self.stepfast = info.get("stepfast", self.step)

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.input_int(
            self.label, self.value, self.step, self.stepfast
        )

        if changed:
            if not (self.vmin is None or self.vmax is None):
                new_value = max(self.vmin, min(new_value, self.vmax))

            if new_value != self.value:
                self.update_mpl_rcparams(new_value)

        return


class FloatEntry(Entry):
    """
    dict info should like:
    {
        "value": 0.0,
        "vmin": 0.0,
        "vmax": 100.0,
        "step": 1.0,
        "stepfast": 10.0,
        "format": "%.3f",
    }
    """

    def __init__(
        self,
        key: str,
        info: dict[str, Any],
        sameline: bool = False,
    ):
        super().__init__(key, sameline)

        self.value = info.get("value", 0.0)
        self.vmin = info.get("vmin")
        self.vmax = info.get("vmax")
        self.step = info.get("step", 1.0)
        self.stepfast = info.get("stepfast", self.step)
        self.format = info.get("format", "%.3f")

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.input_float(
            self.label,
            self.value,
            self.step,
            self.stepfast,
            self.format,
        )
        if changed:
            if not (self.vmin is None or self.vmax is None):
                new_value = max(self.vmin, min(new_value, self.vmax))

            if new_value != self.value:
                self.update_mpl_rcparams(new_value)
        return

    def reset_by_rcParams(self) -> None:
        value = plt.rcParams[self.key]
        if isinstance(value, float):
            self.value = value
        return

    def to_str(self) -> str:
        return f"{self.key}: {self.value:.4f}"


class Float2Entry(Entry):
    """
    dict info should like:
    {
        "value": [0.0, 0.0],
        "vmin": 0.0,
        "vmax": 100.0,
        "format": "%.3f",
    }
    """

    def __init__(
        self,
        key: str,
        info: dict[str, Any],
        sameline: bool = False,
    ):
        super().__init__(key, sameline)

        self.value = info.get("value", 0.0)
        self.vmin = info.get("vmin")
        self.vmax = info.get("vmax")
        self.format = info.get("format", "%.3f")

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.input_float2(self.label, self.value, self.format)
        if changed:
            if not (self.vmin is None or self.vmax is None):
                new_value = max(self.vmin, min(new_value, self.vmax))

            if new_value != self.value:
                self.update_mpl_rcparams(new_value)
        return

    def reset_by_rcParams(self) -> None:
        value = plt.rcParams[self.key]
        if isinstance(value, list) and len(value) == 2:
            try:
                value = [float(v) for v in value]
            except ValueError:
                return
            self.value = value
        return

    def to_str(self) -> str:
        return f"{self.key}: {self.value[0]:.4f}, {self.value[1]:.4f}"


class Float4Entry(Entry):
    pass


class StrEntry(Entry):
    """
    dict info should like:
    {
        "value": 0,
        "items": ["AA", "BB", "CC", "DD"],
    }
    """

    def __init__(self, key: str, info: dict[str, Any]):
        super().__init__(key)
        self.value = info.get("value", 0)
        self.items: list[str] = info.get("items", [])

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.combo(self.label, self.value, self.items)
        if changed and new_value != self.value:
            self.update_mpl_rcparams(new_value)
        return

    def update_mpl_rcparams(self, value) -> None:
        self.value = value
        plt.rcParams[self.key] = self.items[self.value]

        self.updated = True
        return

    def reset_by_rcParams(self) -> None:
        value = plt.rcParams[self.key]
        if self.key == "font.family":
            value = value[0] if value else value

        if value in self.items:
            self.value = self.items.index(value)
        return

    def to_str(self) -> str:
        return f'{self.key}: "{self.items[self.value]}"'


class MarkerStyleEntry(Entry):
    """
    dict info should like:
    {
        "value": 0,
        "items": ["AA", "BB", "CC", "DD"],
    }
    """

    def __init__(self, key: str):
        super().__init__(key)
        self.value = "none"

        marker_dir = assetsPath() / "marker"
        marker: dict[str, str] = {
            "none": "none",
            "point": ".",
            "circle": "o",
            "triangle_up": "^",
            "triangle_down": "v",
            "triangle_right": ">",
            "triangle_left": "<",
            "octagon": "8",
            "square": "s",
            "pentagon": "p",
            "plus": "P",
            "star": "*",
            "hexagon1": "h",
            "hexagon2": "H",
            "x": "X",
            "diamond": "D",
            "thin_diamond": "d",
            "pixel": ",",
            "plus_unfilled": "+",
            "x_unfilled": "x",
            "tri_down": "1",
            "tri_up": "2",
            "tri_left": "3",
            "tri_right": "4",
            "vline": "|",
            "hline": "_",
        }
        marker_names = list(marker.keys())
        marker_values = list(marker.values())
        marker_labels = [f"{key} ('{value}')" for key, value in marker.items()]
        marker_img_paths = [marker_dir / f"{name}.png" for name in marker_names]

        marker_images = load_images(marker_img_paths)
        marker_options = [
            ImageComboOption(img, label, value)
            for img, label, value in zip(marker_images, marker_labels, marker_values)
        ]

        self.image_combo = ImageCombo(marker_options)

    def gui(self) -> None:
        super().gui()

        state_changed = self.image_combo.gui("Marker")
        if state_changed:
            new_value = self.image_combo.get_value()
            if new_value != self.value:
                self.update_mpl_rcparams(new_value)
        return

    def update_mpl_rcparams(self, value) -> None:
        self.value = value
        plt.rcParams[self.key] = value

        self.updated = True
        return

    def reset_by_rcParams(self) -> None:
        value = plt.rcParams[self.key]

        if value in self.image_combo.values:
            self.value = value
            idx = self.image_combo.values.index(value)
            self.image_combo.set_index(idx)
        else:
            self.image_combo.set_index(None)

        return

    def to_str(self) -> str:
        return f'{self.key}: "{self.value}"'


class ColorEntry(Entry):
    """
    dict info should like:
    {
        "value": [1,1,1,1],
    }
    """

    def __init__(
        self,
        key: str,
        info: dict[str, Any] | None = None,
        sameline: bool = False,
    ):
        super().__init__(key, sameline)
        self.value = info.get("value", [1, 1, 1, 1]) if info else [1, 1, 1, 1]

        self.color_flags = imgui.ColorEditFlags_.no_inputs.value
        # imgui.ColorEditFlags_.no_label.value

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.color_edit4(
            self.label, self.value, flags=self.color_flags
        )
        if changed:
            delta = [abs(new - old) for new, old in zip(new_value, self.value)]
            if any(d > 0.0005 for d in delta):
                self.update_mpl_rcparams(new_value)

        return

    def reset_by_rcParams(self) -> None:
        value = plt.rcParams[self.key]

        # handle "auto" and "inherit" cases
        if value == "auto":  # maybe need recover to default value
            if self.key in ["lines.markerfacecolor", "lines.markeredgecolor"]:
                value = plt.rcParams["lines.color"]
            elif self.key == "axes.titlecolor":
                value = plt.rcParams["text.color"]
        elif value == "inherit":
            if self.key == "xtick.labelcolor":
                value = plt.rcParams["xtick.color"]
            elif self.key == "ytick.labelcolor":
                value = plt.rcParams["ytick.color"]
            elif self.key == "legend.facecolor":
                value = plt.rcParams["axes.facecolor"]

        try:
            rgba = mcolors.to_rgba(value)
        except ValueError:
            hello_imgui.log(
                hello_imgui.LogLevel.info,
                f"Invalid color value for {self.key}: {value}, use white instead.",
            )
            rgba = (1.0, 1.0, 1.0, 1.0)
            return

        self.value = rgba
        return

    def to_str(self) -> str:
        return f'{self.key}: "{mcolors.to_hex(self.value)}"'
