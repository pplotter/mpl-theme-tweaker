"""Hook file for pyinstaller."""

import os  # noqa: I001

from PyInstaller.utils.hooks import copy_metadata


# Copy `mpl_theme_tweaker/assets` folder to _internal
source_dir = os.path.abspath("../src/mpl_theme_tweaker/assets")
datas = [(source_dir, "mpl_theme_tweaker/assets")]
