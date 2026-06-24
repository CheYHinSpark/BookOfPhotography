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
        ("arrow-gold", "#c58a2d"),
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


def rounded_box(parent, x, y, w, h, fill, stroke, title, subtitle=None, title_color="#102a43"):
    SubElement(parent, "rect", {
        "x": str(x), "y": str(y), "width": str(w), "height": str(h),
        "rx": "16", "fill": fill, "stroke": stroke, "stroke-width": "2.5",
    })
    text(parent, x + w / 2, y + 44, title, size=22, weight="700", fill=title_color)
    if subtitle:
        text(parent, x + w / 2, y + 84, subtitle, size=20, fill="#486581")


def photon_to_electron_pixel():
    width, height = 1450, 650
    svg = base_svg(width, height, "像素从入射光子到存储电子的结构")
    text(svg, width / 2, 43, "像素首先是光子计数器，其次才是电压源", size=31, weight="700", fill="#102a43")
    line(svg, 760, 82, 760, 570, stroke="#d7e0e7", width=2)
    # Optical stack.
    text(svg, 380, 92, "光学堆栈把方向与波长路由到光电二极管", size=23, weight="700", fill="#285b7a")
    colors = ["#536fc5", "#4d9f69", "#c85b73", "#d5a33d"]
    xs = [120, 210, 300, 390, 480, 570]
    for j, x in enumerate(xs):
        color = colors[j % len(colors)]
        line(svg, x, 135, 355 + 0.22 * (x - 345), 275, stroke=color, width=3, marker="arrow-blue")
        SubElement(svg, "circle", {"cx": str(x), "cy": "130", "r": "7", "fill": color})
    SubElement(svg, "path", {"d": "M 205 245 Q 355 135 505 245 L 485 285 Q 355 205 225 285 Z", "fill": "#d9ecfb", "stroke": "#3b82b5", "stroke-width": "3"})
    text(svg, 355, 250, "微透镜", size=18, weight="700", fill="#285b7a")
    SubElement(svg, "rect", {"x": "205", "y": "292", "width": "300", "height": "55", "fill": "#d9efd8", "stroke": "#4d8c6a", "stroke-width": "3"})
    text(svg, 355, 328, "彩色滤光片 / 光谱选择", size=18, weight="700", fill="#397456")
    SubElement(svg, "rect", {"x": "165", "y": "365", "width": "380", "height": "155", "rx": "12", "fill": "#eaf4ff", "stroke": "#527da3", "stroke-width": "3"})
    text(svg, 355, 402, "硅光电二极管", size=21, weight="700", fill="#285b7a")
    # Electron well.
    SubElement(svg, "path", {"d": "M 260 430 Q 355 545 450 430", "fill": "none", "stroke": "#7b4b74", "stroke-width": "4"})
    for k in range(18):
        x = 305 + (k % 6) * 20 + (k // 6) * 4
        y = 475 + (k // 6) * 17 + (k % 2) * 3
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "6", "fill": "#7b4b74"})
    text(svg, 355, 550, "电子势阱：积分期间累积电荷", size=18, fill="#7b4b74")
    # Stochastic conversion panel.
    text(svg, 1105, 92, "每个光子只以一定概率贡献可收集电子", size=23, weight="700", fill="#397456")
    rounded_box(svg, 845, 155, 220, 115, "#fff7e8", "#e8c77d", "入射光子", "Nγ")
    rounded_box(svg, 1145, 155, 220, 115, "#edf8f2", "#9fd6b7", "收集电子", "Ne")
    line(svg, 1070, 213, 1135, 213, stroke="#4d8c6a", width=4, marker="arrow-green")
    text(svg, 1103, 190, "η(λ)", size=19, weight="700", fill="#397456")
    text(svg, 1105, 330, "E[Ne | Nγ] = ηNγ", size=24, weight="700", fill="#102a43")
    # Bernoulli dots.
    for k in range(10):
        x = 865 + k * 50
        SubElement(svg, "circle", {"cx": str(x), "cy": "405", "r": "8", "fill": "#c58a2d"})
        if k not in (2, 6, 9):
            line(svg, x, 418, x, 474, stroke="#4d8c6a", width=2.5, marker="arrow-green")
            SubElement(svg, "circle", {"cx": str(x), "cy": "495", "r": "7", "fill": "#4d8c6a"})
        else:
            line(svg, x - 8, 455, x + 8, 471, stroke="#c85b73", width=3)
            line(svg, x + 8, 455, x - 8, 471, stroke="#c85b73", width=3)
    text(svg, 1105, 550, "未吸收、未分离或未收集的事件不会进入 RAW", size=18, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "photon_to_electron_pixel.svg", encoding="utf-8", xml_declaration=True)


