from __future__ import annotations

import math
from html import escape
from pathlib import Path


def save_vectors(path: Path, items: list[dict], description: str,
                 width: int = 1200, height: int = 920) -> None:
    """Write the same line/rectangle/text scene as SVG and single-page PDF."""
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
           f"<desc>{escape(description)}</desc>", '<rect width="100%" height="100%" fill="white"/>']
    pdf = ["0.72 0 0 0.72 0 0 cm"]
    for item in items:
        kind = item["kind"]
        if kind not in {"line", "rect", "text"}:
            raise ValueError("unsupported vector primitive")
        if any(not math.isfinite(v) for v in item.values() if type(v) in {int, float}):
            raise ValueError("nonfinite vector coordinate")
        color = item.get("color", "#222222")
        rgb = " ".join(str(int(color[i:i+2], 16) / 255) for i in (1, 3, 5))
        pdf.append(f"{rgb} RG {rgb} rg 1 w")
        if kind == "line":
            x, y, a, b = (item[k] for k in ("x", "y", "a", "b"))
            svg.append(f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" stroke="{color}"/>')
            pdf.append(f"{x} {height-y} m {a} {height-b} l S")
        elif kind == "rect":
            x, y, w, h = (item[k] for k in ("x", "y", "w", "h"))
            filled = item.get("filled", True)
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                       f'fill="{color if filled else "white"}" stroke="{color}"/>')
            if not filled:
                pdf.append("1 1 1 rg")
            pdf.append(f"{x} {height-y-h} {w} {h} re {'f' if filled else 'B'}")
        else:
            x, y, text = item["x"], item["y"], item["text"]
            size = item.get("size", 14)
            svg.append(f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" '
                       f'font-size="{size}" fill="{color}">{escape(text)}</text>')
            # Chart labels deliberately use ASCII for the built-in PDF font.
            text.encode("ascii")
            literal = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            pdf.append(f"BT /F1 {size} Tf {x} {height-y} Td ({literal}) Tj ET")
    svg.append("</svg>")
    with path.with_suffix(".svg").open("x", encoding="utf-8") as stream:
        stream.write("\n".join(svg))
    content = "\n".join(pdf).encode("ascii")
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width*.72} {height*.72}] "
         "/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>").encode(),
        f"<< /Length {len(content)} >>\nstream\n".encode() + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    data = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f"{i} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(data)
    data.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode())
    trailer = f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    data.extend(trailer.encode())
    with path.with_suffix(".pdf").open("xb") as stream:
        stream.write(data)
