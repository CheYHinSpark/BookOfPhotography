from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"
FONT = "Source Han Sans SC, Microsoft YaHei, sans-serif"


def text(parent, x, y, value, size=24, weight="400", fill="#243b53", anchor="middle"):
    node = SubElement(
        parent,
        "text",
        {
            "x": str(x),
            "y": str(y),
            "text-anchor": anchor,
            "font-family": FONT,
            "font-size": str(size),
            "font-weight": weight,
            "fill": fill,
        },
    )
    node.text = value
    return node


def line(parent, x1, y1, x2, y2, stroke="#527da3", width=3, dash=None, marker=None):
    attrs = {
        "x1": str(x1),
        "y1": str(y1),
        "x2": str(x2),
        "y2": str(y2),
        "stroke": stroke,
        "stroke-width": str(width),
        "stroke-linecap": "round",
    }
    if dash:
        attrs["stroke-dasharray"] = dash
    if marker:
        attrs["marker-end"] = f"url(#{marker})"
    return SubElement(parent, "line", attrs)


def add_defs(svg):
    defs = SubElement(svg, "defs")
    marker = SubElement(
        defs,
        "marker",
        {
            "id": "arrow",
            "markerWidth": "10",
            "markerHeight": "8",
            "refX": "9",
            "refY": "4",
            "orient": "auto",
            "markerUnits": "strokeWidth",
        },
    )
    SubElement(marker, "path", {"d": "M 0 0 L 10 4 L 0 8 z", "fill": "#527da3"})
    marker_dark = SubElement(
        defs,
        "marker",
        {
            "id": "arrow-dark",
            "markerWidth": "10",
            "markerHeight": "8",
            "refX": "9",
            "refY": "4",
            "orient": "auto",
            "markerUnits": "strokeWidth",
        },
    )
    SubElement(marker_dark, "path", {"d": "M 0 0 L 10 4 L 0 8 z", "fill": "#334e68"})


def box(parent, x, y, w, h, title, symbol, unit, fill, stroke):
    SubElement(
        parent,
        "rect",
        {
            "x": str(x),
            "y": str(y),
            "width": str(w),
            "height": str(h),
            "rx": "18",
            "fill": fill,
            "stroke": stroke,
            "stroke-width": "2.5",
        },
    )
    text(parent, x + w / 2, y + 37, title, size=23, weight="700", fill="#102a43")
    text(parent, x + w / 2, y + 72, symbol, size=25, weight="600", fill="#285b7a")
    text(parent, x + w / 2, y + 103, unit, size=18, fill="#627d98")


def radiometric_quantities():
    width, height = 1400, 720
    svg = Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
            "role": "img",
            "aria-label": "六个基本辐射量的定义关系",
        },
    )
    add_defs(svg)
    text(svg, width / 2, 30, "辐射量：对时间、面积与方向逐层取密度", size=28, weight="600", fill="#102a43")

    box(svg, 45, 245, 210, 125, "辐射能", "Qₑ", "J", "#eaf4ff", "#8dbce6")
    box(svg, 335, 245, 210, 125, "辐射通量", "Φₑ = dQₑ/dt", "W", "#edf8f2", "#8fceb0")

    line(svg, 265, 307, 325, 307, marker="arrow")
    text(svg, 295, 286, "时间密度", size=17, fill="#486581")

    branches = [
        (665, 90, "辐照度 / 出射度", "Eₑ / Mₑ = dΦₑ/dA", "W·m⁻²", "#fff7e8", "#e4bd70", "面积密度 dA"),
        (665, 245, "辐射强度", "Iₑ = dΦₑ/dΩ", "W·sr⁻¹", "#f7efff", "#c4a1e4", "方向密度 dΩ"),
        (665, 400, "辐亮度", "Lₑ = d²Φₑ/(dA⊥dΩ)", "W·m⁻²·sr⁻¹", "#fff0f3", "#e6a2b2", "面积与方向密度"),
    ]
    for x, y, title_value, symbol, unit, fill, stroke, label in branches:
        box(svg, x, y, 315, 125, title_value, symbol, unit, fill, stroke)
        line(svg, 555, 307, 635, y + 62, marker="arrow")
        text(svg, 595, (307 + y + 62) / 2 - 8, label, size=16, fill="#486581")

    SubElement(
        svg,
        "rect",
        {
            "x": "1040",
            "y": "150",
            "width": "310",
            "height": "310",
            "rx": "20",
            "fill": "#f5f8fa",
            "stroke": "#b8c7d1",
            "stroke-width": "2",
        },
    )
    text(svg, 1195, 193, "变量被保留到哪一步？", size=23, weight="700", fill="#102a43")
    text(svg, 1070, 240, "Eₑ / Mₑ", size=20, weight="600", anchor="start", fill="#8b5e20")
    text(svg, 1215, 240, "保留位置，积分方向", size=18, anchor="start", fill="#486581")
    text(svg, 1070, 295, "Iₑ", size=20, weight="600", anchor="start", fill="#765097")
    text(svg, 1215, 295, "保留方向，积分面积", size=18, anchor="start", fill="#486581")
    text(svg, 1070, 350, "Lₑ", size=20, weight="600", anchor="start", fill="#9a4059")
    text(svg, 1215, 350, "同时保留位置和方向", size=18, anchor="start", fill="#486581")
    text(svg, 1070, 405, "下标 λ", size=20, weight="600", anchor="start", fill="#285b7a")
    text(svg, 1215, 405, "再保留波长分辨率", size=18, anchor="start", fill="#486581")

    line(svg, 85, 590, 1315, 590, stroke="#9fb3c2", width=2)
    text(svg, width / 2, 630, "箭头表示取密度或边缘化后的定义关系，并不表示这些量可以无条件互相反演", size=20, fill="#486581")
    text(svg, width / 2, 670, "摄影中最常见的错误，是把相同单位或相近日常名称当成相同物理量", size=19, fill="#7b4b74")

    ElementTree(svg).write(SVG_DIR / "radiometric_quantities.svg", encoding="utf-8", xml_declaration=True)


