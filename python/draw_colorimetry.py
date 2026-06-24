from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
import math


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"
FONT = "Source Han Sans SC, Microsoft YaHei, sans-serif"


def text(parent, x, y, value, size=22, weight="400", fill="#243b53", anchor="middle"):
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


def polygon(parent, points, fill, stroke="none", width=1, opacity=None):
    attrs = {
        "points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points),
        "fill": fill, "stroke": stroke, "stroke-width": str(width),
        "stroke-linejoin": "round",
    }
    if opacity is not None:
        attrs["fill-opacity"] = str(opacity)
    return SubElement(parent, "polygon", attrs)


def path(parent, d, stroke="#527da3", width=3, fill="none", opacity=None):
    attrs = {"d": d, "stroke": stroke, "stroke-width": str(width), "fill": fill, "stroke-linejoin": "round", "stroke-linecap": "round"}
    if opacity is not None:
        attrs["fill-opacity"] = str(opacity)
    return SubElement(parent, "path", attrs)


def add_defs(svg):
    defs = SubElement(svg, "defs")
    for marker_id, color in (
        ("arrow-blue", "#3b82b5"), ("arrow-dark", "#334e68"),
        ("arrow-red", "#c85b73"), ("arrow-green", "#4d8c6a"),
        ("arrow-gold", "#c58a2d"), ("arrow-purple", "#7b4b74"),
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


def rounded_box(parent, x, y, w, h, fill, stroke, title_value, subtitle=None, title_color="#102a43"):
    SubElement(parent, "rect", {
        "x": str(x), "y": str(y), "width": str(w), "height": str(h),
        "rx": "16", "fill": fill, "stroke": stroke, "stroke-width": "2.5",
    })
    text(parent, x + w / 2, y + 42, title_value, size=21, weight="700", fill=title_color)
    if subtitle:
        text(parent, x + w / 2, y + 77, subtitle, size=16, fill="#486581")


def axes(parent, l, r, t, b, x_label=None, y_label=None):
    line(parent, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(parent, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    if x_label:
        text(parent, r, b + 32, x_label, size=15, fill="#627d98", anchor="end")
    if y_label:
        text(parent, l - 5, t - 12, y_label, size=15, fill="#627d98", anchor="start")


def spectral_to_tristimulus():
    width, height = 1500, 720
    svg = base_svg(width, height, "光谱经三类响应函数积分成为三刺激值")
    text(svg, width / 2, 43, "颜色测量把无限维光谱投影为三个线性响应", size=31, weight="700", fill="#102a43")
    # Spectrum panel.
    rounded_box(svg, 35, 115, 335, 430, "#f4f9fd", "#9bc7ee", "入眼光谱 s(λ)", "物理量：随波长连续变化", "#285b7a")
    l, r, t, b = 75, 335, 210, 460
    axes(svg, l, r, t, b, "λ", None)
    pts = []
    for j in range(161):
        u = j / 160
        value = 0.18 + 0.55 * math.exp(-((u - 0.32) / 0.18) ** 2) + 0.38 * math.exp(-((u - 0.72) / 0.11) ** 2)
        pts.append((l + (r - l) * u, b - 180 * value))
    polyline(svg, pts, stroke="#3b82b5", width=5)
    text(svg, 205, 510, "一个函数：自由度远多于 3", size=17, weight="700", fill="#7b4b74")
    line(svg, 375, 330, 435, 330, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Cone weighting panel.
    rounded_box(svg, 440, 115, 420, 430, "#fffaf1", "#e8c77d", "三类光谱灵敏度", "L、M、S 锥体或等价配色函数", "#8a5f19")
    l2, r2, t2, b2 = 485, 820, 220, 455
    axes(svg, l2, r2, t2, b2, "λ", None)
    curves = [
        (0.72, 0.19, "L", "#c85b73"),
        (0.55, 0.17, "M", "#4d8c6a"),
        (0.25, 0.12, "S", "#3b82b5"),
    ]
    for center, sigma, label, color in curves:
        pts = []
        for j in range(151):
            u = j / 150
            value = math.exp(-0.5 * ((u - center) / sigma) ** 2)
            pts.append((l2 + (r2 - l2) * u, b2 - 175 * value))
        polyline(svg, pts, stroke=color, width=4)
        text(svg, l2 + (r2 - l2) * center, b2 - 190, label, size=18, weight="700", fill=color)
    text(svg, 650, 510, "每个响应 = ∫s(λ)qᵢ(λ)dλ", size=17, weight="700", fill="#7b4b74")
    line(svg, 865, 330, 925, 330, stroke="#3b82b5", width=4, marker="arrow-blue")
    # LMS and XYZ.
    rounded_box(svg, 930, 115, 250, 430, "#edf8f2", "#9fd6b7", "三刺激向量", "只保留三个内积", "#397456")
    for idx, (label, color) in enumerate((("L", "#c85b73"), ("M", "#4d8c6a"), ("S", "#3b82b5"))):
        y = 245 + idx * 92
        SubElement(svg, "circle", {"cx": "1005", "cy": str(y), "r": "24", "fill": color, "fill-opacity": "0.22", "stroke": color, "stroke-width": "3"})
        text(svg, 1005, y + 7, label, size=22, weight="700", fill=color)
        text(svg, 1060, y + 6, f"t{idx + 1}", size=18, fill="#486581", anchor="start")
    line(svg, 1185, 330, 1245, 330, stroke="#3b82b5", width=4, marker="arrow-blue")
    rounded_box(svg, 1250, 115, 215, 430, "#f7efff", "#c9a9e8", "坐标变换", "LMS ↔ XYZ ↔ RGB", "#7b4b74")
    text(svg, 1357, 270, "[X Y Z]ᵀ", size=25, weight="700", fill="#7b4b74")
    line(svg, 1300, 305, 1415, 305, stroke="#9a79b1", width=2)
    text(svg, 1357, 355, "x = X/(X+Y+Z)", size=17, fill="#486581")
    text(svg, 1357, 395, "y = Y/(X+Y+Z)", size=17, fill="#486581")
    text(svg, 1357, 475, "尺度被色度归一化消去", size=15, fill="#a24862")
    rounded_box(svg, 130, 605, 1240, 72, "#eef5fb", "#a8c8e0", "tᵢ = k∫s(λ)qᵢ(λ)dλ：投影是线性的；XYZ 不是新的光谱，而是同一三维响应空间的一组坐标", None, "#285b7a")
    ElementTree(svg).write(SVG_DIR / "spectral_to_tristimulus.svg", encoding="utf-8", xml_declaration=True)


def metamer_nullspace():
    width, height = 1500, 720
    svg = base_svg(width, height, "不同光谱落入三刺激映射同一输出形成同色异谱")
    text(svg, width / 2, 43, "同色异谱是线性映射零空间的必然结果", size=31, weight="700", fill="#102a43")
    # Two spectra.
    panels = [(45, "光谱 s₁(λ)", "#3b82b5", 0), (405, "光谱 s₂(λ)", "#c85b73", 1)]
    for x0, title_value, color, variant in panels:
        rounded_box(svg, x0, 110, 310, 390, "#f7f9fb", "#b8c5cf", title_value, "形状明显不同")
        l, r, t, b = x0 + 35, x0 + 275, 210, 430
        axes(svg, l, r, t, b, "λ", None)
        pts = []
        for j in range(151):
            u = j / 150
            if variant == 0:
                value = 0.22 + 0.65 * math.exp(-((u - 0.28) / 0.14) ** 2) + 0.30 * math.exp(-((u - 0.75) / 0.14) ** 2)
            else:
                value = 0.34 + 0.28 * math.exp(-((u - 0.12) / 0.10) ** 2) + 0.46 * math.exp(-((u - 0.52) / 0.13) ** 2) + 0.12 * math.sin(7 * math.pi * u)
            pts.append((l + (r - l) * u, b - 175 * max(0.05, value)))
        polyline(svg, pts, stroke=color, width=4)
    line(svg, 725, 305, 790, 305, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Difference/nullspace.
    rounded_box(svg, 795, 110, 330, 390, "#fffaf1", "#e8c77d", "差光谱 d=s₂−s₁", "可有正负分量；A d = 0", "#8a5f19")
    l, r, mid = 835, 1085, 330
    line(svg, l, mid, r, mid, stroke="#8aa2b5", width=2)
    pts = []
    for j in range(151):
        u = j / 150
        value = 0.55 * math.sin(3 * math.pi * u) * math.sin(math.pi * u) + 0.18 * math.sin(7 * math.pi * u)
        pts.append((l + (r - l) * u, mid - 115 * value))
    polyline(svg, pts, stroke="#c58a2d", width=4)
    text(svg, 960, 455, "∫d(λ)qᵢ(λ)dλ = 0，i=1,2,3", size=16, weight="700", fill="#7b4b74")
    line(svg, 1130, 305, 1195, 305, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Same result.
    rounded_box(svg, 1200, 110, 265, 390, "#edf8f2", "#9fd6b7", "相同三刺激值", "As₁ = As₂", "#397456")
    for idx, (label, color, value) in enumerate((("X", "#c85b73", 0.72), ("Y", "#4d8c6a", 0.58), ("Z", "#3b82b5", 0.35))):
        y = 235 + idx * 78
        text(svg, 1245, y + 6, label, size=18, weight="700", fill=color, anchor="start")
        SubElement(svg, "rect", {"x": "1280", "y": str(y - 13), "width": str(125 * value), "height": "25", "rx": "7", "fill": color, "fill-opacity": "0.55"})
    text(svg, 1332, 452, "人眼匹配；光谱仪仍可区分", size=16, fill="#486581")
    # Linear algebra strip.
    rounded_box(svg, 120, 575, 1260, 92, "#f7efff", "#c9a9e8", "离散为 N 个波长样本：t = A s，A∈ℝ³ˣᴺ；当 rank(A)=3 时，dim ker(A)=N−3", "因此三刺激值不能唯一反演光谱", "#7b4b74")
    ElementTree(svg).write(SVG_DIR / "metamer_nullspace.svg", encoding="utf-8", xml_declaration=True)


def chromaticity_gamuts():
    width, height = 1500, 760
    svg = base_svg(width, height, "CIE xy色度图与多个RGB色域三角形")
    text(svg, width / 2, 43, "xy 色度图压掉亮度；RGB 非负色域在其中形成原色三角形", size=31, weight="700", fill="#102a43")
    # Plot setup.
    l, r, t, b = 120, 850, 110, 675
    axes(svg, l, r, t, b, "x", "y")
    for q in [0.0, 0.2, 0.4, 0.6, 0.8]:
        x = l + (r - l) * q / 0.8
        y = b - (b - t) * q / 0.9
        line(svg, x, t, x, b, stroke="#e0e7ec", width=1)
        line(svg, l, y, r, y, stroke="#e0e7ec", width=1)
        text(svg, x, b + 25, f"{q:.1f}", size=13, fill="#627d98")
        text(svg, l - 12, y + 5, f"{q:.1f}", size=13, fill="#627d98", anchor="end")
    locus = [
        (0.174, 0.005), (0.157, 0.018), (0.124, 0.058), (0.091, 0.133),
        (0.045, 0.295), (0.008, 0.538), (0.014, 0.750), (0.074, 0.834),
        (0.155, 0.806), (0.230, 0.754), (0.302, 0.692), (0.373, 0.625),
        (0.444, 0.555), (0.513, 0.487), (0.575, 0.424), (0.627, 0.373),
        (0.666, 0.334), (0.692, 0.308), (0.708, 0.292), (0.726, 0.273),
        (0.735, 0.265),
    ]
    def map_xy(p):
        x, y = p
        return (l + (r - l) * x / 0.8, b - (b - t) * y / 0.9)
    locus_px = [map_xy(p) for p in locus]
    spectral_poly = locus_px + [locus_px[0]]
    polygon(svg, spectral_poly, "#eef5fb", "#4f7290", 3, 0.7)
    line(svg, *locus_px[-1], *locus_px[0], stroke="#7b4b74", width=3)
    text(svg, 308, 630, "紫线（非单色光）", size=15, fill="#7b4b74")
    text(svg, 470, 132, "光谱轨迹", size=17, weight="700", fill="#285b7a")
    # Gamut triangles.
    gamuts = [
        ("sRGB", [(0.64, 0.33), (0.30, 0.60), (0.15, 0.06)], "#3b82b5"),
        ("Display P3", [(0.68, 0.32), (0.265, 0.69), (0.15, 0.06)], "#4d8c6a"),
        ("ProPhoto RGB", [(0.7347, 0.2653), (0.1596, 0.8404), (0.0366, 0.0001)], "#c85b73"),
    ]
    for label, coords, color in gamuts:
        pts = [map_xy(p) for p in coords]
        pts.append(pts[0])
        polyline(svg, pts, stroke=color, width=4, dash="9 5" if label == "ProPhoto RGB" else None)
    d65 = map_xy((0.3127, 0.3290))
    d50 = map_xy((0.3457, 0.3585))
    for point in (d65, d50):
        SubElement(svg, "circle", {"cx": str(point[0]), "cy": str(point[1]), "r": "7", "fill": "#ffffff", "stroke": "#334e68", "stroke-width": "3"})
    text(svg, d65[0] - 12, d65[1] + 24, "D65", size=13, weight="700", fill="#334e68", anchor="end")
    text(svg, d50[0] + 12, d50[1] - 10, "D50", size=13, weight="700", fill="#334e68", anchor="start")
    # Right explanation.
    rounded_box(svg, 930, 110, 500, 155, "#eaf4ff", "#9bc7ee", "色度图只显示方向", "(X,Y,Z) 与 k(X,Y,Z) 落在同一点", "#285b7a")
    rounded_box(svg, 930, 305, 500, 155, "#edf8f2", "#9fd6b7", "色域是可表示集合", "三角形面积不是精度、位深或色数", "#397456")
    rounded_box(svg, 930, 500, 500, 155, "#fff0f3", "#eab0be", "边界外需负 RGB 或映射", "直接裁切会改变色相与明度关系", "#a24862")
    legend_y = 92
    for idx, (label, _, color) in enumerate(gamuts):
        x = 250 + idx * 235
        line(svg, x - 70, legend_y - 6, x - 20, legend_y - 6, stroke=color, width=4, dash="9 5" if label == "ProPhoto RGB" else None)
        text(svg, x, legend_y, label, size=15, weight="700", fill=color, anchor="start")
    ElementTree(svg).write(SVG_DIR / "chromaticity_gamuts.svg", encoding="utf-8", xml_declaration=True)


def rgb_matrix_gamut_mapping():
    width, height = 1500, 720
    svg = base_svg(width, height, "由原色色度和白点构造RGB到XYZ矩阵及超色域映射")
    text(svg, width / 2, 43, "RGB 空间由原色、白点和编码曲线共同定义", size=31, weight="700", fill="#102a43")
    blocks = [
        (35, "原色色度", "(xr,yr),(xg,yg),(xb,yb)", "#fff0f3", "#eab0be"),
        (330, "单位亮度原色", "pi=(xi/yi,1,(1−xi−yi)/yi)", "#eaf4ff", "#9bc7ee"),
        (625, "白点定标", "s=P⁻¹w", "#fff7e8", "#e8c77d"),
        (920, "线性矩阵", "M=P diag(s)", "#edf8f2", "#9fd6b7"),
        (1215, "XYZ", "t=M rgblinear", "#f7efff", "#c9a9e8"),
    ]
    for x, title_value, subtitle, fill, stroke in blocks:
        rounded_box(svg, x, 110, 250, 130, fill, stroke, title_value, subtitle)
    for x in (285, 580, 875, 1170):
        line(svg, x, 175, x + 38, 175, stroke="#527da3", width=3, marker="arrow-blue")
    text(svg, 750, 280, "矩阵只作用于线性光 RGB；非线性编码值必须先逆 OETF", size=19, weight="700", fill="#7b4b74")
    # Bottom panels: in gamut/out of gamut.
    line(svg, 750, 315, 750, 660, stroke="#d7e0e7", width=2)
    text(svg, 375, 350, "RGB 立方体经线性变换成为 XYZ 平行六面体", size=21, weight="700", fill="#285b7a")
    # Cube wireframe.
    front = [(170, 585), (430, 585), (430, 410), (170, 410)]
    back = [(260, 530), (520, 530), (520, 355), (260, 355)]
    for pts in (front + [front[0]], back + [back[0]]):
        pass
    polyline(svg, front + [front[0]], stroke="#3b82b5", width=4)
    polyline(svg, back + [back[0]], stroke="#4d8c6a", width=4)
    for a, bpt in zip(front, back):
        line(svg, *a, *bpt, stroke="#7b4b74", width=3)
    vertex_labels = [((170, 585), "0"), ((430, 585), "R"), ((170, 410), "G"), ((260, 355), "B"), ((520, 355), "R+G+B")]
    for (x, y), label in vertex_labels:
        text(svg, x, y - 12, label, size=14, weight="700", fill="#486581")
    text(svg, 350, 630, "非负 RGB 只是三维颜色空间中的有限子集", size=17, fill="#486581")
    # Gamut mapping diagram.
    text(svg, 1125, 350, "超色域点的三种处理", size=21, weight="700", fill="#a24862")
    cx, cy = 1040, 515
    triangle = [(850, 615), (1090, 390), (1230, 615)]
    polygon(svg, triangle, "#eaf4ff", "#3b82b5", 3, 0.45)
    p_out = (1305, 430)
    SubElement(svg, "circle", {"cx": str(p_out[0]), "cy": str(p_out[1]), "r": "10", "fill": "#c85b73"})
    text(svg, p_out[0] + 15, p_out[1] - 8, "目标色", size=15, weight="700", fill="#a24862", anchor="start")
    # Three destinations.
    destinations = [((1190, 570), "逐通道裁切", "#c85b73"), ((1135, 520), "保持色相压缩", "#4d8c6a"), ((1045, 470), "允许负中间值", "#7b4b74")]
    for idx, (dest, label, color) in enumerate(destinations):
        line(svg, p_out[0] - 10, p_out[1] + idx * 4, dest[0], dest[1], stroke=color, width=3, dash="8 5", marker="arrow-red" if idx == 0 else None)
        SubElement(svg, "circle", {"cx": str(dest[0]), "cy": str(dest[1]), "r": "7", "fill": color})
        text(svg, dest[0] + 12, dest[1] + 5, label, size=14, weight="700", fill=color, anchor="start")
    text(svg, 1125, 660, "选择映射规则，就是选择哪些关系优先保留", size=17, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "rgb_matrix_gamut_mapping.svg", encoding="utf-8", xml_declaration=True)


def illuminant_reflectance_wb():
    width, height = 1500, 740
    svg = base_svg(width, height, "照明与反射率乘积不可分离及相机白平衡增益")
    text(svg, width / 2, 43, "相机测到照明与反射率的乘积；白平衡选择一种解释", size=31, weight="700", fill="#102a43")
    line(svg, 750, 85, 750, 675, stroke="#d7e0e7", width=2)
    # Left ambiguity.
    text(svg, 375, 103, "同一入射光谱可有不同因子分解", size=23, weight="700", fill="#285b7a")
    panels = [(70, 155, "照明 E₁", "#c58a2d", 0), (300, 155, "反射率 ρ₁", "#4d8c6a", 1), (530, 155, "乘积 s=Eρ", "#3b82b5", 2)]
    for x0, y0, title_value, color, kind in panels:
        rounded_box(svg, x0, y0, 180, 190, "#f7f9fb", "#b8c5cf", title_value, None)
        l, r, t, b = x0 + 22, x0 + 158, y0 + 70, y0 + 160
        line(svg, l, b, r, b, stroke="#9fb3c2", width=1.5)
        pts = []
        for j in range(81):
            u = j / 80
            if kind == 0:
                value = 0.25 + 0.65 * u
            elif kind == 1:
                value = 0.82 - 0.45 * u + 0.12 * math.sin(3 * math.pi * u)
            else:
                value = (0.25 + 0.65 * u) * (0.82 - 0.45 * u + 0.12 * math.sin(3 * math.pi * u))
            pts.append((l + (r - l) * u, b - 75 * value))
        polyline(svg, pts, stroke=color, width=3.5)
    text(svg, 275, 255, "×", size=30, weight="700", fill="#334e68")
    text(svg, 505, 255, "=", size=30, weight="700", fill="#334e68")
    # Second factorization.
    text(svg, 375, 390, "取任意正函数 a(λ)：E₂=E₁a，ρ₂=ρ₁/a，乘积不变", size=18, weight="700", fill="#7b4b74")
    rounded_box(svg, 75, 435, 600, 145, "#fff7e8", "#e8c77d", "图像形成的谱模型", "cᵢ = ∫E(λ)ρ(λ)qᵢ(λ)dλ", "#8a5f19")
    text(svg, 375, 620, "即使通道无噪声，也不能由单次观测唯一分离光源与物体", size=17, fill="#a24862")
    # Right white balance.
    text(svg, 1125, 103, "白平衡与色适应是通道变换", size=23, weight="700", fill="#397456")
    rounded_box(svg, 825, 150, 270, 125, "#eaf4ff", "#9bc7ee", "相机线性响应", "c = (cR,cG,cB)ᵀ", "#285b7a")
    rounded_box(svg, 1155, 150, 270, 125, "#edf8f2", "#9fd6b7", "对角白平衡", "c′ = diag(gR,gG,gB)c", "#397456")
    line(svg, 1100, 212, 1145, 212, stroke="#3b82b5", width=3, marker="arrow-blue")
    text(svg, 1125, 315, "中性参考：令 gᵢcᵢ 相等", size=17, weight="700", fill="#7b4b74")
    # Gains bars.
    gains = [("R", 0.72, "#c85b73"), ("G", 0.42, "#4d8c6a"), ("B", 0.90, "#3b82b5")]
    for idx, (label, value, color) in enumerate(gains):
        y = 370 + idx * 58
        text(svg, 860, y + 5, label, size=17, weight="700", fill=color, anchor="start")
        SubElement(svg, "rect", {"x": "900", "y": str(y - 13), "width": str(260 * value), "height": "25", "rx": "7", "fill": color, "fill-opacity": "0.55"})
        text(svg, 1180, y + 5, f"g{label}", size=16, fill="#486581", anchor="start")
    rounded_box(svg, 835, 565, 580, 100, "#fff0f3", "#eab0be", "局限", "一个全局对角矩阵不能同时校正多种照明，也不能恢复未知反射谱", "#a24862")
    ElementTree(svg).write(SVG_DIR / "illuminant_reflectance_wb.svg", encoding="utf-8", xml_declaration=True)


def cct_chromatic_adaptation():
    width, height = 1500, 735
    svg = base_svg(width, height, "相关色温Duv与vonKries型色适应变换")
    text(svg, width / 2, 43, "色温只定位黑体轨迹附近的一维方向；色适应还需白点和响应空间", size=31, weight="700", fill="#102a43")
    line(svg, 750, 85, 750, 670, stroke="#d7e0e7", width=2)
    # CCT plot.
    text(svg, 375, 103, "CCT 与 Duv", size=24, weight="700", fill="#a24862")
    l, r, t, b = 90, 690, 160, 590
    axes(svg, l, r, t, b, "u", "v")
    pts = []
    for j in range(151):
        u = j / 150
        x = l + 70 + 440 * u
        y = b - 85 - 230 * (u ** 0.72) + 75 * u * u
        pts.append((x, y))
    polyline(svg, pts, stroke="#c58a2d", width=6)
    labels = [(0.12, "10000 K"), (0.40, "6500 K"), (0.68, "4000 K"), (0.90, "2500 K")]
    for u, label in labels:
        idx = int(u * 150)
        x, y = pts[idx]
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "7", "fill": "#c58a2d"})
        text(svg, x + 12, y - 10, label, size=14, weight="700", fill="#8a5f19", anchor="start")
    idx = 66
    x0, y0 = pts[idx]
    line(svg, x0 - 65, y0 + 48, x0 + 65, y0 - 48, stroke="#7b4b74", width=3, dash="8 5")
    p_plus = (x0 - 42, y0 - 56)
    p_minus = (x0 + 42, y0 + 56)
    for point, label, color in ((p_plus, "+Duv", "#4d8c6a"), (p_minus, "−Duv", "#c85b73")):
        SubElement(svg, "circle", {"cx": str(point[0]), "cy": str(point[1]), "r": "8", "fill": color})
        text(svg, point[0] + 12, point[1] + 5, label, size=15, weight="700", fill=color, anchor="start")
    text(svg, 375, 635, "同一 CCT 的光源仍可在绿—品红方向显著不同", size=17, fill="#7b4b74")
    # Adaptation pipeline.
    text(svg, 1125, 103, "von Kries 型色适应", size=24, weight="700", fill="#397456")
    blocks = [
        (805, 175, 250, "源白点 XYZ", "t"),
        (1085, 175, 250, "锥体样空间", "l = M t"),
        (945, 355, 250, "白点比例缩放", "l′ = D l"),
        (1225, 355, 220, "目标 XYZ", "t′ = M⁻¹l′"),
    ]
    for idx, (x, y, w, title_value, subtitle) in enumerate(blocks):
        fills = ["#eaf4ff", "#fff7e8", "#edf8f2", "#f7efff"]
        strokes = ["#9bc7ee", "#e8c77d", "#9fd6b7", "#c9a9e8"]
        rounded_box(svg, x, y, w, 115, fills[idx], strokes[idx], title_value, subtitle)
    line(svg, 1060, 232, 1075, 232, stroke="#3b82b5", width=3, marker="arrow-blue")
    line(svg, 1210, 295, 1070, 345, stroke="#3b82b5", width=3, marker="arrow-blue")
    line(svg, 1200, 412, 1215, 412, stroke="#3b82b5", width=3, marker="arrow-blue")
    rounded_box(svg, 845, 535, 560, 105, "#eef5fb", "#a8c8e0", "适应矩阵", "A = M⁻¹ diag(lw,dst / lw,src) M", "#285b7a")
    text(svg, 1125, 680, "Bradford 等方法的差别主要在 M 与经验校正；它们都是近似观察者模型", size=16, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "cct_chromatic_adaptation.svg", encoding="utf-8", xml_declaration=True)


def lab_deltae():
    width, height = 1500, 735
    svg = base_svg(width, height, "CIELAB非线性变换色相彩度与局部色差度量")
    text(svg, width / 2, 43, "CIELAB 用白点归一化和立方根压缩，近似而非完美地均匀化色差", size=31, weight="700", fill="#102a43")
    # Nonlinearity.
    rounded_box(svg, 35, 105, 410, 500, "#f4f9fd", "#9bc7ee", "非线性 f(t)", "高亮立方根；暗部线性延拓", "#285b7a")
    l, r, t, b = 90, 400, 220, 500
    axes(svg, l, r, t, b, "t", "f(t)")
    delta = 6 / 29
    pts = []
    for j in range(201):
        u = j / 200
        value = u ** (1 / 3) if u > delta ** 3 else u / (3 * delta ** 2) + 4 / 29
        pts.append((l + (r - l) * u, b - 235 * value))
    polyline(svg, pts, stroke="#3b82b5", width=5)
    xk = l + (r - l) * delta ** 3
    line(svg, xk, t, xk, b, stroke="#c85b73", width=2, dash="7 5")
    text(svg, xk + 10, 455, "δ³", size=15, weight="700", fill="#a24862", anchor="start")
    text(svg, 240, 560, "δ=6/29 保证函数与一阶导数连续", size=16, fill="#7b4b74")
    # Lab geometry.
    rounded_box(svg, 480, 105, 480, 500, "#fffaf1", "#e8c77d", "Lab 几何", "L* 明度；a*、b* 为对手色轴", "#8a5f19")
    cx, cy = 720, 400
    line(svg, cx, cy, cx, 205, stroke="#334e68", width=3, marker="arrow-dark")
    line(svg, cx, cy, 535, 500, stroke="#4d8c6a", width=3, marker="arrow-green")
    line(svg, cx, cy, 905, 500, stroke="#c85b73", width=3, marker="arrow-red")
    text(svg, cx + 12, 205, "L*", size=18, weight="700", fill="#334e68", anchor="start")
    text(svg, 520, 520, "−a* 绿", size=16, weight="700", fill="#397456")
    text(svg, 920, 520, "+a* 红", size=16, weight="700", fill="#a24862")
    line(svg, cx, cy, 610, 300, stroke="#3b82b5", width=3, marker="arrow-blue")
    line(svg, cx, cy, 830, 300, stroke="#c58a2d", width=3, marker="arrow-gold")
    text(svg, 595, 288, "−b* 蓝", size=16, weight="700", fill="#285b7a")
    text(svg, 845, 288, "+b* 黄", size=16, weight="700", fill="#8a5f19")
    # Chroma circle and hue.
    SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": "78", "fill": "none", "stroke": "#7b4b74", "stroke-width": "2", "stroke-dasharray": "7 5"})
    px, py = cx + 62, cy - 47
    line(svg, cx, cy, px, py, stroke="#7b4b74", width=4)
    SubElement(svg, "circle", {"cx": str(px), "cy": str(py), "r": "8", "fill": "#7b4b74"})
    text(svg, px + 15, py - 8, "C*ab", size=16, weight="700", fill="#7b4b74", anchor="start")
    text(svg, 720, 570, "C* = √(a*²+b*²)，h = atan2(b*,a*)", size=17, fill="#486581")
    # Delta E metrics.
    rounded_box(svg, 995, 105, 470, 500, "#f7efff", "#c9a9e8", "局部色差度量", "同样数值不一定同样可见", "#7b4b74")
    # Ellipses.
    ellipse_specs = [(1080, 285, 52, 22, -20), (1260, 270, 30, 58, 25), (1160, 430, 68, 30, 15), (1350, 455, 38, 18, -35)]
    for x, y, rx, ry, angle in ellipse_specs:
        SubElement(svg, "ellipse", {"cx": str(x), "cy": str(y), "rx": str(rx), "ry": str(ry), "fill": "#c9a9e8", "fill-opacity": "0.25", "stroke": "#7b4b74", "stroke-width": "2.5", "transform": f"rotate({angle} {x} {y})"})
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "5", "fill": "#7b4b74"})
    text(svg, 1230, 535, "ΔE*ab = √(ΔL*²+Δa*²+Δb*²)", size=18, weight="700", fill="#7b4b74")
    text(svg, 1230, 570, "ΔE00 用位置相关权重与旋转项修正", size=16, fill="#486581")
    rounded_box(svg, 165, 640, 1170, 62, "#fff0f3", "#eab0be", "色差阈值依赖亮度、色相、面积、纹理、显示与观察者；不存在跨条件通用的“ΔE<1 绝对不可见”", None, "#a24862")
    ElementTree(svg).write(SVG_DIR / "lab_deltae.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    spectral_to_tristimulus()
    metamer_nullspace()
    chromaticity_gamuts()
    rgb_matrix_gamut_mapping()
    illuminant_reflectance_wb()
    cct_chromatic_adaptation()
    lab_deltae()


if __name__ == "__main__":
    main()
