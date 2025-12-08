[英文版](./packaging.README.md)

# 打包说明

项目使用 [PyInstaller](https://pyinstaller.org/en/stable/) 打包，
下面的打包命令主要参数含义如下：

1. --onedir：将所有文件打包到一个目录中，如果采用`--onefile`参数，则会将所有文件打包到一个可执行文件中，运行时会临时解压。
2. --icon：指定应用程序的图标文件路径。
3. --name：指定打包后的应用程序名称。
4. --upx-dir：指定 UPX 压缩工具的目录路径，如果本地未安装 UPX 压缩工具，可以去掉该参数。
5. --additional-hooks-dir：指定额外的钩子目录路径，用于将资源文件打包到可执行文件中。

```bash
# 进入 pyinstaller 目录
cd pyinstaller
# 打包项目
pyinstaller --onedir
    --icon "..\\src\\mpl_theme_tweaker\\assets\\mpl-theme-tweaker.png"
    --name "mpl-theme-tweaker"
    --upx-dir ""
    --additional-hooks-dir "."
    ../src/mpl_theme_tweaker/main.py

# 或者可以直接使用配置文件
pyinstaller mpl-theme-tweaker.spec
```

打包完成后会在打包目录下生成`dist`目录，其中包含了打包后的应用程序。
