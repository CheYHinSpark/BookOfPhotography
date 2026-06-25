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
    for marker_id, color in (("arrow-blue", "#3b82b5"), ("arrow-red", "#c85b73"), ("arrow-dark", "#334e68")):
        marker = SubElement(
            defs,
            "marker",
            {
                "id": marker_id,
                "markerWidth": "10",
                "markerHeight": "8",
                "refX": "9",
                "refY": "4",
                "orient": "auto",
                "markerUnits": "strokeWidth",
            },
        )
        SubElement(marker, "path", {"d": "M 0 0 L 10 4 L 0 8 z", "fill": color})


def base_svg(width, height, label):
    svg = Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
            "role": "img",
            "aria-label": label,
        },
    )
    add_defs(svg)
    SubElement(svg, "rect", {"width": str(width), "height": str(height), "fill": "#fbfdff"})
    return svg


def fermat_snell():
    width, height = 1300, 700
    svg = base_svg(width, height, "费马原理与斯涅尔折射定律")
    text(svg, width / 2, 46, "驻光程在界面处给出折射定律", size=30, weight="700", fill="#102a43")

    interface_y = 350
    line(svg, 90, interface_y, 1210, interface_y, stroke="#829ab1", width=3)
    text(svg, 1160, 324, "介质界面", size=19, fill="#627d98")
    text(svg, 1140, 135, "n₁", size=26, weight="700", fill="#2f6f9f")
    text(svg, 1140, 565, "n₂", size=26, weight="700", fill="#a24862")

    ax, ay = 190, 105
    bx, by = 1090, 585
    px, py = 600, interface_y
    line(svg, ax, ay, px, py, stroke="#3b82b5", width=4, marker="arrow-blue")
    line(svg, px, py, bx, by, stroke="#c85b73", width=4, marker="arrow-red")
    SubElement(svg, "circle", {"cx": str(ax), "cy": str(ay), "r": "8", "fill": "#285b7a"})
    SubElement(svg, "circle", {"cx": str(px), "cy": str(py), "r": "8", "fill": "#334e68"})
    SubElement(svg, "circle", {"cx": str(bx), "cy": str(by), "r": "8", "fill": "#9a4059"})
    text(svg, ax - 20, ay - 24, "A", size=24, weight="700")
    text(svg, px, py - 24, "P(x)", size=23, weight="700")
    text(svg, bx + 23, by + 7, "B", size=24, weight="700")

    line(svg, px, 120, px, 585, stroke="#73899b", width=2, dash="10 8")
    text(svg, px + 28, 135, "法线", size=18, fill="#627d98", anchor="start")

    SubElement(svg, "path", {"d": "M 600 292 A 58 58 0 0 0 552 318", "fill": "none", "stroke": "#3b82b5", "stroke-width": "3"})
    SubElement(svg, "path", {"d": "M 600 408 A 58 58 0 0 1 651 378", "fill": "none", "stroke": "#c85b73", "stroke-width": "3"})
    text(svg, 548, 287, "θ₁", size=22, weight="600", fill="#2f6f9f")
    text(svg, 657, 414, "θ₂", size=22, weight="600", fill="#a24862")

    line(svg, ax, 80, ax, interface_y, stroke="#aac0d1", width=2, dash="6 7")
    line(svg, bx, interface_y, bx, 615, stroke="#d7a9b5", width=2, dash="6 7")
    text(svg, ax - 30, 235, "a", size=22, weight="600", fill="#486581")
    text(svg, bx + 28, 485, "b", size=22, weight="600", fill="#7b4b74")
    line(svg, ax, 655, bx, 655, stroke="#334e68", width=2)
    line(svg, ax, 640, ax, 670, stroke="#334e68", width=2)
    line(svg, bx, 640, bx, 670, stroke="#334e68", width=2)
    text(svg, (ax + bx) / 2, 685, "水平间隔 D", size=21, weight="600")
    text(svg, 370, 380, "x", size=21, weight="600", fill="#334e68")
    text(svg, 845, 380, "D - x", size=21, weight="600", fill="#334e68")

    text(svg, 330, 160, "光程 n₁·AP", size=20, weight="600", fill="#2f6f9f")
    text(svg, 865, 520, "光程 n₂·PB", size=20, weight="600", fill="#a24862")
    ElementTree(svg).write(SVG_DIR / "fermat_snell.svg", encoding="utf-8", xml_declaration=True)


