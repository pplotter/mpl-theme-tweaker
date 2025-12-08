[中文版](./packaging.README.zh.md)

# Packaging Instructions

The project is packaged using [PyInstaller](https://pyinstaller.org/en/stable/).
The main parameters of the packaging command are explained below:

1. --onedir: Packages all files into a single directory. If the `--onefile` parameter is used instead, all files will be packaged into a single executable file, which will be temporarily extracted during runtime.
2. --icon: Specifies the path to the application icon file.
3. --name: Specifies the name of the packaged application.
4. --upx-dir: Specifies the directory path for the UPX compression tool. If UPX is not installed locally, this parameter can be omitted.
5. --additional-hooks-dir: Specifies the path to an additional hooks directory, used to package resource files into the executable.

```bash
# Navigate to the pyinstaller directory
cd pyinstaller
# Package the project
pyinstaller --onedir
    --icon "..\\src\\mpl_theme_tweaker\\assets\\mpl-theme-tweaker.png"
    --name "mpl-theme-tweaker"
    --upx-dir ""
    --additional-hooks-dir "."
    ../src/mpl_theme_tweaker/main.py

# Or you can directly use the configuration file
pyinstaller mpl-theme-tweaker.spec
```

After packaging is completed, a `dist` directory will be generated in the packaging directory, which contains the packaged application.
