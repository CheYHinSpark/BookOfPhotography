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
    text(parent, x + w / 2, y + 43, title_value, size=21, weight="700", fill=title_color)
    if subtitle:
        text(parent, x + w / 2, y + 78, subtitle, size=16, fill="#486581")


def motion_path_kernel():
    width, height = 1500, 670
    svg = base_svg(width, height, "曝光轨迹与运动模糊核")
    text(svg, width / 2, 43, "运动模糊核是曝光时间内位置占据的归一化测度", size=31, weight="700", fill="#102a43")
    centers = [250, 750, 1250]
    titles = ["恒定像面速度", "加速或抖动轨迹", "空间变化的运动场"]
    colors = ["#3b82b5", "#7b4b74", "#c85b73"]
    for idx, (cx, title_value, color) in enumerate(zip(centers, titles, colors)):
        if idx:
            line(svg, cx - 250, 82, cx - 250, 590, stroke="#d7e0e7", width=2)
        text(svg, cx, 95, title_value, size=23, weight="700", fill=color)
    # Constant line path.
    line(svg, 90, 260, 410, 260, stroke=colors[0], width=8, marker="arrow-blue")
    for j in range(9):
        x = 100 + 36 * j
        SubElement(svg, "circle", {"cx": str(x), "cy": "260", "r": "8", "fill": colors[0]})
        text(svg, x, 225 - 12 * (j % 2), f"t{j}", size=13, fill="#627d98")
    text(svg, 250, 330, "长度 L=|v|T", size=20, weight="700", fill=colors[0])
    # PSF strip.
    SubElement(svg, "rect", {"x": "115", "y": "390", "width": "270", "height": "58", "rx": "14", "fill": "#bcd9ef", "stroke": colors[0], "stroke-width": "3"})
    text(svg, 250, 485, "线段核：近似卷积", size=18, fill="#486581")
    # Curved trajectory.
    pts = []
    for j in range(120):
        u = j / 119
        x = 580 + 330 * u
        y = 340 - 120 * math.sin(math.pi * u) + 45 * math.sin(3 * math.pi * u)
        pts.append((x, y))
    polyline(svg, pts, stroke=colors[1], width=7)
    for j in range(0, 120, 15):
        x, y = pts[j]
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "7", "fill": "#c8b0d9", "stroke": colors[1], "stroke-width": "2"})
    text(svg, 750, 430, "停留久处权重大", size=19, weight="700", fill=colors[1])
    text(svg, 750, 485, "核可弯曲、多峰、带回折", size=18, fill="#486581")
    # Spatially varying flow field.
    for row in range(4):
        for col in range(4):
            x = 1080 + col * 105
            y = 190 + row * 85
            dx = 35 + 8 * col
            dy = 10 * (row - 1.5) + 4 * col
            line(svg, x, y, x + dx, y + dy, stroke=colors[2], width=3, marker="arrow-red")
    text(svg, 1250, 525, "不同位置具有不同 v(x)", size=19, weight="700", fill=colors[2])
    text(svg, 1250, 560, "不能由单一全局卷积描述", size=18, fill="#486581")
    text(svg, width / 2, 630, "一般核 h(x)=T⁻¹∫δ(x−r(t))dt；曝光只记录轨迹的时间占据，不记录经过顺序", size=20, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "motion_path_kernel.svg", encoding="utf-8", xml_declaration=True)


def motion_mtf():
    width, height = 1450, 670
    svg = base_svg(width, height, "匀速运动模糊的 sinc 频率响应")
    text(svg, width / 2, 43, "线段模糊在运动方向产生 sinc 零点", size=31, weight="700", fill="#102a43")
    l, r, t, b = 120, 1360, 125, 545
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    for nu in [0, 0.25, 0.5, 0.75, 1.0]:
        x = l + (r - l) * nu
        line(svg, x, t, x, b, stroke="#e0e7ec", width=1.2)
        text(svg, x, b + 34, f"{nu:.2f}", size=16, fill="#627d98")
    for q in [0, 0.25, 0.5, 0.75, 1.0]:
        y = b - (b - t) * q
        line(svg, l, y, r, y, stroke="#e0e7ec", width=1.2)
        text(svg, l - 16, y + 5, f"{q:.2f}", size=15, fill="#627d98", anchor="end")
    def sinc(x):
        return 1.0 if abs(x) < 1e-10 else math.sin(math.pi * x) / (math.pi * x)
    curves = [(0.5, "L=0.5 px", "#4d8c6a"), (1.0, "L=1 px", "#3b82b5"), (2.0, "L=2 px", "#c85b73"), (4.0, "L=4 px", "#7b4b74")]
    for blur, label, color in curves:
        pts = []
        for j in range(321):
            nu = j / 320
            value = abs(sinc(nu * blur))
            pts.append((l + (r - l) * nu, b - (b - t) * value))
        polyline(svg, pts, stroke=color, width=4)
    labels = [(1090, 190, "L=0.5 px", "#397456"), (1030, 260, "L=1 px", "#285b7a"), (730, 405, "L=2 px", "#a24862"), (390, 475, "L=4 px", "#7b4b74")]
    for x, y, value, color in labels:
        text(svg, x, y, value, size=18, weight="700", fill=color)
    text(svg, r, b + 66, "沿运动方向的空间频率 ν / cycle·pixel⁻¹", size=18, fill="#627d98", anchor="end")
    text(svg, l - 10, t - 14, "|MTFmotion|", size=17, fill="#627d98", anchor="start")
    text(svg, width / 2, 625, "垂直于运动方向的理想响应不受此一维线段核影响；真实抖动会在多个方向扩散", size=20, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "motion_mtf.svg", encoding="utf-8", xml_declaration=True)