def thin_lens_imaging():
    width, height = 1300, 690
    svg = base_svg(width, height, "薄会聚透镜的近轴成像")
    text(svg, width / 2, 45, "薄透镜：三条特征光线与同一共轭像点", size=30, weight="700", fill="#102a43")

    axis_y = 350
    lens_x = 650
    object_x = 300
    image_x = 945
    object_top = 160
    image_tip = 510
    f_px = 160
    line(svg, 80, axis_y, 1215, axis_y, stroke="#829ab1", width=2, marker="arrow-dark")
    text(svg, 1190, axis_y - 18, "光轴 z", size=20, fill="#627d98")

    lens_path = f"M {lens_x} 85 C {lens_x-62} 155 {lens_x-62} 545 {lens_x} 615 C {lens_x+62} 545 {lens_x+62} 155 {lens_x} 85 Z"
    SubElement(svg, "path", {"d": lens_path, "fill": "#eaf4ff", "fill-opacity": "0.8", "stroke": "#5595c5", "stroke-width": "3"})
    line(svg, lens_x, 90, lens_x, 610, stroke="#3b82b5", width=2, dash="8 7")
    text(svg, lens_x, 647, "薄透镜平面", size=20, weight="600", fill="#2f6f9f")

    front_f = lens_x - f_px
    back_f = lens_x + f_px
    for x, label in ((front_f, "F"), (back_f, "F′")):
        line(svg, x, axis_y - 10, x, axis_y + 10, stroke="#334e68", width=3)
        text(svg, x, axis_y + 38, label, size=22, weight="700")

    line(svg, object_x, axis_y, object_x, object_top, stroke="#285b7a", width=5, marker="arrow-blue")
    text(svg, object_x - 8, object_top - 25, "物体 yₒ", size=22, weight="700", fill="#285b7a")
    line(svg, image_x, axis_y, image_x, image_tip, stroke="#9a4059", width=5, marker="arrow-red")
    text(svg, image_x + 18, image_tip + 30, "倒立实像 yᵢ", size=22, weight="700", fill="#9a4059")

    # Parallel ray, then through image-side focus.
    line(svg, object_x, object_top, lens_x, object_top, stroke="#3b82b5", width=3)
    line(svg, lens_x, object_top, image_x, image_tip, stroke="#3b82b5", width=3)
    # Central ray.
    line(svg, object_x, object_top, image_x, image_tip, stroke="#5f8f72", width=3)
    # Through front focus, then parallel.
    line(svg, object_x, object_top, lens_x, image_tip, stroke="#c58a2d", width=3)
    line(svg, lens_x, image_tip, image_x, image_tip, stroke="#c58a2d", width=3)

    line(svg, object_x, 610, lens_x, 610, stroke="#334e68", width=2)
    line(svg, object_x, 598, object_x, 622, stroke="#334e68", width=2)
    line(svg, lens_x, 598, lens_x, 622, stroke="#334e68", width=2)
    text(svg, (object_x + lens_x) / 2, 642, "s = −zₒ", size=21, weight="600")
    line(svg, lens_x, 610, image_x, 610, stroke="#334e68", width=2)
    line(svg, image_x, 598, image_x, 622, stroke="#334e68", width=2)
    text(svg, (lens_x + image_x) / 2, 642, "s′ = zᵢ", size=21, weight="600")

    text(svg, 640, 78, "1/zᵢ - 1/zₒ = 1/f", size=23, weight="600", fill="#7b3651")
    ElementTree(svg).write(SVG_DIR / "thin_lens_imaging.svg", encoding="utf-8", xml_declaration=True)


