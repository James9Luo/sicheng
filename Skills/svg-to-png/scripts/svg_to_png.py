#!/usr/bin/env python3
"""
SVG to PNG 转换脚本
单文件 SVG 转 PNG，支持自定义尺寸和背景
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


def svg_to_png(
    input_path: str,
    output_path: str,
    width: int = None,
    height: int = None,
    scale: float = None,
    background: str = None
):
    """
    将 SVG 文件转换为 PNG

    Args:
        input_path: 输入 SVG 文件路径
        output_path: 输出 PNG 文件路径
        width: 输出宽度（像素）
        height: 输出高度（像素）
        scale: 缩放比例
        background: 背景颜色 (RGBA格式，如 "255,255,255,255")
    """
    # 确保输出目录存在
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 准备转换参数
    convert_kwargs = {}

    if width:
        convert_kwargs['output_width'] = width
    if height:
        convert_kwargs['output_height'] = height
    if scale:
        convert_kwargs['scale'] = scale
    if background:
        # 解析 RGBA 格式
        rgba = [int(x) for x in background.split(',')]
        if len(rgba) == 4:
            convert_kwargs['background_color'] = (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3]/255)

    # 执行转换
    try:
        cairosvg.svg2png(
            url=input_path,
            write_to=output_path,
            **convert_kwargs
        )
        print(f"✓ Converted: {input_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error converting {input_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert SVG to PNG',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion
  python svg_to_png.py input.svg output.png

  # Custom size
  python svg_to_png.py input.svg output.png --width 68 --height 68

  # With scale
  python svg_to_png.py input.svg output.png --scale 2.0

  # With background
  python svg_to_png.py input.svg output.png --background 255,255,255,255
        """
    )

    parser.add_argument('input', help='Input SVG file path')
    parser.add_argument('output', help='Output PNG file path')
    parser.add_argument('-w', '--width', type=int, help='Output width in pixels')
    parser.add_argument('--height', type=int, help='Output height in pixels')
    parser.add_argument('-s', '--scale', type=float, help='Scale factor')
    parser.add_argument('-b', '--background', help='Background color (RGBA format: R,G,B,A)')

    args = parser.parse_args()

    # 验证输入文件
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # 执行转换
    success = svg_to_png(
        args.input,
        args.output,
        width=args.width,
        height=args.height,
        scale=args.scale,
        background=args.background
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()