def image_velocity_geometry():
    width, height = 1500, 680
    svg = base_svg(width, height, "主体运动相机转动与平移产生像面速度")
    text(svg, width / 2, 43, "像面速度取决于角运动；相机平移还带有深度因子 1/Z", size=31, weight="700", fill="#102a43")
    line(svg, 750, 82, 750, 610, stroke="#d7e0e7", width=2)
    # Subject motion side.
    text(svg, 375, 92, "主体横向运动", size=24, weight="700", fill="#285b7a")
    # Camera/lens and sensor.
    SubElement(svg, "ellipse", {"cx": "420", "cy": "340", "rx": "24", "ry": "105", "fill": "#eaf4ff", "stroke": "#3b82b5", "stroke-width": "3"})
    line(svg, 620, 210, 620, 470, stroke="#334e68", width=5)
    text(svg, 620, 500, "像面", size=17, weight="700", fill="#334e68")
    # Object at depth.
    SubElement(svg, "circle", {"cx": "100", "cy": "245", "r": "18", "fill": "#c85b73"})
    line(svg, 85, 220, 180, 220, stroke="#c85b73", width=4, marker="arrow-red")
    text(svg, 130, 195, "横向速度 V", size=18, weight="700", fill="#a24862")
    line(svg, 100, 245, 420, 340, stroke="#627d98", width=2)
    line(svg, 420, 340, 620, 399, stroke="#627d98", width=2)
    line(svg, 100, 245, 420, 340, stroke="#627d98", width=2)
    line(svg, 100, 340, 420, 340, stroke="#d7e0e7", width=1.5, dash="8 6")
    line(svg, 100, 540, 420, 540, stroke="#334e68", width=2)
    line(svg, 100, 530, 100, 550, stroke="#334e68", width=2)
    line(svg, 420, 530, 420, 550, stroke="#334e68", width=2)
    text(svg, 260, 570, "物距 Z", size=18, weight="700", fill="#486581")
    line(svg, 620, 399, 620, 350, stroke="#c85b73", width=7, marker="arrow-red")
    text(svg, 545, 320, "|vimg|≈f|V|/Z", size=20, weight="700", fill="#a24862")
    # Camera motion side.
    text(svg, 1125, 92, "相机旋转与平移", size=24, weight="700", fill="#397456")
    rounded_box(svg, 845, 155, 560, 125, "#edf8f2", "#9fd6b7", "小角旋转 Ω", "全画面近似共同位移；与景深 Z 无关", "#397456")
    rounded_box(svg, 845, 330, 560, 125, "#fff7e8", "#e8c77d", "相机平移 T", "近物移动更快；光流含 1/Z", "#8a5f19")
    # Depth planes with arrows.
    for y, length, label in ((515, 170, "近处"), (565, 85, "远处")):
        line(svg, 920, y, 920 + length, y, stroke="#c85b73", width=5, marker="arrow-red")
        text(svg, 900, y + 6, label, size=17, weight="700", fill="#a24862", anchor="end")
    line(svg, 1180, 515, 1350, 515, stroke="#4d8c6a", width=4, marker="arrow-green")
    line(svg, 1180, 565, 1350, 565, stroke="#4d8c6a", width=4, marker="arrow-green")
    text(svg, 1265, 605, "旋转分量近似同长", size=17, fill="#397456")
    ElementTree(svg).write(SVG_DIR / "image_velocity_geometry.svg", encoding="utf-8", xml_declaration=True)