def aperture_pupils():
    width, height = 1350, 680
    svg = base_svg(width, height, "孔径光阑与入瞳出瞳")
    axis_y = 290
    line(svg, 70, axis_y, 1280, axis_y, stroke="#9fb3c2", width=2, marker="arrow-dark")
    text(svg, 105, axis_y - 30, "物方", size=19, weight="600", fill="#627d98")
    text(svg, 1245, axis_y - 30, "像方", size=19, weight="600", fill="#627d98")

    # Optical groups.
    for x, label, color in ((360, "前透镜组", "#5a9bcc"), (860, "后透镜组", "#8d6bb4")):
        SubElement(svg, "path", {"d": f"M {x} 85 C {x-45} 155 {x-45} 425 {x} 495 C {x+45} 425 {x+45} 155 {x} 85 Z", "fill": "#eef6fb" if x < 600 else "#f5effb", "stroke": color, "stroke-width": "3"})
        text(svg, x, 535, label, size=21, weight="700", fill=color)

    stop_x = 650
    line(svg, stop_x, 70, stop_x, 190, stroke="#334e68", width=8)
    line(svg, stop_x, 390, stop_x, 510, stroke="#334e68", width=8)
    text(svg, stop_x, 48, "孔径光阑", size=22, weight="700")
    text(svg, stop_x, 325, "真实机械开口", size=18, fill="#627d98")

    # Virtual pupil images.
    SubElement(svg, "ellipse", {"cx": "480", "cy": str(axis_y), "rx": "22", "ry": "118", "fill": "none", "stroke": "#2f7ba8", "stroke-width": "4", "stroke-dasharray": "12 8"})
    text(svg, 480, 122, "入瞳", size=24, weight="700", fill="#2f7ba8")
    text(svg, 480, 154, "物方看到的光阑像", size=18, weight="600", fill="#2f7ba8")
    SubElement(svg, "ellipse", {"cx": "1025", "cy": str(axis_y), "rx": "24", "ry": "138", "fill": "none", "stroke": "#a24862", "stroke-width": "4", "stroke-dasharray": "12 8"})
    text(svg, 1025, 112, "出瞳", size=24, weight="700", fill="#a24862")
    text(svg, 1025, 144, "像方看到的光阑像", size=18, weight="600", fill="#a24862")

    line(svg, 430, axis_y - 118, 430, axis_y + 118, stroke="#2f7ba8", width=2)
    line(svg, 420, axis_y - 118, 440, axis_y - 118, stroke="#2f7ba8", width=2)
    line(svg, 420, axis_y + 118, 440, axis_y + 118, stroke="#2f7ba8", width=2)
    text(svg, 405, axis_y + 5, "Dₑₙ", size=20, weight="600", fill="#2f7ba8")
    line(svg, 1070, axis_y - 138, 1070, axis_y + 138, stroke="#a24862", width=2)
    line(svg, 1060, axis_y - 138, 1080, axis_y - 138, stroke="#a24862", width=2)
    line(svg, 1060, axis_y + 138, 1080, axis_y + 138, stroke="#a24862", width=2)
    text(svg, 1100, axis_y + 5, "Dₑₓ", size=20, weight="600", fill="#a24862")

    text(svg, 120, 200, "从物方看进去", size=20, weight="600", fill="#2f7ba8")
    line(svg, 130, 225, 454, axis_y - 118, stroke="#3b82b5", width=3, marker="arrow-blue")
    line(svg, 130, 355, 454, axis_y + 118, stroke="#3b82b5", width=3)
    line(svg, 506, axis_y - 118, stop_x, 190, stroke="#3b82b5", width=2, dash="8 6")
    line(svg, 506, axis_y + 118, stop_x, 390, stroke="#3b82b5", width=2, dash="8 6")
    text(svg, 1220, 200, "从像方看回来", size=20, weight="600", fill="#a24862")
    line(svg, 1210, 225, 1052, axis_y - 138, stroke="#c85b73", width=3, marker="arrow-red")
    line(svg, 1210, 355, 1052, axis_y + 138, stroke="#c85b73", width=3)
    line(svg, 998, axis_y - 138, stop_x, 190, stroke="#c85b73", width=2, dash="8 6")
    line(svg, 998, axis_y + 138, stop_x, 390, stroke="#c85b73", width=2, dash="8 6")

    text(svg, 675, 600, "虚线椭圆是同一个孔径光阑经前后镜组形成的像，位置和直径可与机械开口不同", size=19, fill="#627d98")

    ElementTree(svg).write(SVG_DIR / "aperture_pupils.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    fermat_snell()
    thin_lens_imaging()
    aperture_pupils()


if __name__ == "__main__":
    main()
