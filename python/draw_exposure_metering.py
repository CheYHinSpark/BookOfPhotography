from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
import math


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"
FONT = "Source Han Sans SC, Microsoft YaHei, sans-serif"


def text(parent, x, y, value, size=24, weight="400", fill="#243b53", anchor="middle"):
    node = SubElement(parent, "text", {
        "x": str(x), "y": str(y), "text-anchor": anchor,
        "font-family": FONT, "font-size": str(size),
        "font-weight": weight, "fill": fill,
    })
    node.text = value
    return node


def line(parent, x1, y1, x2, y2, stroke="#527da3", width=3, dash=None, marker=None):
    attrs = {
        "x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2),
        "stroke": stroke, "stroke-width": str(width), "stroke-linecap": "round",
    }
    if dash:
        attrs["stroke-dasharray"] = dash
    if marker:
        attrs["marker-end"] = f"url(#{marker})"
    return SubElement(parent, "line", attrs)


def polyline(parent, points, stroke="#527da3", width=3, fill="none", dash=None):
    attrs = {
        "points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points),
        "stroke": stroke, "stroke-width": str(width), "fill": fill,
        "stroke-linejoin": "round", "stroke-linecap": "round",
    }
    if dash:
        attrs["stroke-dasharray"] = dash
    return SubElement(parent, "polyline", attrs)


def add_defs(svg):
    defs = SubElement(svg, "defs")
    for marker_id, color in (
        ("arrow-blue", "#3b82b5"), ("arrow-dark", "#334e68"),
        ("arrow-red", "#c85b73"), ("arrow-green", "#4d8c6a"),
    ):
        marker = SubElement(defs, "marker", {
            "id": marker_id, "markerWidth": "10", "markerHeight": "8",
            "refX": "9", "refY": "4", "orient": "auto",
            "markerUnits": "strokeWidth",
        })
        SubElement(marker, "path", {"d": "M 0 0 L 10 4 L 0 8 z", "fill": color})


def base_svg(width, height, label):
    svg = Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg", "width": str(width),
        "height": str(height), "viewBox": f"0 0 {width} {height}",
        "role": "img", "aria-label": label,
    })
    add_defs(svg)
    SubElement(svg, "rect", {"width": str(width), "height": str(height), "fill": "#fbfdff"})
    return svg


def rounded_box(parent, x, y, w, h, fill, stroke, title, subtitle, title_color="#102a43"):
    SubElement(parent, "rect", {
        "x": str(x), "y": str(y), "width": str(w), "height": str(h),
        "rx": "18", "fill": fill, "stroke": stroke, "stroke-width": "2.5",
    })
    text(parent, x + w / 2, y + 55, title, size=25, weight="700", fill=title_color)
    text(parent, x + w / 2, y + 94, subtitle, size=18, fill="#486581")


def exposure_chain():
    width, height = 1500, 560
    svg = base_svg(width, height, "从场景辐亮度到光电子的曝光链")
    text(svg, width / 2, 43, "曝光不是亮度旋钮，而是一条有单位的积分链", size=31, weight="700", fill="#102a43")
    boxes = [
        (35, "场景辐亮度", "L(λ,x,ω)", "#eaf4ff", "#9bc7ee"),
        (330, "孔径与透过", "τ(λ) / N²", "#fff7e8", "#e8c77d"),
        (625, "像面辐照度", "E(λ,x)", "#edf8f2", "#9fd6b7"),
        (920, "时间积分", "H = ∫ E dt", "#f7efff", "#c9a9e8"),
        (1215, "光电子期望", "μₑ = ∫ ηHλ/(hc)dλ", "#fff0f3", "#eab0be"),
    ]
    for x, title_value, subtitle, fill, stroke in boxes:
        rounded_box(svg, x, 125, 250, 145, fill, stroke, title_value, subtitle)
    for x in (285, 580, 875, 1170):
        line(svg, x + 8, 197, x + 38, 197, stroke="#527da3", width=3, marker="arrow-blue")
    text(svg, 750, 330, "每一级都可能随位置、方向、波长和时间变化", size=22, weight="700", fill="#3d6f99")
    line(svg, 130, 390, 1370, 390, stroke="#c6d2dc", width=2)
    notes = [
        (160, "场景不由相机参数改变"),
        (455, "f 数控制方向锥体"),
        (750, "W·m⁻² 或光谱密度"),
        (1045, "J·m⁻²；快门波形参与"),
        (1330, "泊松涨落从这里出现"),
    ]
    for x, value in notes:
        SubElement(svg, "circle", {"cx": str(x), "cy": "390", "r": "7", "fill": "#527da3"})
        text(svg, x, 430, value, size=17, fill="#627d98")
    text(svg, width / 2, 510, "显示明度与 JPEG 数值位于这条链之后，不能倒过来定义物理曝光", size=21, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "exposure_chain.svg", encoding="utf-8", xml_declaration=True)


