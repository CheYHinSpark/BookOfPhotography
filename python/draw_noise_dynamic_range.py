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


def poisson_pmf(mu, k):
    if mu <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(-mu + k * math.log(mu) - math.lgamma(k + 1))


def poisson_shot_noise():
    width, height = 1500, 690
    svg = base_svg(width, height, "泊松分布与散粒噪声平方根定律")
    text(svg, width / 2, 43, "绝对涨落变大，相对涨落却按 1/√μ 缩小", size=31, weight="700", fill="#102a43")
    line(svg, 760, 82, 760, 610, stroke="#d7e0e7", width=2)
    # Left distributions.
    text(svg, 380, 92, "不同均值的泊松计数", size=24, weight="700", fill="#285b7a")
    l, r, t, b = 80, 700, 145, 540
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    curves = [
        (4, "μ=4", "#c85b73"),
        (25, "μ=25", "#3b82b5"),
        (100, "μ=100", "#4d8c6a"),
    ]
    # Map k 0..130 and normalized density so shapes coexist.
    for mu, label, color in curves:
        pts = []
        peak = max(poisson_pmf(mu, k) for k in range(131))
        for k in range(131):
            x = l + (r - l) * k / 130
            y = b - (b - t) * 0.78 * poisson_pmf(mu, k) / peak
            pts.append((x, y))
        polyline(svg, pts, stroke=color, width=4)
        x_mu = l + (r - l) * mu / 130
        line(svg, x_mu, b, x_mu, b - (b - t) * 0.80, stroke=color, width=2, dash="8 6")
        text(svg, x_mu, t + 25 + (0 if mu == 4 else 32 if mu == 25 else 64), label, size=18, weight="700", fill=color)
    text(svg, r, b + 35, "电子计数 N", size=17, fill="#627d98", anchor="end")
    text(svg, l - 8, t - 12, "归一化形状", size=16, fill="#627d98", anchor="start")
    text(svg, 380, 590, "标准差 σ=√μ；相对标准差 σ/μ=1/√μ", size=20, fill="#7b4b74")
    # Right SNR curve.
    text(svg, 1130, 92, "散粒受限 SNR = √μ", size=24, weight="700", fill="#397456")
    l2, r2, t2, b2 = 840, 1410, 145, 540
    line(svg, l2, b2, r2, b2, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l2, b2, l2, t2, stroke="#334e68", width=2, marker="arrow-dark")
    # log-log axes: mu 1..1e6, SNR 1..1e3.
    for p in range(7):
        x = l2 + (r2 - l2) * p / 6
        line(svg, x, t2, x, b2, stroke="#e0e7ec", width=1.2)
        text(svg, x, b2 + 33, f"10^{p}", size=15, fill="#627d98")
    for p in range(4):
        y = b2 - (b2 - t2) * p / 3
        line(svg, l2, y, r2, y, stroke="#e0e7ec", width=1.2)
        text(svg, l2 - 16, y + 5, f"10^{p}", size=15, fill="#627d98", anchor="end")
    pts = []
    for j in range(241):
        log_mu = 6 * j / 240
        log_snr = 0.5 * log_mu
        pts.append((l2 + (r2 - l2) * log_mu / 6, b2 - (b2 - t2) * log_snr / 3))
    polyline(svg, pts, stroke="#4d8c6a", width=5)
    for p, note in ((2, "100 e⁻ → SNR 10"), (4, "10⁴ e⁻ → SNR 100")):
        x = l2 + (r2 - l2) * p / 6
        y = b2 - (b2 - t2) * (p / 2) / 3
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "7", "fill": "#4d8c6a"})
        text(svg, x + 14, y - 15, note, size=16, weight="700", fill="#397456", anchor="start")
    text(svg, 1130, 590, "SNR 加倍需要 4 倍电子；增加一档只提高 √2", size=20, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "poisson_shot_noise.svg", encoding="utf-8", xml_declaration=True)


