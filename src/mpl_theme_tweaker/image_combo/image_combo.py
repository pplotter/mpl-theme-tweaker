import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from imgui_bundle import imgui
from PIL import Image

from mpl_theme_tweaker.opengl import create_texture_from_image


def load_images(img_paths: list[Path] | str) -> list[Image.Image]:
    images = []
    for img_path in img_paths:
        if isinstance(img_path, str):
            img_path = Path(img_path)
        if img_path.is_file():
            image = Image.open(img_path).convert("RGBA")
            images.append(image)
        else:
            warnings.warn(
                f"Image `{img_path}` does not exist.", UserWarning, stacklevel=2
            )
    return images


@dataclass
class ImageComboOption:
    image: Image.Image
    label: str
    value: Any


class ImageCombo:
    # texture_ids: list[imgui.ImTextureID]
    texture_refs: list[imgui.ImTextureRef]

    def __init__(
        self,
        options: list[ImageComboOption],
        preview_label: str = "",
        preview_value: Any | None = None,
    ) -> None:
        self.options = options
        self.values = [option.value for option in options]
        self.labels = [option.label for option in options]
        self.images = [option.image for option in options]

        self.preview_label = preview_label
        self.preview_value = preview_value

        self.index: int | None = None

    @classmethod
    def _from(
        cls,
        values: list[Any],
        labels: list[str],
        images: list[Image.Image],
        preview_label: str = "",
        preview_value: Any | None = None,
    ) -> "ImageCombo":
        assert len(values) == len(labels) == len(images)

        options = []
        for value, label, image in zip(values, labels, images):
            options.append(ImageComboOption(image, label, value))

        return cls(options, preview_label, preview_value)

    def set_index(self, index: int | None) -> None:
        self.index = index
        return

    def get_value(self) -> Any | None:
        if self.index is None:
            return self.preview_value
        return self.values[self.index]

    def get_label(self) -> str:
        if self.index is None:
            return self.preview_label
        return self.labels[self.index]

    def gui(self, combo_label: str) -> bool:
        if not hasattr(self, "texture_refs"):
            self.texture_refs = []
            for image in self.images:
                texture_id = create_texture_from_image(image)
                texture_ref = imgui.ImTextureRef(texture_id)
                self.texture_refs.append(texture_ref)

        state_changed = False
        if imgui.begin_combo(combo_label, self.get_label()):
            for i, (label, texture_ref) in enumerate(
                zip(self.labels, self.texture_refs)
            ):
                changed, value = imgui.selectable(f"##{i:02d}", False)
                imgui.same_line()
                imgui.image(texture_ref, (32, 32))
                imgui.same_line()
                imgui.text(label)

                if changed and value:
                    self.index = i
                    state_changed = True
            imgui.end_combo()
        return state_changed
