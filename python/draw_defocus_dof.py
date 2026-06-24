from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
import math


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


def polyline(parent, points, stroke="#527da3", width=2, fill="none", dash=None):
    attrs = {
        "points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points),
        "stroke": stroke,
        "stroke-width": str(width),
        "fill": fill,
        "stroke-linejoin": "round",
        "stroke-linecap": "round",
    }
    if dash:
        attrs["stroke-dasharray"] = dash
    return SubElement(parent, "polyline", attrs)


def add_defs(svg):
    defs = SubElement(svg, "defs")
    for marker_id, color in (("arrow-blue", "#3b82b5"), ("arrow-red", "#c85b73"), ("arrow-dark", "#334e68"), ("arrow-green", "#4d8c6a")):
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


def defocus_cone():
    width, height = 1350, 650
    svg = base_svg(width, height, "离焦光束锥与弥散圆")
    text(svg, width / 2, 44, "传感器截取光束锥：轴向误差变成横向离焦圆", size=30, weight="700", fill="#102a43")
    axis_y = 330
    lens_x = 250
    sensor_x = 850
    focus_x = 1030
    aperture_top, aperture_bottom = 130, 530
    line(svg, 70, axis_y, 1240, axis_y, stroke="#9fb3c2", width=2, marker="arrow-dark")
    # Lens and aperture.
    SubElement(svg, "path", {"d": f"M {lens_x} 95 C {lens_x-50} 170 {lens_x-50} 490 {lens_x} 565 C {lens_x+50} 490 {lens_x+50} 170 {lens_x} 95 Z", "fill": "#eaf4ff", "stroke": "#5595c5", "stroke-width": "3"})
    line(svg, lens_x, aperture_top, lens_x, aperture_bottom, stroke="#285b7a", width=3)
    text(svg, lens_x, 600, "入瞳直径 D", size=21, weight="700", fill="#285b7a")

    # Cone rays.
    line(svg, lens_x, aperture_top, focus_x, axis_y, stroke="#3b82b5", width=4)
    line(svg, lens_x, aperture_bottom, focus_x, axis_y, stroke="#3b82b5", width=4)
    SubElement(svg, "circle", {"cx": str(focus_x), "cy": str(axis_y), "r": "8", "fill": "#285b7a"})
    text(svg, focus_x, axis_y - 24, "真实共轭像面 v(s)", size=20, weight="700", fill="#285b7a")

    # Sensor plane and circle section.
    line(svg, sensor_x, 95, sensor_x, 565, stroke="#a24862", width=6)
    y_top = aperture_top + (axis_y-aperture_top)*(sensor_x-lens_x)/(focus_x-lens_x)
    y_bottom = aperture_bottom + (axis_y-aperture_bottom)*(sensor_x-lens_x)/(focus_x-lens_x)
    line(svg, sensor_x-18, y_top, sensor_x+18, y_top, stroke="#c85b73", width=4)
    line(svg, sensor_x-18, y_bottom, sensor_x+18, y_bottom, stroke="#c85b73", width=4)
    line(svg, sensor_x+25, y_top, sensor_x+25, y_bottom, stroke="#c85b73", width=3)
    line(svg, sensor_x+16, y_top, sensor_x+34, y_top, stroke="#c85b73", width=3)
    line(svg, sensor_x+16, y_bottom, sensor_x+34, y_bottom, stroke="#c85b73", width=3)
    text(svg, sensor_x+48, axis_y+6, "c", size=24, weight="700", fill="#a24862", anchor="start")
    text(svg, sensor_x, 82, "传感器 v₀", size=22, weight="700", fill="#a24862")

    # Distances.
    line(svg, lens_x, 620, sensor_x, 620, stroke="#334e68", width=2)
    line(svg, lens_x, 610, lens_x, 632, stroke="#334e68", width=2)
    line(svg, sensor_x, 610, sensor_x, 632, stroke="#334e68", width=2)
    text(svg, (lens_x+sensor_x)/2, 645, "v₀", size=21, weight="600")
    line(svg, sensor_x, 590, focus_x, 590, stroke="#7b4b74", width=2)
    line(svg, focus_x, 580, focus_x, 602, stroke="#7b4b74", width=2)
    text(svg, (sensor_x+focus_x)/2, 580, "|Δv|", size=20, weight="600", fill="#7b4b74")
    text(svg, 1170, 510, "c = D |1 - v₀/v|", size=22, weight="700", fill="#7b3651")

    ElementTree(svg).write(SVG_DIR / "defocus_cone.svg", encoding="utf-8", xml_declaration=True)


