import matplotlib.pyplot as plt
from imgui_bundle import hello_imgui, imgui, implot  # type: ignore
from matplotlib.figure import Figure
from PIL.Image import Image

from mpl_theme_tweaker.app_state import set_app_key
from mpl_theme_tweaker.figure import plot_figure
from mpl_theme_tweaker.mpl_utils import Figure2Image
from mpl_theme_tweaker.opengl import (
    create_texture_from_image,
    rebind_texture_from_image,
)


class FigureWindow:
    def __init__(self):
        plt.style.use("default")
        self.figure: Figure = plot_figure()
        self.image: Image = Figure2Image(self.figure)
        self.texture_id: int = None  # type: ignore
        self.texture_ref: imgui.ImTextureRef = None  # type: ignore
        self.replot_times: int = 0
        self.plot_flags = implot.Flags_.equal + implot.Flags_.no_legend
        set_app_key("FigureWidow.replot_func", self.replot)

    def gui(self) -> None:
        if self.texture_id is None:
            self.texture_id = create_texture_from_image(self.image)
            self.texture_ref = imgui.ImTextureRef(self.texture_id)

        if implot.begin_plot("##image", [-1, -1], flags=self.plot_flags):
            implot.setup_axes(
                x_label="", y_label="", x_flags=implot.AxisFlags_.opposite
            )

            bounds_min, bounds_max = implot.Point(0, 0), implot.Point(*self.image.size)
            implot.plot_image("Demo Figure", self.texture_ref, bounds_min, bounds_max)
            implot.end_plot()
        return

    def replot(self) -> None:
        self.replot_times += 1
        hello_imgui.log(hello_imgui.LogLevel.info, f"replot {self.replot_times}")

        if self.figure:
            plt.close(self.figure)
            self.figure = None  # type: ignore
        try:
            self.figure = plot_figure()
        except Exception as e:
            hello_imgui.log(hello_imgui.LogLevel.error, f"Error: {str(e)}")
            self.figure = None  # type: ignore
            return

        self.image = Figure2Image(self.figure)
        rebind_texture_from_image(self.texture_id, self.image)
        self.texture_ref = imgui.ImTextureRef(self.texture_id)

        return