def quantum_efficiency_rgb():
    width, height = 1450, 650
    svg = base_svg(width, height, "量子效率与彩色通道的光谱响应")
    text(svg, width / 2, 43, "量子效率是波长函数，彩色滤光片进一步选择光谱", size=31, weight="700", fill="#102a43")
    l, r, t, b = 135, 1350, 120, 535
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    for wl in range(400, 701, 50):
        x = l + (r - l) * (wl - 400) / 300
        line(svg, x, t, x, b, stroke="#e0e7ec", width=1.2)
        text(svg, x, b + 34, str(wl), size=16, fill="#627d98")
    for q in (0.25, 0.5, 0.75, 1.0):
        y = b - (b - t) * q
        line(svg, l, y, r, y, stroke="#e0e7ec", width=1.2)
        text(svg, l - 18, y + 5, f"{q:.2f}", size=15, fill="#627d98", anchor="end")
    text(svg, r, b + 62, "波长 λ / nm", size=18, fill="#627d98", anchor="end")
    text(svg, l - 15, t - 12, "相对响应", size=18, fill="#627d98", anchor="start")
    curves = [
        ("硅器件包络", "#7b4b74", lambda wl: 0.86 * math.exp(-0.5 * ((wl - 555) / 115) ** 2), "10 7"),
        ("B", "#536fc5", lambda wl: 0.62 * math.exp(-0.5 * ((wl - 460) / 43) ** 2), None),
        ("G", "#4d9f69", lambda wl: 0.70 * math.exp(-0.5 * ((wl - 540) / 48) ** 2), None),
        ("R", "#c85b73", lambda wl: 0.66 * math.exp(-0.5 * ((wl - 615) / 55) ** 2), None),
    ]
    for label, color, func, dash in curves:
        pts = []
        for j in range(301):
            wl = 400 + j
            value = min(1, func(wl))
            pts.append((l + (r - l) * j / 300, b - (b - t) * value))
        polyline(svg, pts, stroke=color, width=4, dash=dash)
    text(svg, 620, 165, "硅器件包络", size=18, weight="700", fill="#7b4b74")
    text(svg, 365, 280, "B", size=20, weight="700", fill="#536fc5")
    text(svg, 700, 235, "G", size=20, weight="700", fill="#4d9f69")
    text(svg, 1010, 285, "R", size=20, weight="700", fill="#c85b73")
    text(svg, width / 2, 615, "曲线为教学示意；实际响应还包含微透镜、CFA、红外截止滤镜与入射角", size=20, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "quantum_efficiency_rgb.svg", encoding="utf-8", xml_declaration=True)


def full_well_conversion_gain():
    width, height = 1450, 680
    svg = base_svg(width, height, "满阱容量与转换增益的权衡")
    text(svg, width / 2, 43, "浮动扩散电容把电子数变为电压：斜率与容量互相制约", size=31, weight="700", fill="#102a43")
    line(svg, 725, 82, 725, 610, stroke="#d7e0e7", width=2)
    # Left graph.
    text(svg, 360, 92, "电荷—电压转换", size=24, weight="700", fill="#285b7a")
    l, r, t, b = 105, 650, 145, 540
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    text(svg, r, b + 34, "电子数 Ne", size=17, fill="#627d98", anchor="end")
    text(svg, l - 18, t + 4, "电压变化 ΔV", size=17, fill="#627d98", anchor="start")
    # LCG: shallow slope, farther full well.
    line(svg, l + 20, b - 20, r - 30, t + 90, stroke="#3b82b5", width=5)
    line(svg, r - 30, t + 90, r - 30, b, stroke="#3b82b5", width=2, dash="8 6")
    text(svg, 520, 305, "低转换增益 LCG", size=18, weight="700", fill="#285b7a")
    text(svg, r - 30, b + 62, "较大满阱", size=16, fill="#285b7a")
    # HCG: steep slope, earlier saturation.
    line(svg, l + 20, b - 20, 430, t + 35, stroke="#c85b73", width=5)
    line(svg, 430, t + 35, 430, b, stroke="#c85b73", width=2, dash="8 6")
    text(svg, 305, 260, "高转换增益 HCG", size=18, weight="700", fill="#a24862")
    text(svg, 430, b + 62, "较小满阱", size=16, fill="#a24862")
    # Right explanation boxes.
    text(svg, 1085, 92, "同一电压摆幅 ΔVmax", size=24, weight="700", fill="#397456")
    rounded_box(svg, 820, 155, 530, 125, "#eaf4ff", "#9bc7ee", "LCG：电容较大，µV/e⁻ 较低", "更多电子才走完整个电压摆幅", "#285b7a")
    rounded_box(svg, 820, 325, 530, 125, "#fff0f3", "#eab0be", "HCG：有效电容较小，µV/e⁻ 较高", "少量电子产生更大电压，读出链更易分辨", "#a24862")
    text(svg, 1085, 505, "NFW ≈ Cfd ΔVmax / qe", size=23, weight="700", fill="#102a43")
    text(svg, 1085, 550, "切换增益改变读出坐标，不改变已经到达的光子", size=19, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "full_well_conversion_gain.svg", encoding="utf-8", xml_declaration=True)