def image_irradiance_controls():
    width, height = 1450, 660
    svg = base_svg(width, height, "f 数透过率与离轴衰减对像面照度的作用")
    text(svg, width / 2, 43, "像面照度的三个乘法因子", size=31, weight="700", fill="#102a43")
    line(svg, 725, 82, 725, 590, stroke="#d7e0e7", width=2)
    # Left: inverse-square aperture curve.
    text(svg, 360, 92, "轴上：E ∝ τ / N²", size=24, weight="700", fill="#285b7a")
    l, r, t, b = 100, 660, 145, 535
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    apertures = [1.4, 2, 2.8, 4, 5.6, 8, 11]
    vals = [(1.4 / n) ** 2 for n in apertures]
    pts = []
    for idx, (n, val) in enumerate(zip(apertures, vals)):
        x = l + 35 + (r - l - 70) * idx / (len(apertures) - 1)
        y = b - (b - t - 35) * val
        pts.append((x, y))
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "7", "fill": "#3b82b5"})
        text(svg, x, b + 32, f"f/{n:g}", size=16, fill="#627d98")
        if idx < 4:
            text(svg, x, y - 17, f"{val:.2f}", size=15, fill="#285b7a")
    polyline(svg, pts, stroke="#3b82b5", width=4)
    text(svg, l - 25, t + 5, "相对 E", size=17, fill="#627d98")
    text(svg, 360, 585, "相邻整档 f 数乘 √2，照度减半", size=19, fill="#486581")
    # Right: off-axis factors.
    text(svg, 1085, 92, "离轴：cos⁴θ × V(h,λ)", size=24, weight="700", fill="#397456")
    l2, r2, t2, b2 = 805, 1370, 145, 535
    line(svg, l2, b2, r2, b2, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l2, b2, l2, t2, stroke="#334e68", width=2, marker="arrow-dark")
    curves = [
        ("仅 cos⁴θ", "#3b82b5", lambda u: math.cos(math.radians(45 * u)) ** 4, None),
        ("含机械渐晕", "#c85b73", lambda u: math.cos(math.radians(45 * u)) ** 4 * (1 - 0.42 * u ** 3), "10 7"),
        ("数字补偿后", "#4d8c6a", lambda u: max(0, min(1.05, 1 - 0.10 * u ** 2)), None),
    ]
    for label, color, func, dash in curves:
        pts = []
        for j in range(200):
            u = j / 199
            value = func(u)
            pts.append((l2 + (r2 - l2) * u, b2 - (b2 - t2) * value))
        polyline(svg, pts, stroke=color, width=4, dash=dash)
    text(svg, 1060, 235, "数字补偿后", size=17, weight="700", fill="#397456")
    text(svg, 1110, 325, "仅 cos⁴θ", size=17, weight="700", fill="#285b7a")
    text(svg, 1155, 425, "含机械渐晕", size=17, weight="700", fill="#a24862")
    text(svg, r2, b2 + 34, "归一化像高 h", size=17, fill="#627d98")
    text(svg, l2 - 25, t2 + 5, "相对 E", size=17, fill="#627d98")
    text(svg, 1085, 585, "补偿能抬高数值，也会同时放大边缘噪声", size=19, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "image_irradiance_controls.svg", encoding="utf-8", xml_declaration=True)