def dof_boundaries():
    width, height = 1400, 690
    svg = base_svg(width, height, "景深边界与离焦阈值")
    text(svg, width / 2, 44, "景深是离焦曲线低于容许阈值的区间", size=30, weight="700", fill="#102a43")
    # Plot area.
    left, right, top, bottom = 110, 1290, 100, 500
    line(svg, left, bottom, right, bottom, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, left, bottom, left, top, stroke="#334e68", width=2, marker="arrow-dark")
    text(svg, right-10, bottom+32, "物距 s", size=21, fill="#486581")
    text(svg, left-20, top+10, "c(s)", size=21, fill="#486581")

    # An asymmetric defocus curve whose threshold crossings match the labels.
    sn_x, s0_x, sf_x = 360, 610, 1080
    c0_y = 300
    line(svg, left, c0_y, right, c0_y, stroke="#c85b73", width=3, dash="12 8")
    text(svg, right-15, c0_y-14, "阈值 c₀", size=21, weight="700", fill="#a24862", anchor="end")
    pts = []
    for j in range(400):
        x = left + (right-left)*j/399
        if x <= s0_x:
            scale = (s0_x-x)/(s0_x-sn_x)
            y = bottom - (bottom-c0_y)*scale**1.15
        else:
            tau = 260
            scale = (1-math.exp(-(x-s0_x)/tau))/(1-math.exp(-(sf_x-s0_x)/tau))
            y = bottom - (bottom-c0_y)*scale
        pts.append((x, y))
    polyline(svg, pts, stroke="#3b82b5", width=4)
    # Mark boundaries and focus.
    for x, label, color in ((sn_x, "近界 sₙ", "#397456"), (s0_x, "焦点 s₀", "#285b7a"), (sf_x, "远界 s_f", "#397456")):
        line(svg, x, bottom, x, 250 if x != s0_x else bottom-18, stroke=color, width=2, dash="7 6")
        text(svg, x, bottom+34, label, size=20, weight="700", fill=color)
    SubElement(svg, "rect", {"x": str(sn_x), "y": str(bottom+55), "width": str(sf_x-sn_x), "height": "42", "rx": "12", "fill": "#dff5e8", "stroke": "#78bb90", "stroke-width": "2"})
    text(svg, (sn_x+sf_x)/2, bottom+84, "可接受景深区间：c(s) ≤ c₀", size=21, weight="700", fill="#397456")
    text(svg, 700, 650, "对焦到超焦距时，右侧交点移到无穷远；曲线仍只在 s₀ 处达到最小", size=20, fill="#627d98")

    ElementTree(svg).write(SVG_DIR / "dof_boundaries.svg", encoding="utf-8", xml_declaration=True)