def cmos_readout_pipeline():
    width, height = 1200, 440
    svg = base_svg(width, height, "CMOS 像素从电荷到 RAW 码值的读出链")
    text(svg, width / 2, 40, "增益放在哪里，决定哪些噪声会被共同放大", size=28, weight="700", fill="#102a43")
    boxes = [
        (20, 200, "光电二极管", "Ne 电子", "#edf8f2", "#9fd6b7"),
        (260, 200, "浮动扩散节点", "ΔV = qeNe/Cfd", "#eaf4ff", "#9bc7ee"),
        (500, 200, "相关双采样", "复位样本 − 信号样本", "#fff7e8", "#e8c77d"),
        (740, 200, "模拟增益", "ga", "#f7efff", "#c9a9e8"),
        (980, 200, "ADC 与数字偏置", "B bit → RAW DN", "#fff0f3", "#eab0be"),
    ]
    for x, w, title_value, subtitle, fill, stroke in boxes:
        rounded_box(svg, x, 80, w, 110, fill, stroke, title_value, subtitle)
    for x in (222, 462, 702, 942):
        line(svg, x, 135, x + 36, 135, stroke="#527da3", width=3, marker="arrow-blue")
    # Noise injection points.
    noise = [
        (120, 260, "光子与暗电荷", "积分前/期间", "#4d8c6a"),
        (360, 320, "像素源跟随器", "模拟读出", "#3b82b5"),
        (600, 260, "列放大与 CDS 残差", "增益之前", "#c58a2d"),
        (840, 320, "下游放大器", "增益之后", "#7b4b74"),
        (1080, 260, "量化与数字处理", "ADC/编码", "#c85b73"),
    ]
    for x, y, title_value, subtitle, color in noise:
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "10", "fill": color})
        line(svg, x, y - 12, x, 200, stroke=color, width=2.5, dash="7 5")
        text(svg, x, y + 36, title_value, size=20, weight="700", fill=color)
        text(svg, x, y + 62, subtitle, size=18, fill="#627d98")
    text(svg, width / 2, 420, "模拟增益可压低其后噪声折算到输入端的影响，却不能改善此前已形成的散粒涨落", size=20, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "cmos_readout_pipeline.svg", encoding="utf-8", xml_declaration=True)