def noise_budget():
    width, height = 1500, 700
    svg = base_svg(width, height, "信号相关噪声预算与光子转移曲线")
    text(svg, width / 2, 43, "噪声源按方差相加，主导项随信号区间改变", size=31, weight="700", fill="#102a43")
    line(svg, 750, 82, 750, 625, stroke="#d7e0e7", width=2)
    # Left sigma budget log-log.
    text(svg, 375, 92, "输入电子尺度上的标准差", size=24, weight="700", fill="#285b7a")
    l, r, t, b = 90, 690, 145, 545
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    # x log μ -1..5; y log σ -1..3.
    for p in range(-1, 6):
        x = l + (r - l) * (p + 1) / 6
        line(svg, x, t, x, b, stroke="#e0e7ec", width=1.2)
        text(svg, x, b + 32, f"10^{p}", size=14, fill="#627d98")
    for p in range(-1, 4):
        y = b - (b - t) * (p + 1) / 4
        line(svg, l, y, r, y, stroke="#e0e7ec", width=1.2)
        text(svg, l - 15, y + 5, f"10^{p}", size=14, fill="#627d98", anchor="end")
    sigma_r = 2.0
    mu_dark = 9.0
    alpha = 0.006
    funcs = [
        ("读出 σr", "#7b4b74", lambda mu: sigma_r, "10 7"),
        ("散粒 √μ", "#3b82b5", lambda mu: math.sqrt(mu), None),
        ("暗电流 √μd", "#c58a2d", lambda mu: math.sqrt(mu_dark), "5 6"),
        ("PRNU αμ", "#c85b73", lambda mu: alpha * mu, "12 6"),
        ("总标准差", "#4d8c6a", lambda mu: math.sqrt(sigma_r**2 + mu + mu_dark + (alpha * mu)**2), None),
    ]
    for label, color, func, dash in funcs:
        pts = []
        for j in range(241):
            lx = -1 + 6 * j / 240
            mu = 10 ** lx
            ly = max(-1, min(3, math.log10(func(mu))))
            pts.append((l + (r - l) * (lx + 1) / 6, b - (b - t) * (ly + 1) / 4))
        polyline(svg, pts, stroke=color, width=4 if label == "总标准差" else 3, dash=dash)
    labels = [(550, 208, "总标准差", "#397456"), (520, 300, "散粒", "#285b7a"), (470, 445, "读出/暗电流", "#7b4b74"), (610, 390, "PRNU", "#a24862")]
    for x, y, value, color in labels:
        text(svg, x, y, value, size=17, weight="700", fill=color)
    text(svg, 375, 600, "低信号：读出主导；中信号：散粒主导；高信号空间比较：PRNU 可主导", size=18, fill="#627d98")
    # Right photon transfer variance.
    text(svg, 1125, 92, "均值—方差（光子转移）", size=24, weight="700", fill="#397456")
    l2, r2, t2, b2 = 830, 1410, 145, 545
    line(svg, l2, b2, r2, b2, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l2, b2, l2, t2, stroke="#334e68", width=2, marker="arrow-dark")
    for p in range(0, 6):
        x = l2 + (r2 - l2) * p / 5
        y = b2 - (b2 - t2) * p / 6
        line(svg, x, t2, x, b2, stroke="#e0e7ec", width=1.2)
        text(svg, x, b2 + 32, f"10^{p}", size=14, fill="#627d98")
        if p < 5:
            line(svg, l2, y, r2, y, stroke="#e0e7ec", width=1.2)
    pts_linear, pts_total = [], []
    for j in range(241):
        lx = 5 * j / 240
        mu = 10 ** lx
        var_linear = sigma_r**2 + mu
        var_total = sigma_r**2 + mu + (alpha * mu)**2
        for arr, var in ((pts_linear, var_linear), (pts_total, var_total)):
            ly = max(0, min(6, math.log10(var)))
            arr.append((l2 + (r2 - l2) * lx / 5, b2 - (b2 - t2) * ly / 6))
    polyline(svg, pts_linear, stroke="#3b82b5", width=4)
    polyline(svg, pts_total, stroke="#c85b73", width=4, dash="10 7")
    text(svg, 1000, 360, "斜率 1：散粒区", size=17, weight="700", fill="#285b7a")
    text(svg, 1250, 225, "高信号上翘：PRNU", size=17, weight="700", fill="#a24862")
    text(svg, 850, 510, "截距：读出方差", size=16, fill="#7b4b74", anchor="start")
    text(svg, 1125, 600, "成对平场相减可去除稳定图样，估计时间方差", size=18, fill="#627d98")
    ElementTree(svg).write(SVG_DIR / "noise_budget.svg", encoding="utf-8", xml_declaration=True)


