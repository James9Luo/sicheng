# SVG to PNG 批量生成技能

## 技能描述

### 触发条件
当用户请求以下任务时激活此技能：
- SVG 转 PNG
- 批量生成图标
- 批量生成图片资源
- SVG 模板渲染
- 生成表盘图标资源

### 适用场景
- Zepp OS 表盘开发：数字、汉字、刻度图标批量生成
- UI 资源批量导出
- 多尺寸图片生成
- 模板化图片批量渲染

---

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

---

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

---

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

---

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

---

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

---

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

---

## 相关技能

- [[svg-design-review|SVG 设计审稿]] - SVG 设计评审与优化
- [[watchface-development|表盘开发]] - Zepp OS 表盘完整开发流程