def ev_lattice():
    width, height = 1450, 720
    svg = base_svg(width, height, "光圈值快门值与 EV 的对数格点")
    text(svg, width / 2, 43, "APEX 把乘法曝光关系变成加法格点", size=31, weight="700", fill="#102a43")
    l, r, t, b = 180, 1320, 130, 610
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    tvs = list(range(5, 12))
    avs = list(range(1, 9))
    shutter_labels = {5: "1/32", 6: "1/64", 7: "1/128", 8: "1/256", 9: "1/512", 10: "1/1024", 11: "1/2048"}
    aperture_labels = {1: "f/1.4", 2: "f/2", 3: "f/2.8", 4: "f/4", 5: "f/5.6", 6: "f/8", 7: "f/11", 8: "f/16"}
    def xp(tv): return l + (r - l) * (tv - 5) / 6
    def yp(av): return b - (b - t) * (av - 1) / 7
    for tv in tvs:
        x = xp(tv)
        line(svg, x, t, x, b, stroke="#dbe3e9", width=1.4)
        text(svg, x, b + 35, shutter_labels[tv], size=17, fill="#627d98")
        text(svg, x, b + 61, f"Tᵥ={tv}", size=14, fill="#8aa0b2")
    for av in avs:
        y = yp(av)
        line(svg, l, y, r, y, stroke="#dbe3e9", width=1.4)
        text(svg, l - 26, y + 6, aperture_labels[av], size=17, fill="#627d98", anchor="end")
    colors = {9: "#9a7bb8", 11: "#3b82b5", 13: "#4d8c6a", 15: "#c58a2d", 17: "#c85b73"}
    for ev, color in colors.items():
        pts = []
        for tv in [5 + 6 * j / 120 for j in range(121)]:
            av = ev - tv
            if 1 <= av <= 8:
                pts.append((xp(tv), yp(av)))
        if len(pts) > 1:
            polyline(svg, pts, stroke=color, width=5)
            xlab, ylab = pts[-1]
            text(svg, min(xlab + 15, r - 5), ylab - 14, f"EV {ev}", size=18, weight="700", fill=color, anchor="end")
    # Highlight one equivalence diagonal.
    for tv, av in ((5, 8), (6, 7), (7, 6), (8, 5), (9, 4), (10, 3), (11, 2)):
        SubElement(svg, "circle", {"cx": str(xp(tv)), "cy": str(yp(av)), "r": "8", "fill": "#4d8c6a"})
    text(svg, width / 2, 680, "沿同一条 EV 线移动：快门少一档，光圈多一档；H 近似不变，但运动与景深会改变", size=21, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "ev_lattice.svg", encoding="utf-8", xml_declaration=True)


def reciprocity_limits():
    width, height = 1450, 600
    svg = base_svg(width, height, "相同能量曝光与摄影结果不等价")
    text(svg, width / 2, 43, "互易律只约束积分量，不保证图像等价", size=31, weight="700", fill="#102a43")
    line(svg, 725, 85, 725, 530, stroke="#d7e0e7", width=2)
    text(svg, 360, 92, "理想静态线性探测：E₁t₁ = E₂t₂", size=23, weight="700", fill="#285b7a")
    # Equal-area rectangles.
    for x, w, h, color, label in (
        (105, 140, 300, "#3b82b5", "强光 × 短时"),
        (390, 280, 150, "#69a87f", "弱光 × 长时"),
    ):
        y = 480 - h
        SubElement(svg, "rect", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "fill": color, "fill-opacity": ".45", "stroke": color, "stroke-width": "3"})
        text(svg, x + w / 2, 510, label, size=18, weight="700", fill=color)
    text(svg, 360, 150, "矩形面积相同 → H 相同", size=19, fill="#486581")
    # Right: failure modes.
    text(svg, 1085, 92, "摄影结果仍可能不同", size=23, weight="700", fill="#a24862")
    items = [
        (840, 175, "运动积分", "轨迹长度 ∝ t", "#c85b73"),
        (1110, 175, "闪烁照明", "E(t) 非常数", "#c58a2d"),
        (840, 350, "暗电流/温升", "额外电子随时间积累", "#7b4b74"),
        (1110, 350, "快门与饱和", "门函数、峰值受限", "#4d8c6a"),
    ]
    for x, y, title_value, subtitle, color in items:
        SubElement(svg, "rect", {"x": str(x), "y": str(y), "width": "230", "height": "120", "rx": "16", "fill": color, "fill-opacity": ".10", "stroke": color, "stroke-width": "2.5"})
        text(svg, x + 115, y + 45, title_value, size=21, weight="700", fill=color)
        text(svg, x + 115, y + 82, subtitle, size=16, fill="#486581")
    ElementTree(svg).write(SVG_DIR / "reciprocity_limits.svg", encoding="utf-8", xml_declaration=True)