def dynamic_range_definitions():
    width, height = 1500, 650
    svg = base_svg(width, height, "动态范围阈值与高光余量的不同定义")
    text(svg, width / 2, 43, "动态范围不是单一自然数：下限取决于可用性阈值", size=31, weight="700", fill="#102a43")
    x0, x1, y = 125, 1380, 310
    line(svg, x0, y, x1, y, stroke="#334e68", width=5, marker="arrow-dark")
    # log electron positions 1..1e5.
    def xp(value):
        return x0 + (x1 - x0) * math.log10(value) / 5
    ticks = [1, 2, 3, 10, 100, 1000, 10000, 60000]
    labels = {
        1: "1 e⁻", 2: "σr=2", 3: "SNR≈1", 10: "10 e⁻",
        100: "SNR≈10", 1000: "中间调", 10000: "高光", 60000: "饱和 6×10⁴",
    }
    colors = {1: "#627d98", 2: "#7b4b74", 3: "#c58a2d", 10: "#627d98", 100: "#3b82b5", 1000: "#4d8c6a", 10000: "#c58a2d", 60000: "#c85b73"}
    for idx, value in enumerate(ticks):
        x = xp(value)
        h = 72 if idx % 2 == 0 else 48
        line(svg, x, y - h, x, y + h, stroke=colors[value], width=3)
        text(svg, x, y - h - 18 if idx % 2 == 0 else y + h + 30, labels[value], size=16, weight="700", fill=colors[value])
    # DR arrows.
    levels = [(430, 2, 60000, "工程 DR：满阱 / σr", "#7b4b74"), (500, 3, 60000, "SNR=1 阈值", "#c58a2d"), (570, 100, 60000, "照片可用阈值 SNR=10", "#3b82b5")]
    for yy, low, high, label, color in levels:
        line(svg, xp(low), yy, xp(high), yy, stroke=color, width=4)
        line(svg, xp(low), yy - 10, xp(low), yy + 10, stroke=color, width=3)
        line(svg, xp(high), yy - 10, xp(high), yy + 10, stroke=color, width=3)
        text(svg, (xp(low) + xp(high)) / 2, yy - 15, label, size=17, weight="700", fill=color)
    # Highlight headroom.
    x_ref = xp(10000)
    x_sat = xp(60000)
    line(svg, x_ref, 165, x_sat, 165, stroke="#c85b73", width=5)
    line(svg, x_ref, 153, x_ref, 177, stroke="#c85b73", width=3)
    line(svg, x_sat, 153, x_sat, 177, stroke="#c85b73", width=3)
    text(svg, (x_ref + x_sat) / 2, 135, "高光余量 = log₂(Nsat/Nhighlight)", size=18, weight="700", fill="#a24862")
    text(svg, width / 2, 95, "示例：Nsat=60000 e⁻，σr=2 e⁻；不同阈值给出不同“档数”", size=20, fill="#627d98")
    ElementTree(svg).write(SVG_DIR / "dynamic_range_definitions.svg", encoding="utf-8", xml_declaration=True)


