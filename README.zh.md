[English Version](./README.md)

# Matplotlib Theme Tweaker

一个简单的 GUI 工具，用于调整、预览和管理 matplotlib 样式表。

**当前版本(0.1.0)仅在 Windows 平台上测试过，其他平台可能存在问题。**

## 安装

软件开发使用 python3.13，目前支持以下安装方式

1. [pipx](https://pipx.pypa.io/stable/installation/)

```bash
pipx install mpl-theme-tweaker
```

2. [uv tool](https://docs.astral.sh/uv/getting-started/installation/)

```bash
uv tool install mpl-theme-tweaker
```

3. 对于 Windows 用户，也可以直接从[Release](https://github.com/pplotter/mpl-theme-tweaker/releases)页面下载预编译的可执行文件。

4. 从源代码安装，本项目使用 [uv](https://docs.astral.sh/uv/getting-started/installation/) 作为依赖管理工具，建议使用 uv 安装项目依赖，下载后运行以下命令安装项目依赖。

```bash
uv sync
```

## 基本使用

按照上面 1-3 的安装方式安装完成后，即可在命令行中运行 `mpl-theme-tweaker` 命令或者双击团结图标启动工具，
按照方式 4 安装，则需要执行 main.py 文件运行软件，软件界面如下。

![gui](./image/gui.png)

用户可以自行跳转不同配置项的参数，观察图片上的变化。

- `File`菜单：用于导出样式文件
- `View`菜单：用于控制软件视图和主题
- `Style`菜单：用于切换不同的样式表

## 多语言支持

软件使用 python 的 `gettext` 模块进行国际化，使用 [Gnu gettext](https://www.gnu.org/software/gettext/) 工具制作翻译文件，命令为：

```bash
msgfmt messages.<LANG_ID_CODE>.po -o messages.mo
```

当前支持中文和英文，翻译文件位于 `src/mpl_theme_tweaker/assets/locale/` 目录下，
有其它语言需求的用户可以自行拷贝一份 `messages.en.po` 文件，进行翻译。

## Todo

- [ ] 自定义公式字体
- [ ] 添加更多示例图像
- [ ] 添加代码测试(多平台)