def metering_geometries():
    width, height = 1450, 650
    svg = base_svg(width, height, "入射式与反射式测光的几何差异")
    text(svg, width / 2, 43, "两种测光测量的是不同位置、不同方向集合", size=31, weight="700", fill="#102a43")
    line(svg, 725, 82, 725, 575, stroke="#d7e0e7", width=2)
    # Incident side.
    text(svg, 360, 92, "入射式：在主体处估计入射照度", size=23, weight="700", fill="#397456")
    SubElement(svg, "circle", {"cx": "150", "cy": "190", "r": "38", "fill": "#ffe8a3", "stroke": "#c58a2d", "stroke-width": "3"})
    text(svg, 150, 197, "光源", size=18, weight="700", fill="#8a5f19")
    SubElement(svg, "rect", {"x": "510", "y": "270", "width": "90", "height": "185", "rx": "8", "fill": "#c6d8e6", "stroke": "#527da3", "stroke-width": "3"})
    text(svg, 555, 485, "主体", size=18, weight="700", fill="#285b7a")
    for y in (175, 225, 275, 325):
        line(svg, 195, y, 500, 300 + 0.18 * (y - 250), stroke="#c58a2d", width=2.4, marker="arrow-red")
    SubElement(svg, "path", {"d": "M 440 350 A 65 65 0 0 1 570 350 L 505 350 Z", "fill": "#edf8f2", "stroke": "#4d8c6a", "stroke-width": "3"})
    text(svg, 505, 380, "半球受光头", size=16, weight="700", fill="#397456")
    text(svg, 360, 550, "不直接看到主体反射率与镜面高光", size=19, fill="#486581")
    # Reflected side.
    text(svg, 1085, 92, "反射式：从相机方向估计出射亮度", size=23, weight="700", fill="#285b7a")
    SubElement(svg, "circle", {"cx": "860", "cy": "190", "r": "38", "fill": "#ffe8a3", "stroke": "#c58a2d", "stroke-width": "3"})
    text(svg, 860, 197, "光源", size=18, weight="700", fill="#8a5f19")
    SubElement(svg, "rect", {"x": "1000", "y": "260", "width": "105", "height": "200", "rx": "8", "fill": "#d6b7a5", "stroke": "#9a6d55", "stroke-width": "3"})
    text(svg, 1052, 490, "ρ · BRDF", size=18, weight="700", fill="#7b4b3a")
    line(svg, 900, 220, 1000, 300, stroke="#c58a2d", width=3, marker="arrow-red")
    # Camera.
    SubElement(svg, "rect", {"x": "1260", "y": "300", "width": "120", "height": "90", "rx": "12", "fill": "#eaf4ff", "stroke": "#3b82b5", "stroke-width": "3"})
    SubElement(svg, "circle", {"cx": "1260", "cy": "345", "r": "27", "fill": "#d9ecfb", "stroke": "#285b7a", "stroke-width": "3"})
    text(svg, 1320, 430, "相机/反射式表", size=17, weight="700", fill="#285b7a")
    for y in (300, 340, 380, 420):
        line(svg, 1110, y, 1225, 345 + 0.18 * (y - 360), stroke="#3b82b5", width=2.4, marker="arrow-blue")
    text(svg, 1085, 550, "观测到照明 × 反射 × 方向性的乘积", size=19, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "metering_geometries.svg", encoding="utf-8", xml_declaration=True)


def metering_objectives():
    width, height = 1500, 680
    svg = base_svg(width, height, "中间调优先与高光优先测光的目标函数")
    text(svg, width / 2, 43, "同一场景分布，不同损失函数给出不同曝光", size=31, weight="700", fill="#102a43")
    line(svg, 750, 82, 750, 610, stroke="#d7e0e7", width=2)
    panels = [
        (375, "中间调优先", "把加权几何均值映射到目标码值", "#3b82b5", 0.90),
        (1125, "高光优先", "让高分位数停在饱和阈值之前", "#c85b73", 0.63),
    ]
    for cx, title_value, subtitle, color, scale in panels:
        text(svg, cx, 95, title_value, size=24, weight="700", fill=color)
        text(svg, cx, 125, subtitle, size=17, fill="#627d98")
        l, r, t, b = cx - 285, cx + 285, 180, 510
        line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
        line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
        # Three-mode log-luminance distribution.
        pts = []
        for j in range(240):
            x = -5 + 10 * j / 239
            y = (0.80 * math.exp(-0.5 * ((x + 1.8) / 1.25) ** 2)
                 + 0.42 * math.exp(-0.5 * ((x - 1.2) / 0.65) ** 2)
                 + 0.10 * math.exp(-0.5 * ((x - 3.5) / 0.35) ** 2))
            px = l + (r - l) * j / 239
            py = b - (b - t) * y / 0.85
            pts.append((px, py))
        polyline(svg, pts, stroke="#627d98", width=3, fill="none")
        # Mapping positions.
        sat_x = l + (r - l) * (0.5 + scale * 0.42)
        mid_x = l + (r - l) * (0.5 - (1 - scale) * 0.25)
        line(svg, sat_x, t, sat_x, b, stroke=color, width=4, dash="9 7")
        line(svg, mid_x, 300, mid_x, b, stroke="#4d8c6a", width=3)
        text(svg, sat_x - 8, t + 20, "饱和界", size=17, weight="700", fill=color, anchor="end")
        text(svg, mid_x, 550, "目标中间调", size=16, weight="700", fill="#397456")
        text(svg, l, b + 35, "暗部", size=16, fill="#627d98", anchor="start")
        text(svg, r, b + 35, "高光", size=16, fill="#627d98", anchor="end")
    text(svg, width / 2, 645, "相机若不知道哪些区域属于主体，就不能从物理量自动推出唯一“正确曝光”", size=21, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "metering_objectives.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    exposure_chain()
    image_irradiance_controls()
    ev_lattice()
    reciprocity_limits()
    metering_geometries()
    metering_objectives()


if __name__ == "__main__":
    main()