def ettr_constraints():
    width, height = 1500, 690
    svg = base_svg(width, height, "ETTR 在饱和约束下提高曝光尺度")
    text(svg, width / 2, 43, "ETTR 是带约束的最大化，不是让直方图无条件碰右", size=31, weight="700", fill="#102a43")
    panels = [
        (250, "曝光不足", 0.48, "#7b4b74"),
        (750, "约束内右移", 0.78, "#4d8c6a"),
        (1250, "越界裁切", 1.03, "#c85b73"),
    ]
    for idx, (cx, title_value, shift, color) in enumerate(panels):
        if idx:
            line(svg, cx - 250, 90, cx - 250, 590, stroke="#d7e0e7", width=2)
        text(svg, cx, 95, title_value, size=23, weight="700", fill=color)
        l, r, t, b = cx - 205, cx + 205, 150, 500
        line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
        line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
        sat_x = r - 35
        line(svg, sat_x, t, sat_x, b, stroke="#c85b73", width=3, dash="8 6")
        text(svg, sat_x, t - 15, "饱和", size=16, weight="700", fill="#a24862")
        pts = []
        for j in range(220):
            u = j / 219
            xbase = -3.2 + 6.4 * u
            value = (0.9 * math.exp(-0.5 * ((xbase + 0.8) / 0.9) ** 2)
                     + 0.35 * math.exp(-0.5 * ((xbase - 1.7) / 0.38) ** 2))
            shifted = u * 0.60 + shift * 0.52 - 0.28
            x = l + (r - l) * shifted
            yv = b - (b - t) * value / 1.0
            pts.append((x, yv))
        # Clip points at saturation for visual display.
        clipped = [(min(x, sat_x), yv) for x, yv in pts]
        polyline(svg, clipped, stroke=color, width=4)
        if title_value == "越界裁切":
            SubElement(svg, "rect", {"x": str(sat_x), "y": str(t + 45), "width": str(r - sat_x), "height": str(b - t - 45), "fill": "#f8dce3", "fill-opacity": ".65"})
            text(svg, sat_x - 10, 245, "重要高光丢失", size=16, weight="700", fill="#a24862", anchor="end")
        elif title_value == "约束内右移":
            text(svg, cx, 555, "阴影电子数增加，重要高光仍有余量", size=17, weight="700", fill="#397456")
        else:
            text(svg, cx, 555, "高光安全，但阴影受读出噪声影响更大", size=17, fill="#7b4b74")
    text(svg, width / 2, 635, "还必须满足运动、景深、衍射、闪烁、温升和测光不确定度等约束", size=20, fill="#627d98")
    ElementTree(svg).write(SVG_DIR / "ettr_constraints.svg", encoding="utf-8", xml_declaration=True)


def channel_clipping():
    width, height = 1450, 650
    svg = base_svg(width, height, "彩色通道饱和导致比例信息丢失")
    text(svg, width / 2, 43, "通道饱和不是“变白”这么简单，而是比例约束变成不等式", size=31, weight="700", fill="#102a43")
    panels = [
        (250, "均未饱和", [0.75, 0.58, 0.42], "比例可测", "#4d8c6a"),
        (725, "红通道饱和", [1.0, 0.70, 0.50], "只知 R ≥ 上限", "#c58a2d"),
        (1200, "三通道饱和", [1.0, 1.0, 1.0], "只剩亮度下界", "#c85b73"),
    ]
    bar_colors = ["#c85b73", "#4d9f69", "#536fc5"]
    labels = ["R", "G", "B"]
    for idx, (cx, title_value, values, note, color) in enumerate(panels):
        if idx:
            line(svg, cx - 237, 90, cx - 237, 585, stroke="#d7e0e7", width=2)
        text(svg, cx, 95, title_value, size=23, weight="700", fill=color)
        x0, y0 = cx - 150, 480
        for j, (value, bcolor, label) in enumerate(zip(values, bar_colors, labels)):
            x = x0 + j * 110
            height = 300 * value
            SubElement(svg, "rect", {"x": str(x), "y": str(y0 - height), "width": "65", "height": str(height), "rx": "7", "fill": bcolor, "fill-opacity": ".72", "stroke": bcolor, "stroke-width": "2"})
            text(svg, x + 32, y0 + 34, label, size=18, weight="700", fill=bcolor)
            if value >= 0.999:
                line(svg, x - 6, y0 - 300, x + 72, y0 - 300, stroke="#a24862", width=4)
        line(svg, x0 - 20, y0 - 300, x0 + 3 * 110 - 25, y0 - 300, stroke="#a24862", width=2, dash="8 6")
        text(svg, cx, 540, note, size=18, weight="700", fill=color)
    text(svg, width / 2, 610, "高光重建必须借助邻域、其他曝光或材料先验；它是推断，不是读取被裁切的原值", size=20, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "channel_clipping.svg", encoding="utf-8", xml_declaration=True)