def format_dof_equivalence():
    width, height = 1400, 650
    svg = base_svg(width, height, "不同画幅的景深等效")
    text(svg, width / 2, 44, "相同视角与景深：焦距、f 数和画幅按同一比例缩放", size=30, weight="700", fill="#102a43")
    axis_y = 340
    # Two cameras with the same entrance pupil and field of view. The larger
    # format uses twice the focal distance and twice the sensor height.
    panels = [
        (260, 420, 150, "小画幅", "f, N, c₀", "#3b82b5"),
        (870, 1190, 300, "大画幅 k = 2 示意", "2f, 2N, 2c₀", "#a24862"),
    ]
    pupil_h = 140
    for lens_x, sensor_x, sensor_h, title_value, params, color in panels:
        cx = (lens_x + sensor_x) / 2
        line(svg, lens_x, axis_y-pupil_h/2, lens_x, axis_y+pupil_h/2, stroke=color, width=6)
        line(svg, sensor_x, axis_y-sensor_h/2, sensor_x, axis_y+sensor_h/2, stroke="#334e68", width=7)
        # Same object-side field angle and proportionally scaled image plane.
        field_dx = 220
        field_dy = field_dx * (sensor_h/2) / (sensor_x-lens_x)
        line(svg, lens_x, axis_y, lens_x-field_dx, axis_y-field_dy, stroke=color, width=3)
        line(svg, lens_x, axis_y, lens_x-field_dx, axis_y+field_dy, stroke=color, width=3)
        line(svg, lens_x, axis_y, sensor_x, axis_y-sensor_h/2, stroke=color, width=2)
        line(svg, lens_x, axis_y, sensor_x, axis_y+sensor_h/2, stroke=color, width=2)
        text(svg, cx, 105, title_value, size=25, weight="700", fill=color)
        text(svg, cx, 545, params, size=23, weight="700", fill=color)
        text(svg, cx, 585, "入瞳 D = f/N 相同", size=20, fill="#486581")
    line(svg, 700, 85, 700, 585, stroke="#c5d1da", width=2, dash="10 8")
    text(svg, 700, 625, "机位、视角与最终输出一致时，两者得到近似相同的离焦几何", size=20, fill="#627d98")

    ElementTree(svg).write(SVG_DIR / "format_dof_equivalence.svg", encoding="utf-8", xml_declaration=True)


def bokeh_pupil_shapes():
    width, height = 1400, 600
    svg = base_svg(width, height, "焦外点像与出瞳形状")
    text(svg, width / 2, 43, "离焦光斑近似携带出瞳的形状与照度分布", size=30, weight="700", fill="#102a43")
    centers = [180, 450, 720, 990, 1260]
    labels = ["圆形均匀", "六边形光圈", "离轴猫眼", "中心加权", "亮边 / 二线性"]

    # Uniform circle.
    SubElement(svg, "circle", {"cx": str(centers[0]), "cy": "290", "r": "105", "fill": "#9ec9e8", "stroke": "#4b8bbd", "stroke-width": "3"})
    # Hexagonal aperture.
    pts = []
    for j in range(6):
        a = math.radians(30 + 60*j)
        pts.append((centers[1] + 108*math.cos(a), 290 + 108*math.sin(a)))
    SubElement(svg, "polygon", {"points": " ".join(f"{x:.1f},{y:.1f}" for x,y in pts), "fill": "#b7dfc5", "stroke": "#5a9d72", "stroke-width": "3"})
    # Cat eye using ellipse clipped visually by offset circle-like path.
    SubElement(svg, "ellipse", {"cx": str(centers[2]), "cy": "290", "rx": "72", "ry": "112", "fill": "#efc3d0", "stroke": "#c2677e", "stroke-width": "3", "transform": f"rotate(-18 {centers[2]} 290)"})
    # Center weighted rings.
    for r, opacity in ((108,0.18),(78,0.28),(48,0.45),(22,0.7)):
        SubElement(svg, "circle", {"cx": str(centers[3]), "cy": "290", "r": str(r), "fill": "#9c7ac7", "fill-opacity": str(opacity), "stroke": "none"})
    # Bright edge.
    SubElement(svg, "circle", {"cx": str(centers[4]), "cy": "290", "r": "105", "fill": "#f8e4b8", "stroke": "#d5962d", "stroke-width": "14"})
    SubElement(svg, "circle", {"cx": str(centers[4]), "cy": "290", "r": "76", "fill": "#fff8e8", "stroke": "none"})

    for x, label in zip(centers, labels):
        text(svg, x, 445, label, size=20, weight="700", fill="#486581")
    text(svg, width/2, 540, "光斑直径相同，并不意味着卷积后的纹理与边缘观感相同", size=21, weight="600", fill="#7b4b74")

    ElementTree(svg).write(SVG_DIR / "bokeh_pupil_shapes.svg", encoding="utf-8", xml_declaration=True)


