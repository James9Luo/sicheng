---
name: svg-to-png
version: "1.0.0"
description: SVG 转 PNG 批量生成技能，支持 SVG 模板渲染、批量图标生成、表盘资源批量导出等场景。适用于 Zepp OS 表盘开发中的数字、汉字、刻度图标批量生成。
author: "Zepp OS Developer"
category: "asset-generation"
tags:
  - svg
  - png
  - batch
  - icon-generation
  - watchface
  - zeppos
trigger:
  - "SVG 转 PNG"
  - "批量生成图标"
  - "批量生成图片资源"
  - "SVG 模板渲染"
  - "生成表盘图标资源"
  - "svg to png"
  - "batch generate icons"
  - "svg template"
compatibility:
  python_version: ">=3.8"
  requires_packages:
    - cairosvg
    - pillow
    - lxml
  optional_packages:
    - rsvg-convert
    - imagemagick
---

# SVG to PNG 批量生成技能

**版本**: 1.0.0  
**更新日期**: 2025-01-01

## 功能描述

这是一个 SVG 转 PNG 批量生成技能，用于帮助用户快速将 SVG 模板渲染为 PNG 图片资源。该技能支持：

1. **单文件转换** - 将单个 SVG 文件转换为 PNG
2. **批量生成** - 基于模板和配置批量生成多个 PNG 文件
3. **十二时辰专用** - 针对 Zepp OS 表盘开发的十二时辰图标生成

## 快速开始

### 依赖

- Python 3.8+
- cairosvg
- Pillow
- lxml

### 运行方式

```bash
# 单个文件转换
python .trae/skills/svg-to-png/scripts/svg_to_png.py input.svg output.png --width 68 --height 68

# 批量生成
python .trae/skills/svg-to-png/scripts/batch_generate.py config.json

# 使用模板批量生成
python .trae/skills/svg-to-png/scripts/batch_generate.py --template templates/digit.svg --items "0,1,2,3,4,5,6,7,8,9" --output-dir output/digits
```

## 环境要求

### 必需工具

| 工具 | 安装命令 | 说明 |
|------|----------|------|
| Python 3.8+ | - | 运行环境 |
| cairosvg | `pip install cairosvg` | SVG 转 PNG（推荐） |
| Pillow | `pip install pillow` | 图片处理 |
| lxml | `pip install lxml` | XML 解析 |

### 可选工具

| 工具 | 安装命令 | 说明 |
|------|----------|------|
| rsvg-convert | `apt install librsvg2-bin` | 命令行 SVG 转换 |
| ImageMagick | `apt install imagemagick` | 强大的图片处理工具 |

## 使用流程

### 步骤 1：环境检查

```bash
# 检查 Python 版本
python --version

# 检查依赖包
pip show cairosvg pillow lxml
```

### 步骤 2：准备 SVG 模板

在 `templates/` 目录下放置 SVG 模板文件，模板使用变量占位符：

```svg
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{{width}}" 
     height="{{height}}" 
     viewBox="0 0 {{width}} {{height}}">
  <text x="50%" y="50%" 
        font-size="{{fontSize}}"
        text-anchor="middle" 
        dominant-baseline="central">{{content}}</text>
</svg>
```

### 步骤 3：配置生成参数

创建 `config.json` 配置文件：

```json
{
  "template": "templates/digit.svg",
  "output_dir": "output/digits",
  "width": 68,
  "height": 68,
  "items": [
    {"content": "0", "filename": "0.png"},
    {"content": "1", "filename": "1.png"},
    {"content": "2", "filename": "2.png"}
  ]
}
```

### 步骤 4：执行生成

```bash
# 单个文件转换
python .trae/skills/svg-to-png/scripts/svg_to_png.py input.svg output.png --width 68 --height 68

# 批量生成
python .trae/skills/svg-to-png/scripts/batch_generate.py config.json

# 使用模板批量生成
python .trae/skills/svg-to-png/scripts/batch_generate.py --template templates/digit.svg --items "0,1,2,3,4,5,6,7,8,9" --output-dir output/digits
```

## 脚本说明

### svg_to_png.py - 单文件转换

```bash
python svg_to_png.py <input.svg> <output.png> [options]

Options:
  --width, -w      输出宽度（像素）
  --height, -h     输出高度（像素）
  --scale, -s      缩放比例
  --background     背景颜色（RGBA）
```

### batch_generate.py - 批量生成