def shake_probability():
    width, height = 1500, 690
    svg = base_svg(width, height, "安全快门的概率解释与防抖档数")
    text(svg, width / 2, 43, "“安全”不是分界线，而是模糊半径小于阈值的成功概率", size=31, weight="700", fill="#102a43")
    line(svg, 750, 82, 750, 610, stroke="#d7e0e7", width=2)
    # Left 2D Gaussian probability.
    text(svg, 375, 92, "二维抖动位移分布", size=24, weight="700", fill="#285b7a")
    cx, cy = 375, 340
    for r, op in ((210, 0.07), (165, 0.10), (120, 0.16), (75, 0.26), (35, 0.48)):
        SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": str(r), "fill": "#3b82b5", "fill-opacity": str(op)})
    SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": "105", "fill": "none", "stroke": "#c85b73", "stroke-width": "4", "stroke-dasharray": "10 7"})
    text(svg, cx + 120, cy - 80, "容许半径 c", size=18, weight="700", fill="#a24862")
    line(svg, cx, cy, cx + 98, cy - 38, stroke="#c85b73", width=3, marker="arrow-red")
    text(svg, cx, 590, "P(r≤c)=1−exp[−c²/(2σx²)]", size=20, weight="700", fill="#7b4b74")
    # Right success probability curves versus shutter time.
    text(svg, 1125, 92, "成功概率随曝光时间平滑下降", size=24, weight="700", fill="#397456")
    l, r, t, b = 825, 1420, 150, 535
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    for j, label in enumerate(("1/1000", "1/250", "1/60", "1/15", "1/4")):
        x = l + (r - l) * j / 4
        line(svg, x, t, x, b, stroke="#e0e7ec", width=1.2)
        text(svg, x, b + 33, label, size=15, fill="#627d98")
    for q in (0, 0.25, 0.5, 0.75, 1.0):
        y = b - (b - t) * q
        line(svg, l, y, r, y, stroke="#e0e7ec", width=1.2)
        text(svg, l - 16, y + 5, f"{q:.2f}", size=15, fill="#627d98", anchor="end")
    def logistic(x, midpoint, slope=7):
        return 1 / (1 + math.exp(slope * (x - midpoint)))
    for midpoint, color, label, dash in ((0.48, "#c85b73", "无防抖", None), (0.78, "#4d8c6a", "防抖后", None)):
        pts = []
        for j in range(201):
            u = j / 200
            p = logistic(u, midpoint)
            pts.append((l + (r - l) * u, b - (b - t) * p))
        polyline(svg, pts, stroke=color, width=5, dash=dash)
        text(svg, l + (r - l) * (midpoint + 0.04), b - (b - t) * 0.62, label, size=18, weight="700", fill=color, anchor="start")
    line(svg, l, b - (b - t) * 0.5, r, b - (b - t) * 0.5, stroke="#7b4b74", width=2, dash="8 6")
    text(svg, r, b - (b - t) * 0.5 - 12, "例如 50% 成功率", size=16, fill="#7b4b74", anchor="end")
    text(svg, 1125, 590, "“若干档防抖”是同一成功率下可延长的时间倍率", size=19, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "shake_probability.svg", encoding="utf-8", xml_declaration=True)


def stabilization_loop():
    width, height = 1500, 680
    svg = base_svg(width, height, "光学和机身防抖的闭环与频率响应")
    text(svg, width / 2, 43, "防抖降低有限频带内的相机姿态方差，不会改变主体自身运动", size=31, weight="700", fill="#102a43")
    # Top block diagram.
    boxes = [
        (35, "手部角运动", "θhand(t)", "#fff0f3", "#eab0be"),
        (330, "陀螺仪", "测角速度 + 传感噪声", "#eaf4ff", "#9bc7ee"),
        (625, "控制器", "带宽 · 延迟 · 预测", "#f7efff", "#c9a9e8"),
        (920, "执行器", "OIS 镜组 / IBIS 传感器", "#edf8f2", "#9fd6b7"),
        (1215, "残余轨迹", "θres(t)", "#fff7e8", "#e8c77d"),
    ]
    for x, title_value, subtitle, fill, stroke in boxes:
        rounded_box(svg, x, 120, 250, 125, fill, stroke, title_value, subtitle)
    for x in (285, 580, 875, 1170):
        line(svg, x, 182, x + 38, 182, stroke="#527da3", width=3, marker="arrow-blue")
    # Frequency response panel.
    text(svg, 400, 315, "闭环灵敏度 |S(jω)|", size=22, weight="700", fill="#285b7a")
    l, r, t, b = 100, 700, 360, 585
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    pts = []
    for j in range(201):
        u = j / 200
        value = 0.08 + 0.92 / (1 + math.exp(-16 * (u - 0.58)))
        pts.append((l + (r - l) * u, b - (b - t) * value))
    polyline(svg, pts, stroke="#3b82b5", width=5)
    line(svg, l + (r - l) * 0.58, t, l + (r - l) * 0.58, b, stroke="#c85b73", width=2, dash="8 6")
    text(svg, l + 150, 535, "低频被抑制", size=17, weight="700", fill="#285b7a")
    text(svg, l + 420, 405, "带宽外残余", size=17, weight="700", fill="#a24862")
    text(svg, l + (r - l) * 0.58, 340, "控制带宽", size=16, fill="#a24862")
    # Types and limitations.
    rounded_box(svg, 790, 330, 300, 115, "#edf8f2", "#9fd6b7", "OIS", "移动镜组，补偿光线角度", "#397456")
    rounded_box(svg, 1130, 330, 300, 115, "#eaf4ff", "#9bc7ee", "IBIS", "移动传感器，依赖焦距模型", "#285b7a")
    rounded_box(svg, 790, 485, 300, 115, "#fff7e8", "#e8c77d", "电子防抖", "估计后裁切/重采样", "#8a5f19")
    rounded_box(svg, 1130, 485, 300, 115, "#fff0f3", "#eab0be", "共同限制", "行程、延迟、频带与主体运动", "#a24862")
    text(svg, 400, 635, "残余角方差 = ∫|S(ω)|² Φθ(ω)dω", size=19, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "stabilization_loop.svg", encoding="utf-8", xml_declaration=True)