def format_pixel_binning():
    width, height = 1500, 690
    svg = base_svg(width, height, "像素面积传感器面积与像素合并的信号统计")
    text(svg, width / 2, 43, "比较像素前先决定：固定单位面积、整块传感器，还是同尺寸输出", size=31, weight="700", fill="#102a43")
    line(svg, 760, 82, 760, 610, stroke="#d7e0e7", width=2)
    # Left geometry.
    text(svg, 380, 92, "同一感光面积：一个大像素 vs 四个小像素", size=23, weight="700", fill="#285b7a")
    SubElement(svg, "rect", {"x": "105", "y": "165", "width": "230", "height": "230", "fill": "#eaf4ff", "stroke": "#3b82b5", "stroke-width": "4"})
    text(svg, 220, 285, "4μ", size=30, weight="700", fill="#285b7a")
    text(svg, 220, 430, "一个读出节点", size=17, fill="#627d98")
    x0, y0, cell = 435, 165, 115
    for row in range(2):
        for col in range(2):
            SubElement(svg, "rect", {"x": str(x0 + col * cell), "y": str(y0 + row * cell), "width": str(cell), "height": str(cell), "fill": "#edf8f2", "stroke": "#4d8c6a", "stroke-width": "3"})
            text(svg, x0 + col * cell + cell / 2, y0 + row * cell + cell / 2 + 8, "μ", size=24, weight="700", fill="#397456")
    text(svg, 550, 430, "四个读出节点", size=17, fill="#627d98")
    line(svg, 345, 280, 420, 280, stroke="#527da3", width=3, marker="arrow-blue")
    text(svg, 380, 500, "光子总数相同；分别读出时，读出方差会相加", size=19, fill="#7b4b74")
    # Right formulas and output normalization.
    text(svg, 1130, 92, "合并方式决定信号与噪声的缩放", size=23, weight="700", fill="#397456")
    rounded_box(svg, 835, 155, 590, 115, "#edf8f2", "#9fd6b7", "数字求和 n 个像素", "S=nμ，Var=nμ+nσᵣ²", "#397456")
    rounded_box(svg, 835, 315, 590, 115, "#eaf4ff", "#9bc7ee", "数字平均后保持相同输出尺度", "均值=μ，标准差=√(μ+σᵣ²)/√n", "#285b7a")
    rounded_box(svg, 835, 475, 590, 115, "#fff7e8", "#e8c77d", "电荷域合并", "若只读出一次，可少付部分读出噪声", "#8a5f19")
    text(svg, width / 2, 650, "更大传感器在同 f 数、快门与场景辐亮度下接收更多总光；像素尺寸只是分割方式之一", size=20, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "format_pixel_binning.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    poisson_shot_noise()
    noise_budget()
    dynamic_range_definitions()
    ettr_constraints()
    channel_clipping()
    format_pixel_binning()


if __name__ == "__main__":
    main()
