#!/usr/bin/env python3
"""
十二时辰图标批量生成脚本
专门用于生成 Zepp OS 表盘的十二时辰图标
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import cairosvg
except ImportError:
    print("Error: cairosvg not installed. Run: pip install cairosvg")
    sys.exit(1)


# 十二时辰定义
SHICHEN_LIST = [
    {"name": "子", "index": 0, "start": "23:00", "end": "01:00"},
    {"name": "丑", "index": 1, "start": "01:00", "end": "03:00"},
    {"name": "寅", "index": 2, "start": "03:00", "end": "05:00"},
    {"name": "卯", "index": 3, "start": "05:00", "end": "07:00"},
    {"name": "辰", "index": 4, "start": "07:00", "end": "09:00"},
    {"name": "巳", "index": 5, "start": "09:00", "end": "11:00"},
    {"name": "午", "index": 6, "start": "11:00", "end": "13:00"},
    {"name": "未", "index": 7, "start": "13:00", "end": "15:00"},
    {"name": "申", "index": 8, "start": "15:00", "end": "17:00"},
    {"name": "酉", "index": 9, "start": "17:00", "end": "19:00"},
    {"name": "戌", "index": 10, "start": "19:00", "end": "21:00"},
    {"name": "亥", "index": 11, "start": "21:00", "end": "23:00"},
]

# 刻分定义
KEFEN_LIST = [
    {"name": "初", "index": 0},
    {"name": "一刻", "index": 1},
    {"name": "二刻", "index": 2},
    {"name": "三刻", "index": 3},
    {"name": "正", "index": 4},
]

# 辅助字
AUXILIARY_LIST = [
    {"name": "入", "index": 0},
    {"name": "出", "index": 1},
]


def create_digit_template(font_size: int = 48, font_family: str = "Noto Sans SC",
                          color: str = "#FFFFFF", stroke_color: str = "#000000",
                          stroke_width: int = 2, padding: int = 10) -> str:
    """创建数字 SVG 模板"""
    canvas_size = font_size + padding * 2
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{canvas_size}" 
     height="{canvas_size}" 
     viewBox="0 0 {canvas_size} {canvas_size}">
  <rect width="100%" height="100%" fill="transparent"/>
  <text x="50%" y="50%" 
        font-family="{font_family}" 
        font-size="{font_size}" 
        fill="{color}" 
        stroke="{stroke_color}" 
        stroke-width="{stroke_width}"
        text-anchor="middle" 
        dominant-baseline="central">{{content}}</text>
</svg>'''


def create_chinese_template(font_size: int = 48, font_family: str = "Noto Serif SC",
                            color: str = "#FFFFFF", stroke_color: str = "#000000",
                            stroke_width: int = 2, padding: int = 10) -> str:
    """创建汉字 SVG 模板"""
    canvas_size = font_size + padding * 2
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{canvas_size}" 
     height="{canvas_size}" 
     viewBox="0 0 {canvas_size} {canvas_size}">
  <rect width="100%" height="100%" fill="transparent"/>
  <text x="50%" y="50%" 
        font-family="{font_family}" 
        font-size="{font_size}" 
        fill="{color}" 
        stroke="{stroke_color}" 
        stroke-width="{stroke_width}"
        text-anchor="middle" 
        dominant-baseline="central">{{content}}</text>
</svg>'''


def create_vertical_template(font_size: int = 32, font_family: str = "Noto Serif SC",
                             color: str = "#FFFFFF", stroke_color: str = "#000000",
                             stroke_width: int = 2, padding: int = 8,
                             lines: int = 4) -> str:
    """创建竖排 SVG 模板（用于刻分组合）"""
    canvas_width = font_size + padding * 2
    canvas_height = font_size * lines + padding * 2
    line_height = font_size * 1.2
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{canvas_width}" 
     height="{canvas_height}" 
     viewBox="0 0 {canvas_width} {canvas_height}">
  <rect width="100%" height="100%" fill="transparent"/>
  <text x="50%" y="{padding + font_size/2}" 
        font-family="{font_family}" 
        font-size="{font_size}" 
        fill="{color}" 
        stroke="{stroke_color}" 
        stroke-width="{stroke_width}"
        text-anchor="middle" 
        dominant-baseline="central">{{line1}}</text>
  <text x="50%" y="{padding + font_size/2 + line_height}" 
        font-family="{font_family}" 
        font-size="{font_size}" 
        fill="{color}" 
        stroke="{stroke_color}" 
        stroke-width="{stroke_width}"
        text-anchor="middle" 
        dominant-baseline="central">{{line2}}</text>
  <text x="50%" y="{padding + font_size/2 + line_height * 2}" 
        font-family="{font_family}" 
        font-size="{font_size}" 
        fill="{color}" 
        stroke="{stroke_color}" 
        stroke-width="{stroke_width}"
        text-anchor="middle" 
        dominant-baseline="central">{{line3}}</text>
  <text x="50%" y="{padding + font_size/2 + line_height * 3}" 
        font-family="{font_family}" 
        font-size="{font_size}" 
        fill="{color}" 
        stroke="{stroke_color}" 
        stroke-width="{stroke_width}"
        text-anchor="middle" 
        dominant-baseline="central">{{line4}}</text>
</svg>'''


def render_svg(svg_content: str, output_path: str, width: int = None, height: int = None):
    """渲染 SVG 并保存为 PNG"""
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    convert_kwargs = {}
    if width:
        convert_kwargs['output_width'] = width
    if height:
        convert_kwargs['output_height'] = height

    try:
        cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            write_to=output_path,
            **convert_kwargs
        )
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def generate_shichen(output_dir: str, font_size: int = 48, 
                     font_family: str = "Noto Serif SC",
                     color: str = "#FFFFFF", stroke_color: str = "#000000",
                     stroke_width: int = 2):
    """生成十二时辰图标"""
    print(f"\n🕐 Generating Shichen Icons...")
    print(f"   Output: {output_dir}")
    print(f"   Font: {font_family} {font_size}px")
    print("-" * 50)

    template = create_chinese_template(
        font_size=font_size,
        font_family=font_family,
        color=color,
        stroke_color=stroke_color,
        stroke_width=stroke_width
    )

    success = 0
    for shichen in SHICHEN_LIST:
        svg_content = template.replace("{{content}}", shichen["name"])
        filename = f"shichen_{shichen['index']:02d}_{shichen['name']}.png"
        output_path = Path(output_dir) / filename

        if render_svg(svg_content, str(output_path)):
            print(f"  ✓ {filename}")
            success += 1
        else:
            print(f"  ✗ {filename}")

    print("-" * 50)
    print(f"✅ Done: {success}/{len(SHICHEN_LIST)} succeeded")
    return success


def generate_digits(output_dir: str, font_size: int = 48,
                    font_family: str = "Noto Sans SC",
                    color: str = "#FFFFFF", stroke_color: str = "#000000",
                    stroke_width: int = 2):
    """生成数字 0-9 图标"""
    print(f"\n🔢 Generating Digit Icons...")
    print(f"   Output: {output_dir}")
    print(f"   Font: {font_family} {font_size}px")
    print("-" * 50)

    template = create_digit_template(
        font_size=font_size,
        font_family=font_family,
        color=color,
        stroke_color=stroke_color,
        stroke_width=stroke_width
    )

    success = 0
    for i in range(10):
        svg_content = template.replace("{{content}}", str(i))
        filename = f"digit_{i}.png"
        output_path = Path(output_dir) / filename

        if render_svg(svg_content, str(output_path)):
            print(f"  ✓ {filename}")
            success += 1
        else:
            print(f"  ✗ {filename}")

    print("-" * 50)
    print(f"✅ Done: {success}/10 succeeded")
    return success


def generate_kefen(output_dir: str, font_size: int = 32,
                   font_family: str = "Noto Serif SC",
                   color: str = "#FFFFFF", stroke_color: str = "#000000",
                   stroke_width: int = 2):
    """生成刻分图标"""
    print(f"\n⏱️ Generating Kefen Icons...")
    print(f"   Output: {output_dir}")
    print(f"   Font: {font_family} {font_size}px")
    print("-" * 50)

    template = create_chinese_template(
        font_size=font_size,
        font_family=font_family,
        color=color,
        stroke_color=stroke_color,
        stroke_width=stroke_width
    )

    success = 0
    for kefen in KEFEN_LIST:
        svg_content = template.replace("{{content}}", kefen["name"])
        filename = f"kefen_{kefen['index']}_{kefen['name']}.png"
        output_path = Path(output_dir) / filename

        if render_svg(svg_content, str(output_path)):
            print(f"  ✓ {filename}")
            success += 1
        else:
            print(f"  ✗ {filename}")

    print("-" * 50)
    print(f"✅ Done: {success}/{len(KEFEN_LIST)} succeeded")
    return success


def generate_auxiliary(output_dir: str, font_size: int = 32,
                       font_family: str = "Noto Serif SC",
                       color: str = "#FFFFFF", stroke_color: str = "#000000",
                       stroke_width: int = 2):
    """生成辅助字图标"""
    print(f"\n🔤 Generating Auxiliary Icons...")
    print(f"   Output: {output_dir}")
    print(f"   Font: {font_family} {font_size}px")
    print("-" * 50)

    template = create_chinese_template(
        font_size=font_size,
        font_family=font_family,
        color=color,
        stroke_color=stroke_color,
        stroke_width=stroke_width
    )

    success = 0
    for aux in AUXILIARY_LIST:
        svg_content = template.replace("{{content}}", aux["name"])
        filename = f"aux_{aux['index']}_{aux['name']}.png"
        output_path = Path(output_dir) / filename

        if render_svg(svg_content, str(output_path)):
            print(f"  ✓ {filename}")
            success += 1
        else:
            print(f"  ✗ {filename}")

    print("-" * 50)
    print(f"✅ Done: {success}/{len(AUXILIARY_LIST)} succeeded")
    return success


def generate_all(output_dir: str, font_size: int = 48, kefen_size: int = 32,
                 font_family: str = "Noto Serif SC",
                 digit_family: str = "Noto Sans SC",
                 color: str = "#FFFFFF", stroke_color: str = "#000000",
                 stroke_width: int = 2):
    """生成所有图标"""
    print("\n" + "=" * 50)
    print("🎯 Generating All Watchface Assets")
    print("=" * 50)

    total_success = 0

    # 生成十二时辰
    shichen_dir = Path(output_dir) / "shichen"
    total_success += generate_shichen(
        str(shichen_dir), font_size, font_family, color, stroke_color, stroke_width
    )

    # 生成数字
    digit_dir = Path(output_dir) / "digits"
    total_success += generate_digits(
        str(digit_dir), font_size, digit_family, color, stroke_color, stroke_width
    )

    # 生成刻分
    kefen_dir = Path(output_dir) / "kefen"
    total_success += generate_kefen(
        str(kefen_dir), kefen_size, font_family, color, stroke_color, stroke_width
    )

    # 生成辅助字
    aux_dir = Path(output_dir) / "auxiliary"
    total_success += generate_auxiliary(
        str(aux_dir), kefen_size, font_family, color, stroke_color, stroke_width
    )

    print("\n" + "=" * 50)
    print(f"🎉 All Done! Total: {total_success} files generated")
    print(f"📁 Output: {output_dir}")
    print("=" * 50)

    return total_success


def main():
    parser = argparse.ArgumentParser(
        description='Generate Shichen (十二时辰) watchface icons',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all icons
  python generate_shichen.py --output-dir assets

  # Generate only shichen icons
  python generate_shichen.py --output-dir assets --type shichen

  # Custom font size
  python generate_shichen.py --output-dir assets --font-size 48 --kefen-size 32

  # Custom colors
  python generate_shichen.py --output-dir assets --color "#FFD700" --stroke-color "#8B4513"
        """
    )

    parser.add_argument('-o', '--output-dir', default='assets', help='Output directory')
    parser.add_argument('-t', '--type', choices=['all', 'shichen', 'digits', 'kefen', 'auxiliary'],
                        default='all', help='Type of icons to generate')
    parser.add_argument('--font-size', type=int, default=48, help='Font size for shichen/digits')
    parser.add_argument('--kefen-size', type=int, default=32, help='Font size for kefen/auxiliary')
    parser.add_argument('--font-family', default='Noto Serif SC', help='Chinese font family')
    parser.add_argument('--digit-family', default='Noto Sans SC', help='Digit font family')
    parser.add_argument('--color', default='#FFFFFF', help='Text color')
    parser.add_argument('--stroke-color', default='#000000', help='Stroke color')
    parser.add_argument('--stroke-width', type=int, default=2, help='Stroke width')

    args = parser.parse_args()

    if args.type == 'all':
        generate_all(
            args.output_dir,
            args.font_size,
            args.kefen_size,
            args.font_family,
            args.digit_family,
            args.color,
            args.stroke_color,
            args.stroke_width
        )
    elif args.type == 'shichen':
        generate_shichen(
            args.output_dir + "/shichen",
            args.font_size,
            args.font_family,
            args.color,
            args.stroke_color,
            args.stroke_width
        )
    elif args.type == 'digits':
        generate_digits(
            args.output_dir + "/digits",
            args.font_size,
            args.digit_family,
            args.color,
            args.stroke_color,
            args.stroke_width
        )
    elif args.type == 'kefen':
        generate_kefen(
            args.output_dir + "/kefen",
            args.kefen_size,
            args.font_family,
            args.color,
            args.stroke_color,
            args.stroke_width
        )
    elif args.type == 'auxiliary':
        generate_auxiliary(
            args.output_dir + "/auxiliary",
            args.kefen_size,
            args.font_family,
            args.color,
            args.stroke_color,
            args.stroke_width
        )


if __name__ == '__main__':
    main()