def rolling_shutter_flicker():
    width, height = 1500, 700
    svg = base_svg(width, height, "滚动快门与周期照明形成几何倾斜和条纹")
    text(svg, width / 2, 43, "逐行时间原点把时间变化编码为空间结构", size=31, weight="700", fill="#102a43")
    line(svg, 750, 82, 750, 625, stroke="#d7e0e7", width=2)
    # Left rolling geometry.
    text(svg, 375, 92, "匀速运动 → 剪切", size=24, weight="700", fill="#285b7a")
    x0, y0, w, h = 120, 145, 500, 360
    SubElement(svg, "rect", {"x": str(x0), "y": str(y0), "width": str(w), "height": str(h), "fill": "#f3f6f8", "stroke": "#8aa2b5", "stroke-width": "2"})
    rows = 11
    for j in range(rows):
        y = y0 + 22 + j * 30
        start = x0 + 35 + j * 22
        line(svg, start, y, start + 210, y, stroke="#3b82b5", width=10)
        text(svg, x0 - 12, y + 5, f"y{j}", size=13, fill="#627d98", anchor="end")
    line(svg, x0 + 35, y0 + 22, x0 + 35 + 10 * 22, y0 + 22 + 10 * 30, stroke="#c85b73", width=4, dash="9 6")
    text(svg, 375, 555, "xobs(y)=x0+vx[t0+yTread/H+T/2]", size=19, weight="700", fill="#7b4b74")
    text(svg, 375, 595, "剪切量 ∝ vx Tread；行内模糊 ∝ vx T", size=18, fill="#486581")
    # Right flicker.
    text(svg, 1125, 92, "周期照明 → 明暗条纹", size=24, weight="700", fill="#397456")
    l, r, t, b = 820, 1420, 145, 360
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    pts = []
    for j in range(301):
        u = j / 300
        val = 0.52 + 0.38 * math.cos(6 * math.pi * u)
        pts.append((l + (r - l) * u, b - (b - t) * val))
    polyline(svg, pts, stroke="#c58a2d", width=4)
    text(svg, 1125, 395, "E(t)=E0[1+m cos(2πfLt+φ)]", size=18, weight="700", fill="#8a5f19")
    # Band image below.
    img_x, img_y, img_w, img_h = 875, 435, 500, 160
    for j in range(16):
        shade = 224 - int(85 * (0.5 + 0.5 * math.cos(2 * math.pi * j / 5.2)))
        color = f"#{shade:02x}{min(255, shade+12):02x}{min(255, shade+24):02x}"
        SubElement(svg, "rect", {"x": str(img_x), "y": str(img_y + j * img_h / 16), "width": str(img_w), "height": str(img_h / 16 + 1), "fill": color})
    SubElement(svg, "rect", {"x": str(img_x), "y": str(img_y), "width": str(img_w), "height": str(img_h), "fill": "none", "stroke": "#8aa2b5", "stroke-width": "2"})
    text(svg, 1125, 635, "条纹对比被单行积分的 sinc(fL T) 因子衰减", size=18, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "rolling_shutter_flicker.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    motion_path_kernel()
    motion_mtf()
    image_velocity_geometry()
    shake_probability()
    stabilization_loop()
    rolling_shutter_flicker()


if __name__ == "__main__":
    main()
