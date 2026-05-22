#!/usr/bin/env python3
"""
批量 SVG 模板渲染脚本
基于模板和配置批量生成 PNG 图片
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import cairosvg
except ImportError:
    print("Error: cairosvg not installed. Run: pip install cairosvg")
    sys.exit(1)


def render_template(
    template: str,
    variables: dict,
    output_path: str,
    width: int = None,
    height: int = None
):
    """
    渲染 SVG 模板并输出 PNG

    Args:
        template: SVG 模板字符串
        variables: 变量字典
        output_path: 输出路径
        width: 输出宽度
        height: 输出高度
    """
    # 替换模板变量
    content = template
    for key, value in variables.items():
        placeholder = f"{{{{{key}}}}}"
        content = content.replace(placeholder, str(value))

    # 确保输出目录存在
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 准备转换参数
    convert_kwargs = {}
    if width:
        convert_kwargs['output_width'] = width
    if height:
        convert_kwargs['output_height'] = height

    # 执行转换
    try:
        cairosvg.svg2png(
            bytestring=content.encode('utf-8'),
            write_to=output_path,
            **convert_kwargs
        )
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def load_template(template_path: str) -> str:
    """加载 SVG 模板文件"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_items(items_path: str) -> list:
    """加载项目列表（支持 JSON 或简单文本列表）"""
    if items_path.endswith('.json'):
        with open(items_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 简单逗号分隔列表
        return [{"content": item.strip()} for item in items_path.split(',')]


def batch_generate(
    template_path: str,
    items: list,
    output_dir: str,
    width: int = 68,
    height: int = 68,
    base_variables: dict = None
):
    """
    批量生成 PNG 图片

    Args:
        template_path: SVG 模板路径
        items: 项目列表
        output_dir: 输出目录
        width: 输出宽度
        height: 输出高度
        base_variables: 基础变量（字体、大小等）
    """
    # 加载模板
    template = load_template(template_path)

    # 确保输出目录存在
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 基础变量
    base_vars = base_variables or {}

    # 统计
    success = 0
    failed = 0

    print(f"\n📦 Template: {template_path}")
    print(f"📁 Output: {output_dir}")
    print(f"📏 Size: {width}x{height}")
    print(f"📋 Items: {len(items)}")
    print("-" * 50)

    for i, item in enumerate(items):
        # 合并变量
        variables = {**base_vars, **item}

        # 确定输出文件名
        if 'filename' in item:
            filename = item['filename']
        elif 'content' in item:
            # 使用内容作为文件名（处理特殊字符）
            content = str(item['content']).replace('\n', '_')
            filename = f"{content}.png"
        else:
            filename = f"item_{i:03d}.png"

        output_path = output_dir / filename

        # 渲染
        if render_template(template, variables, str(output_path), width, height):
            print(f"  ✓ {filename}")
            success += 1
        else:
            print(f"  ✗ {filename}")
            failed += 1

    print("-" * 50)
    print(f"✅ Done: {success} succeeded, {failed} failed")
    return success, failed


def main():
    parser = argparse.ArgumentParser(
        description='Batch generate PNG from SVG template',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('config', nargs='?', help='Config JSON file path')
    parser.add_argument('-c', '--config-json', help='Config JSON string (use with -c)')
    parser.add_argument('-t', '--template', help='SVG template file path')
    parser.add_argument('-i', '--items', help='Items list (JSON file or comma-separated string)')
    parser.add_argument('-o', '--output-dir', default='output', help='Output directory')
    parser.add_argument('-w', '--width', type=int, default=68, help='Output width')
    parser.add_argument('-h', '--height', type=int, default=68, help='Output height')
    parser.add_argument('--font-size', type=int, help='Font size')
    parser.add_argument('--font-family', default='Noto Sans SC', help='Font family')
    parser.add_argument('--color', default='#FFFFFF', help='Text color')
    parser.add_argument('--stroke-color', default='#000000', help='Stroke color')
    parser.add_argument('--stroke-width', type=int, default=2, help='Stroke width')

    args = parser.parse_args()

    # 解析配置
    config = None

    if args.config:
        # 从文件加载配置
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
    elif args.config_json:
        # 从命令行加载配置
        config = json.loads(args.config_json)

    if config:
        # 使用配置文件
        template = config.get('template')
        items = config.get('items', [])
        output_dir = config.get('output_dir', 'output')
        width = config.get('width', 68)
        height = config.get('height', 68)
        base_vars = {k: v for k, v in config.items()
                     if k not in ['template', 'items', 'output_dir', 'width', 'height']}
    else:
        # 使用命令行参数
        if not args.template:
            print("Error: Template file is required")
            sys.exit(1)

        template = args.template
        output_dir = args.output_dir
        width = args.width
        height = args.height

        # 解析 items
        if args.items:
            if os.path.exists(args.items):
                items = load_items(args.items)
            else:
                # 逗号分隔的字符串
                items = [{"content": item.strip()} for item in args.items.split(',')]
        else:
            items = []

        # 基础变量
        base_vars = {}
        if args.font_size:
            base_vars['fontSize'] = args.font_size
        if args.font_family:
            base_vars['fontFamily'] = args.font_family
        if args.color:
            base_vars['color'] = args.color
        if args.stroke_color:
            base_vars['strokeColor'] = args.stroke_color
        if args.stroke_width:
            base_vars['strokeWidth'] = args.stroke_width

    # 执行批量生成
    success, failed = batch_generate(
        template,
        items,
        output_dir,
        width,
        height,
        base_vars
    )

    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()