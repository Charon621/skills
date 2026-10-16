#!/usr/bin/env python3
"""Render PDF pages and stitch manually selected regions. Requires Pillow and pdftoppm."""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from PIL import Image


def capture(pdf, regions, output, dpi=180):
    if not shutil.which('pdftoppm'):
        raise RuntimeError('Install Poppler (pdftoppm) to render PDF pages')
    if not regions or not 72 <= dpi <= 600:
        raise ValueError('Provide regions and a DPI between 72 and 600')
    crops = []
    with tempfile.TemporaryDirectory(prefix='paper-capture-') as directory:
        rendered = {}
        for region in regions:
            page, box = region['page'], region['box']
            if not isinstance(page, int) or page < 1 or len(box) != 4:
                raise ValueError('page is 1-based; box has four coordinates')
            left, top, right, bottom = map(float, box)
            if not 0 <= left < right <= 1 or not 0 <= top < bottom <= 1:
                raise ValueError('Coordinates must satisfy 0 <= left < right <= 1 and top < bottom')
            if page not in rendered:
                prefix = Path(directory) / str(page)
                subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-singlefile',
                                '-r', str(dpi), '-png', str(pdf.resolve()), str(prefix)],
                               check=True, capture_output=True)
                rendered[page] = prefix.with_suffix('.png')
            with Image.open(rendered[page]) as image:
                bounds = (round(left*image.width), round(top*image.height),
                          round(right*image.width), round(bottom*image.height))
                if bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
                    raise ValueError('Crop is too small at this DPI')
                crops.append(image.crop(bounds).convert('RGB'))
    margin = 24
    result = Image.new('RGB', (max(c.width for c in crops)+margin*2,
                              sum(c.height for c in crops)+margin*(len(crops)+1)), 'white')
    y = margin
    for crop in crops:
        result.paste(crop, ((result.width-crop.width)//2, y))
        y += crop.height + margin
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output, format='PNG')
    return {'output': str(output), 'width': result.width, 'height': result.height,
            'regions': len(crops), 'review': 'Visually verify title and entire abstract before publication'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('regions', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--dpi', type=int, default=180)
    args = parser.parse_args()
    print(json.dumps(capture(args.pdf, json.loads(args.regions.read_text(encoding='utf-8')),
                             args.output, args.dpi), ensure_ascii=False))