```bash
python batch_generate.py <config.json>

# 或使用命令行参数
python batch_generate.py --template <template.svg> --items <items.json> --output-dir <dir>
```

### generate_shichen.py - 十二时辰专用

```bash
# 生成十二时辰图标
python generate_shichen.py --output-dir assets/shichen --font-size 48

# 生成刻分图标
python generate_kefen.py --output-dir assets/kefen
```

## 常用命令速查

```bash
# 安装依赖
pip install cairosvg pillow lxml

# 单个 SVG 转 PNG
python svg_to_png.py input.svg output.png --width 68 --height 68

# 批量转换（同一模板，不同内容）
python batch_generate.py --template digit.svg --items "0,1,2,3,4,5,6,7,8,9" --output-dir digits

# 批量转换（不同模板）
python batch_generate.py config.json

# 十二时辰批量生成
python generate_shichen.py --output-dir assets/shichen

# 查看帮助
python svg_to_png.py --help
python batch_generate.py --help
```

## 故障排除

### 问题 1：cairosvg 导入失败

```bash
# 安装 Cairo 库（Linux）
sudo apt-get install libcairo2-dev

# 安装 Cairo 库（macOS）
brew install cairo

# 重新安装 cairosvg
pip uninstall cairosvg
pip install cairosvg
```

### 问题 2：字体显示异常

确保 SVG 中使用系统已安装的字体，或将字体转换为路径。

### 问题 3：输出尺寸不准确

检查 SVG 的 viewBox 属性是否与 width/height 一致。

## 示例：Zepp OS 表盘图标生成

### 生成数字 0-9

```bash
python batch_generate.py -c <<EOF
{
  "template": "templates/digit.svg",
  "output_dir": "assets/digits",
  "width": 68,
  "height": 68,
  "font_size": 48,
  "font_family": "Noto Sans SC",
  "color": "#FFFFFF",
  "stroke_color": "#000000",
  "stroke_width": 2,
  "items": [
    {"content": "0", "filename": "0.png"},
    {"content": "1", "filename": "1.png"},
    {"content": "2", "filename": "2.png"},
    {"content": "3", "filename": "3.png"},
    {"content": "4", "filename": "4.png"},
    {"content": "5", "filename": "5.png"},
    {"content": "6", "filename": "6.png"},
    {"content": "7", "filename": "7.png"},
    {"content": "8", "filename": "8.png"},
    {"content": "9", "filename": "9.png"}
  ]
}
EOF
```

### 生成十二时辰

```bash
python generate_shichen.py --output-dir assets/shichen --font-size 48
```

## Python API 使用

除了命令行界面，该技能还提供了 Python API 接口：

```python
from .trae.skills.svg_to_png.svg_to_png import SVGToPNGConverter

# 创建转换器实例
converter = SVGToPNGConverter()

# 单文件转换
converter.convert("input.svg", "output.png", width=68, height=68)

# 批量转换
converter.batch_convert(config_file="config.json")

# 模板渲染
converter.render_template(
    template="templates/digit.svg",
    items=[{"content": "0", "filename": "0.png"}],
    output_dir="output"
)
```

## 返回值说明

所有方法调用成功后，返回一个包含以下字段的字典：

```python
{
    "status": "success",  # 状态：success 或 error
    "output_files": ["output/0.png", "output/1.png"],  # 生成的文件列表
    "message": "转换成功"  # 提示信息
}
```

如果发生错误，返回：

```python
{
    "status": "error",
    "error": "错误描述信息",
    "message": "操作失败"
}
```

## 常见问题 (FAQ)

### Q1: 如何生成透明背景的 PNG？
A: 确保 SVG 中没有设置背景矩形，或设置 `fill="transparent"`。

### Q2: 支持哪些 SVG 特性？
A: 支持基本的 SVG 元素（text、rect、circle、path 等），复杂特效可能需要先转换为路径。

### Q3: 如何处理中文字体？
A: 确保系统安装了相应字体，或在 SVG 中使用嵌入字体。

### Q4: 批量生成时如何控制输出质量？
A: 在配置文件中设置 `quality` 参数（1-100）。

### Q5: 如何生成不同尺寸的同一图标？
A: 使用 `batch_generate.py` 的 `--scale` 参数或配置多个尺寸项。

## 相关技能

- [[svg-design-review|SVG 设计审稿]] - SVG 设计评审与优化
- [[watchface-development|表盘开发]] - Zepp OS 表盘完整开发流程

## 许可证

Copyright © [2025] Zepp OS Developer. All rights reserved.