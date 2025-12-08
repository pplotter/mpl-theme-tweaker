[中文版](./README.zh.md)

# Matplotlib Theme Tweaker

A simple GUI tool for adjusting, previewing, and managing matplotlib style sheets.

**Current version (0.1.0) has only been tested on Windows platforms. Issues may arise on other platforms.**

## Installation

The software was developed using Python 3.13 and currently supports the following installation methods:

1. [pipx](https://pipx.pypa.io/stable/installation/)

```bash
pipx install mpl-theme-tweaker
```

2. [uv tool](https://docs.astral.sh/uv/getting-started/installation/)

```bash
uv tool install mpl-theme-tweaker
```

3. For Windows users, you can also directly download the precompiled executable from the [Release](https://github.com/pplotter/mpl-theme-tweaker/releases) page.

4. Install from source code. This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/) as the dependency management tool. It is recommended to use uv to install project dependencies. After downloading, run the following command to install dependencies:

```bash
uv sync
```

## Basic Usage

After installing via methods 1-3 above, you can run the `mpl-theme-tweaker` command in the command line or double-click the application icon to start the tool.
If you installed via method 4, you need to execute the main.py file to run the software. The software interface is as follows:

![gui](./image/gui.png)

Users can adjust parameters in different configuration sections and observe the changes on the image.

- `File` menu: Used to export style files
- `View` menu: Used to control software views and themes
- `Style` menu: Used to switch between different style sheets

## Multi-language Support

The software uses Python's `gettext` module for internationalization, and uses the [Gnu gettext](https://www.gnu.org/software/gettext/) tool to create translation files with the following command:

```bash
msgfmt messages.<LANG_ID_CODE>.po -o messages.mo
```

Currently supports Chinese and English. Translation files are located in the `src/mpl_theme_tweaker/assets/locale/` directory.
Users who need other languages can copy the `messages.en.po` file and translate it themselves.

## Todo

- [ ] Custom formula fonts
- [ ] Add more example images
- [ ] Add code tests (multi-platform)