def radiance_geometry():
    width, height = 1300, 650
    svg = Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
            "role": "img",
            "aria-label": "两个微小面元之间的投影面积与立体角",
        },
    )
    add_defs(svg)
    SubElement(svg, "rect", {"width": str(width), "height": str(height), "fill": "#fbfdff"})
    text(svg, width / 2, 44, "面元之间的几何传输", size=30, weight="700", fill="#102a43")

    source = [(150, 390), (245, 315), (335, 355), (240, 430)]
    receiver = [(970, 230), (1065, 290), (1010, 380), (915, 320)]
    SubElement(svg, "polygon", {"points": " ".join(f"{x},{y}" for x, y in source), "fill": "#eaf4ff", "stroke": "#6aa6d8", "stroke-width": "3"})
    SubElement(svg, "polygon", {"points": " ".join(f"{x},{y}" for x, y in receiver), "fill": "#fff0f3", "stroke": "#d98298", "stroke-width": "3"})

    sx, sy = 242, 372
    rx, ry = 990, 305
    line(svg, sx, sy, rx, ry, stroke="#334e68", width=3, marker="arrow-dark")
    text(svg, 620, 320, "距离 r", size=22, weight="600", fill="#334e68")

    line(svg, sx, sy, 180, 205, stroke="#4b8bbd", width=3, marker="arrow")
    line(svg, rx, ry, 1080, 125, stroke="#c2677e", width=3, marker="arrow")
    text(svg, 161, 188, "法线 nₛ", size=20, weight="600", fill="#356f9d")
    text(svg, 1105, 113, "法线 nᵣ", size=20, weight="600", fill="#a94e66")

    line(svg, sx, sy, 930, 230, stroke="#8aa4b8", width=2, dash="9 7")
    line(svg, sx, sy, 1010, 380, stroke="#8aa4b8", width=2, dash="9 7")
    text(svg, 820, 230, "接收面元张开的 dΩᵣ", size=19, fill="#627d98")

    SubElement(svg, "path", {"d": "M 226 329 A 48 48 0 0 0 198 337", "fill": "none", "stroke": "#4b8bbd", "stroke-width": "3"})
    SubElement(svg, "path", {"d": "M 955 280 A 48 48 0 0 1 1012 263", "fill": "none", "stroke": "#c2677e", "stroke-width": "3"})
    text(svg, 192, 315, "θₛ", size=20, weight="600", fill="#356f9d")
    text(svg, 1008, 245, "θᵣ", size=20, weight="600", fill="#a94e66")

    text(svg, 237, 478, "源面元 dAₛ", size=22, weight="700", fill="#285b7a")
    text(svg, 1000, 430, "接收面元 dAᵣ", size=22, weight="700", fill="#9a4059")

    SubElement(svg, "rect", {"x": "170", "y": "520", "width": "960", "height": "82", "rx": "16", "fill": "#f1f7fb", "stroke": "#b8ccda", "stroke-width": "2"})
    text(svg, 650, 555, "dΩᵣ = cosθᵣ dAᵣ / r²", size=25, weight="600", fill="#234e70")
    text(svg, 650, 588, "d²Φ = Lₛ cosθₛ cosθᵣ dAₛ dAᵣ / r²", size=25, weight="600", fill="#7b3651")

    ElementTree(svg).write(SVG_DIR / "radiance_geometry.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    radiometric_quantities()
    radiance_geometry()


if __name__ == "__main__":
    main()