def rolling_global_shutter():
    width, height = 1500, 690
    svg = base_svg(width, height, "全局快门与滚动快门的时空采样")
    text(svg, width / 2, 43, "快门不仅决定积分长度，也决定各行的时间原点", size=31, weight="700", fill="#102a43")
    line(svg, 750, 82, 750, 620, stroke="#d7e0e7", width=2)
    panels = [(375, "全局快门", False, "#4d8c6a"), (1125, "滚动快门", True, "#c85b73")]
    for cx, title_value, rolling, color in panels:
        text(svg, cx, 95, title_value, size=25, weight="700", fill=color)
        l, r, t, b = cx - 285, cx + 285, 145, 485
        line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
        line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
        text(svg, r, b + 34, "时间", size=17, fill="#627d98", anchor="end")
        text(svg, l - 16, t + 5, "行号", size=17, fill="#627d98", anchor="start")
        rows = 9
        for j in range(rows):
            y = t + 30 + j * 34
            start = l + 80 + (j * 25 if rolling else 0)
            end = start + 235
            SubElement(svg, "rect", {"x": str(start), "y": str(y - 8), "width": str(end - start), "height": "16", "rx": "4", "fill": color, "fill-opacity": ".42", "stroke": color, "stroke-width": "1.5"})
        if rolling:
            line(svg, l + 80, t + 30, l + 80 + 8 * 25, t + 30 + 8 * 34, stroke=color, width=3, dash="9 6")
            text(svg, cx, 535, "顶部与底部相差 Tread", size=18, weight="700", fill=color)
        else:
            line(svg, l + 80, t + 10, l + 80, b - 20, stroke=color, width=3, dash="9 6")
            text(svg, cx, 535, "所有行共享同一曝光起点", size=18, weight="700", fill=color)
    # Moving vertical object sketches.
    line(svg, 190, 575, 190, 640, stroke="#334e68", width=10)
    text(svg, 240, 615, "运动竖杆仍近似竖直", size=17, fill="#486581", anchor="start")
    line(svg, 1000, 575, 1070, 640, stroke="#c85b73", width=10)
    text(svg, 1110, 615, "逐行采样形成倾斜", size=17, fill="#a24862", anchor="start")
    ElementTree(svg).write(SVG_DIR / "rolling_global_shutter.svg", encoding="utf-8", xml_declaration=True)


def iso_invariance_paths():
    width, height = 1500, 700
    svg = base_svg(width, height, "固定曝光下低 ISO 后期提升与高 ISO 模拟增益的比较")
    text(svg, width / 2, 43, "ISO 不改变输入电子数；它改变信号穿过下游读出链的尺度", size=31, weight="700", fill="#102a43")
    # Shared input.
    rounded_box(svg, 45, 265, 220, 130, "#edf8f2", "#9fd6b7", "固定曝光", "同一 Ne 与同一散粒涨落", "#397456")
    line(svg, 270, 330, 350, 210, stroke="#527da3", width=3, marker="arrow-blue")
    line(svg, 270, 330, 350, 500, stroke="#527da3", width=3, marker="arrow-blue")
    # High ISO path.
    text(svg, 820, 100, "路径 A：较高模拟 ISO", size=24, weight="700", fill="#a24862")
    high = [(350, "模拟增益 ×8", "信号先放大", "#fff0f3", "#eab0be"),
            (650, "下游读出噪声", "加在放大之后", "#f7efff", "#c9a9e8"),
            (950, "ADC", "较早碰到满量程", "#eaf4ff", "#9bc7ee"),
            (1250, "输出", "直接达到目标明度", "#fff7e8", "#e8c77d")]
    for x, title_value, subtitle, fill, stroke in high:
        rounded_box(svg, x, 145, 220, 130, fill, stroke, title_value, subtitle)
    for x in (575, 875, 1175):
        line(svg, x, 210, x + 65, 210, stroke="#c85b73", width=3, marker="arrow-red")
    # Low ISO path.
    text(svg, 820, 395, "路径 B：较低 ISO + 后期 ×8", size=24, weight="700", fill="#285b7a")
    low = [(350, "模拟增益 ×1", "信号保持较小", "#eaf4ff", "#9bc7ee"),
           (650, "下游读出噪声", "相对信号更显著", "#f7efff", "#c9a9e8"),
           (950, "ADC", "保留更多高光余量", "#edf8f2", "#9fd6b7"),
           (1250, "数字提升 ×8", "信号与已有噪声同乘", "#fff7e8", "#e8c77d")]
    for x, title_value, subtitle, fill, stroke in low:
        rounded_box(svg, x, 440, 220, 130, fill, stroke, title_value, subtitle)
    for x in (575, 875, 1175):
        line(svg, x, 505, x + 65, 505, stroke="#3b82b5", width=3, marker="arrow-blue")
    text(svg, width / 2, 635, "若下游读出噪声足够小，两条路径匹配后近似相同；差异称为 ISO 不变性问题", size=20, fill="#7b4b74")
    text(svg, width / 2, 671, "高 ISO 可能改善阴影数字化，却通常减少可用高光余量", size=18, fill="#627d98")
    ElementTree(svg).write(SVG_DIR / "iso_invariance_paths.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    photon_to_electron_pixel()
    quantum_efficiency_rgb()
    full_well_conversion_gain()
    cmos_readout_pipeline()
    rolling_global_shutter()
    iso_invariance_paths()


if __name__ == "__main__":
    main()