def autofocus_models():
    width, height = 1400, 650
    svg = base_svg(width, height, "反差与相位自动对焦模型")
    text(svg, width / 2, 43, "自动对焦：极值搜索与子孔径视差", size=30, weight="700", fill="#102a43")
    line(svg, 700, 80, 700, 590, stroke="#c6d2dc", width=2)

    # Contrast AF plot.
    text(svg, 350, 92, "反差检测", size=25, weight="700", fill="#285b7a")
    left, right, top, bottom = 100, 640, 145, 500
    line(svg, left, bottom, right, bottom, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, left, bottom, left, top, stroke="#334e68", width=2, marker="arrow-dark")
    text(svg, right-10, bottom+32, "镜头位置 a", size=19, fill="#627d98")
    text(svg, left-20, top+10, "J(a)", size=19, fill="#627d98")
    pts = []
    for j in range(240):
        x = left + (right-left)*j/239
        t = (x-(left+right)/2)/105
        y = bottom - 285*math.exp(-0.5*t*t) - 18*math.sin(0.09*x)*math.exp(-0.8*abs(t))
        pts.append((x,y))
    polyline(svg, pts, stroke="#3b82b5", width=4)
    peak_x = (left+right)/2
    line(svg, peak_x, bottom, peak_x, 210, stroke="#4d8c6a", width=2, dash="8 7")
    text(svg, peak_x, 185, "arg max J", size=20, weight="700", fill="#397456")
    text(svg, 350, 570, "需要搜索；局部峰值会误导", size=20, fill="#486581")

    # Phase AF geometry.
    text(svg, 1050, 92, "相位检测", size=25, weight="700", fill="#a24862")
    lens_x, sensor_x, focus_x, axis_y = 830, 1170, 1280, 320
    line(svg, 760, axis_y, 1340, axis_y, stroke="#9fb3c2", width=2)
    SubElement(svg, "ellipse", {"cx": str(lens_x), "cy": str(axis_y), "rx": "28", "ry": "150", "fill": "#eef6fb", "stroke": "#5595c5", "stroke-width": "3"})
    # Two sub-apertures.
    for y,color in ((axis_y-75,"#3b82b5"),(axis_y+75,"#c85b73")):
        SubElement(svg, "circle", {"cx": str(lens_x), "cy": str(y), "r": "13", "fill": color})
        line(svg, lens_x, y, focus_x, axis_y, stroke=color, width=3)
    line(svg, sensor_x, 135, sensor_x, 515, stroke="#334e68", width=5)
    # Sensor intersection spots.
    t = (sensor_x-lens_x)/(focus_x-lens_x)
    y1 = (axis_y-75) + (axis_y-(axis_y-75))*t
    y2 = (axis_y+75) + (axis_y-(axis_y+75))*t
    SubElement(svg, "circle", {"cx": str(sensor_x), "cy": f"{y1:.1f}", "r": "9", "fill": "#3b82b5"})
    SubElement(svg, "circle", {"cx": str(sensor_x), "cy": f"{y2:.1f}", "r": "9", "fill": "#c85b73"})
    line(svg, sensor_x+30, y1, sensor_x+30, y2, stroke="#7b4b74", width=3)
    text(svg, sensor_x+50, axis_y+5, "δ", size=23, weight="700", fill="#7b4b74", anchor="start")
    text(svg, sensor_x, 120, "传感器 v₀", size=20, weight="700")
    text(svg, focus_x, 295, "真实焦点 v", size=20, weight="700", fill="#486581")
    text(svg, 1050, 570, "位移符号给出方向，幅度估计离焦量", size=20, fill="#7b4b74")

    ElementTree(svg).write(SVG_DIR / "autofocus_models.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    defocus_cone()
    dof_boundaries()
    format_dof_equivalence()
    bokeh_pupil_shapes()
    autofocus_models()


if __name__ == "__main__":
    main()
