from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
import math
import random


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
        text(parent, r, b + 31, x_label, size=15, fill="#627d98", anchor="end")
    if y_label:
        text(parent, l - 4, t - 12, y_label, size=15, fill="#627d98", anchor="start")


def srgb_oetf(x):
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055


def srgb_eotf(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def encoding_pipeline():
    width, height = 1500, 700
    svg = base_svg(width, height, "场景线性光经OETF编码传输再由EOTF形成显示亮度")
    text(svg, width / 2, 43, "OETF、编码与 EOTF 分属不同物理域", size=31, weight="700", fill="#102a43")
    blocks = [
        (35, "场景线性光", "Lscene ∝ 辐亮度/曝光", "#eaf4ff", "#9bc7ee"),
        (330, "创作与映射", "曝光 · 色调 · OOTF", "#fff7e8", "#e8c77d"),
        (625, "OETF", "V = E(L)", "#edf8f2", "#9fd6b7"),
        (920, "码值与传输", "量化 · 存储 · 压缩", "#f7efff", "#c9a9e8"),
        (1215, "显示 EOTF", "Ld = D(V)", "#fff0f3", "#eab0be"),
    ]
    for x, title_value, subtitle, fill, stroke in blocks:
        rounded_box(svg, x, 120, 250, 125, fill, stroke, title_value, subtitle)
    for x in (285, 580, 875, 1170):
        line(svg, x, 182, x + 38, 182, stroke="#527da3", width=3, marker="arrow-blue")
    # Domain labels.
    labels = [
        (160, 285, "物理/场景参照"), (455, 285, "外观意图"),
        (750, 285, "非线性编码"), (1045, 285, "数字码域"), (1340, 285, "显示光域"),
    ]
    for x, y, value in labels:
        text(svg, x, y, value, size=16, weight="700", fill="#7b4b74")
    # Bottom: transfer composition.
    rounded_box(svg, 155, 380, 520, 165, "#eef5fb", "#a8c8e0", "整体系统变换", "Ld = EOTF(OETF(creative(Lscene)))", "#285b7a")
    text(svg, 415, 510, "匹配的编解码可近似互逆；创作 OOTF 通常不恒等", size=16, fill="#486581")
    rounded_box(svg, 825, 380, 520, 165, "#fff0f3", "#eab0be", "常见错误", "在线性运算前忘记逆 OETF", "#a24862")
    text(svg, 1085, 510, "矩阵、卷积、平均与透明混合会得到错误能量关系", size=16, fill="#486581")
    rounded_box(svg, 255, 600, 990, 62, "#edf8f2", "#9fd6b7", "场景参照数值回答“测到了多少光”；显示参照数值回答“设备应发出多少光”", None, "#397456")
    ElementTree(svg).write(SVG_DIR / "encoding_pipeline.svg", encoding="utf-8", xml_declaration=True)


def transfer_curves():
    width, height = 1500, 720
    svg = base_svg(width, height, "线性sRGB和幂律的OETF与EOTF曲线")
    text(svg, width / 2, 43, "非线性编码把更多码值分配给低亮度，但不改变原始光子统计", size=31, weight="700", fill="#102a43")
    line(svg, 750, 85, 750, 655, stroke="#d7e0e7", width=2)
    panels = [(70, 690, "OETF：线性光 → 码值", True), (810, 1430, "EOTF：码值 → 显示光", False)]
    for l, r, title_value, encode in panels:
        text(svg, (l + r) / 2, 105, title_value, size=23, weight="700", fill="#285b7a" if encode else "#a24862")
        pl, pr, pt, pb = l + 40, r - 30, 160, 545
        axes(svg, pl, pr, pt, pb, "输入", "输出")
        for q in (0, 0.25, 0.5, 0.75, 1.0):
            x = pl + (pr - pl) * q
            y = pb - (pb - pt) * q
            line(svg, x, pt, x, pb, stroke="#e0e7ec", width=1)
            line(svg, pl, y, pr, y, stroke="#e0e7ec", width=1)
        funcs = [
            (lambda x: x, "线性", "#8aa2b5", "8 5"),
            ((lambda x: srgb_oetf(x)) if encode else (lambda x: srgb_eotf(x)), "sRGB", "#3b82b5", None),
            ((lambda x: x ** (1 / 2.2)) if encode else (lambda x: x ** 2.2), "幂律 2.2", "#7b4b74", None),
        ]
        for func, label, color, dash in funcs:
            pts = []
            for j in range(201):
                u = j / 200
                v = max(0, min(1, func(u)))
                pts.append((pl + (pr - pl) * u, pb - (pb - pt) * v))
            polyline(svg, pts, stroke=color, width=4, dash=dash)
        legend_y = 600
        for idx, (_, label, color, dash) in enumerate(funcs):
            x = l + 150 + idx * 165
            line(svg, x - 52, legend_y - 6, x - 10, legend_y - 6, stroke=color, width=4, dash=dash)
            text(svg, x, legend_y, label, size=15, weight="700", fill=color, anchor="start")
    text(svg, 375, 665, "暗部被拉开：相同码差对应更小的线性光差", size=17, fill="#397456")
    text(svg, 1125, 665, "显示端把码值重新弯回物理亮度", size=17, fill="#a24862")
    ElementTree(svg).write(SVG_DIR / "transfer_curves.svg", encoding="utf-8", xml_declaration=True)


def linear_encoded_mixing():
    width, height = 1500, 700
    svg = base_svg(width, height, "在线性光和sRGB编码域平均黑白的不同结果")
    text(svg, width / 2, 43, "平均、卷积和透明混合必须在线性光域进行", size=31, weight="700", fill="#102a43")
    line(svg, 750, 88, 750, 645, stroke="#d7e0e7", width=2)
    # Correct path.
    text(svg, 375, 100, "正确：先解码到线性光", size=24, weight="700", fill="#397456")
    rounded_box(svg, 70, 150, 210, 120, "#111820", "#111820", "黑", "L=0", "#ffffff")
    rounded_box(svg, 470, 150, 210, 120, "#ffffff", "#9fb3c2", "白", "L=1", "#102a43")
    text(svg, 375, 220, "+", size=34, weight="700", fill="#334e68")
    line(svg, 190, 300, 560, 300, stroke="#4d8c6a", width=4, marker="arrow-green")
    text(svg, 375, 335, "线性平均：(0+1)/2 = 0.5", size=19, weight="700", fill="#397456")
    gray_linear_code = srgb_oetf(0.5)
    shade = round(gray_linear_code * 255)
    color = f"#{shade:02x}{shade:02x}{shade:02x}"
    rounded_box(svg, 220, 380, 310, 125, color, "#4d8c6a", "线性 50% 灰", f"编码值 ≈ {gray_linear_code:.3f}", "#ffffff")
    text(svg, 375, 565, "显示光确为白色亮度的一半", size=18, fill="#486581")
    # Incorrect path.
    text(svg, 1125, 100, "错误：直接平均编码码值", size=24, weight="700", fill="#a24862")
    rounded_box(svg, 820, 150, 210, 120, "#111820", "#111820", "黑码", "V=0", "#ffffff")
    rounded_box(svg, 1220, 150, 210, 120, "#ffffff", "#9fb3c2", "白码", "V=1", "#102a43")
    text(svg, 1125, 220, "+", size=34, weight="700", fill="#334e68")
    line(svg, 940, 300, 1310, 300, stroke="#c85b73", width=4, marker="arrow-red")
    text(svg, 1125, 335, "码值平均：(0+1)/2 = 0.5", size=19, weight="700", fill="#a24862")
    shade2 = round(0.5 * 255)
    color2 = f"#{shade2:02x}{shade2:02x}{shade2:02x}"
    rounded_box(svg, 970, 380, 310, 125, color2, "#c85b73", "编码 50% 灰", f"解码线性光 ≈ {srgb_eotf(0.5):.3f}", "#ffffff")
    text(svg, 1125, 565, "只有约 21.4% 的白色线性亮度", size=18, fill="#a24862")
    rounded_box(svg, 285, 610, 930, 58, "#fff7e8", "#e8c77d", "相同的“0.5”在不同域中代表不同物理量；先确认坐标域，再进行运算", None, "#8a5f19")
    ElementTree(svg).write(SVG_DIR / "linear_encoded_mixing.svg", encoding="utf-8", xml_declaration=True)


def quantization_dither():
    width, height = 1500, 740
    svg = base_svg(width, height, "均匀量化的阶梯误差与加入抖动后的误差去相关")
    text(svg, width / 2, 43, "量化把连续值分箱；抖动用随机性换取误差去相关", size=31, weight="700", fill="#102a43")
    # Top quantized ramp.
    l, r, t, b = 100, 1400, 125, 365
    axes(svg, l, r, t, b, "位置", "值")
    pts_line = [(l, b), (r, t + 20)]
    polyline(svg, pts_line, stroke="#9fb3c2", width=3, dash="8 5")
    levels = 8
    step_pts = []
    for j in range(401):
        u = j / 400
        q = round(u * (levels - 1)) / (levels - 1)
        step_pts.append((l + (r - l) * u, b - (b - t - 20) * q))
    polyline(svg, step_pts, stroke="#3b82b5", width=5)
    text(svg, 420, 165, "理想连续渐变", size=16, fill="#627d98")
    text(svg, 1050, 235, "3 bit：8 个台阶", size=18, weight="700", fill="#285b7a")
    # Bottom errors.
    line(svg, 750, 405, 750, 690, stroke="#d7e0e7", width=2)
    text(svg, 375, 430, "无抖动：误差与信号锁定", size=22, weight="700", fill="#a24862")
    text(svg, 1125, 430, "有抖动：单像素更噪，但平均无偏", size=22, weight="700", fill="#397456")
    # No dither sawtooth.
    l1, r1, mid1 = 80, 680, 555
    line(svg, l1, mid1, r1, mid1, stroke="#8aa2b5", width=2)
    pts = []
    for j in range(301):
        u = j / 300
        q = round(u * (levels - 1)) / (levels - 1)
        err = q - u
        pts.append((l1 + (r1 - l1) * u, mid1 - 650 * err))
    polyline(svg, pts, stroke="#c85b73", width=3)
    text(svg, 375, 650, "轮廓与条带来自这种周期相关误差", size=16, fill="#a24862")
    # Dither scatter and mean.
    random.seed(14)
    l2, r2, mid2 = 820, 1420, 555
    line(svg, l2, mid2, r2, mid2, stroke="#8aa2b5", width=2)
    for j in range(140):
        u = j / 139
        d = (random.random() - 0.5) / (levels - 1)
        q = round(max(0, min(1, u + d)) * (levels - 1)) / (levels - 1)
        err = q - u
        x = l2 + (r2 - l2) * u
        y = mid2 - 600 * err
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "3.5", "fill": "#4d8c6a", "fill-opacity": "0.62"})
    line(svg, l2, mid2, r2, mid2, stroke="#3b82b5", width=3, dash="8 5")
    text(svg, 1120, 650, "空间或时间低通后可恢复亚码级平均", size=16, fill="#397456")
    ElementTree(svg).write(SVG_DIR / "quantization_dither.svg", encoding="utf-8", xml_declaration=True)


def bitdepth_allocation():
    width, height = 1500, 720
    svg = base_svg(width, height, "线性编码与幂律编码在各曝光档分配码值的差异")
    text(svg, width / 2, 43, "位深给出码位数量；传递曲线决定这些码位分配到哪些亮度区间", size=31, weight="700", fill="#102a43")
    line(svg, 750, 90, 750, 650, stroke="#d7e0e7", width=2)
    # Bars per stop.
    stops = list(range(1, 9))
    for side, title_value, color, gamma in ((0, "8 bit 线性编码", "#3b82b5", None), (1, "8 bit 幂律编码 γ=2.2", "#7b4b74", 2.2)):
        x0 = 70 + side * 740
        text(svg, x0 + 300, 105, title_value, size=23, weight="700", fill=color)
        chart_l, chart_r, chart_t, chart_b = x0 + 80, x0 + 620, 160, 570
        line(svg, chart_l, chart_b, chart_r, chart_b, stroke="#334e68", width=2)
        max_count = 128 if gamma is None else 70
        counts = []
        for k in stops:
            hi = 2 ** (-(k - 1))
            lo = 2 ** (-k)
            if gamma is None:
                count = 255 * (hi - lo)
            else:
                count = 255 * (hi ** (1 / gamma) - lo ** (1 / gamma))
            counts.append(count)
        for idx, (k, count) in enumerate(zip(stops, counts)):
            bw = 42
            x = chart_l + 18 + idx * 62
            h = 330 * count / max_count
            SubElement(svg, "rect", {"x": str(x), "y": str(chart_b - h), "width": str(bw), "height": str(h), "rx": "5", "fill": color, "fill-opacity": "0.65"})
            text(svg, x + bw / 2, chart_b + 25, f"−{k}", size=13, fill="#627d98")
            text(svg, x + bw / 2, chart_b - h - 9, f"{count:.0f}", size=12, weight="700", fill=color)
        text(svg, (chart_l + chart_r) / 2, 615, "低于满幅的曝光档 / EV", size=16, fill="#627d98")
        if side == 0:
            text(svg, x0 + 300, 660, "最亮一档独占约一半码值；暗部迅速只剩少量码", size=17, fill="#285b7a")
        else:
            text(svg, x0 + 300, 660, "码值分布更接近感知需求，但并非增加物理测量", size=17, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "bitdepth_allocation.svg", encoding="utf-8", xml_declaration=True)


def tone_curve_geometry():
    width, height = 1500, 720
    svg = base_svg(width, height, "单调色调曲线的toe中间调shoulder与局部斜率")
    text(svg, width / 2, 43, "色调曲线重新分配对比：局部斜率决定邻近亮度差如何变化", size=31, weight="700", fill="#102a43")
    line(svg, 750, 85, 750, 660, stroke="#d7e0e7", width=2)
    # Left curve.
    text(svg, 375, 105, "单调 S 曲线", size=24, weight="700", fill="#285b7a")
    l, r, t, b = 90, 690, 155, 585
    axes(svg, l, r, t, b, "输入 x", "输出 T(x)")
    a = 7.0
    lo = 1 / (1 + math.exp(a / 2))
    hi = 1 / (1 + math.exp(-a / 2))
    pts = []
    for j in range(301):
        u = j / 300
        raw = 1 / (1 + math.exp(-a * (u - 0.5)))
        v = (raw - lo) / (hi - lo)
        pts.append((l + (r - l) * u, b - (b - t) * v))
    polyline(svg, pts, stroke="#3b82b5", width=5)
    line(svg, l, b, r, t, stroke="#8aa2b5", width=2, dash="8 5")
    annotations = [(0.18, "toe", "#7b4b74"), (0.50, "中间调高斜率", "#4d8c6a"), (0.83, "shoulder", "#c85b73")]
    for u, label, color in annotations:
        raw = 1 / (1 + math.exp(-a * (u - 0.5)))
        v = (raw - lo) / (hi - lo)
        x = l + (r - l) * u
        y = b - (b - t) * v
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "7", "fill": color})
        text(svg, x + (20 if u < .7 else -20), y - 18, label, size=16, weight="700", fill=color, anchor="start" if u < .7 else "end")
    text(svg, 375, 630, "端点固定时，提高某段对比必然挤压其他区间", size=17, fill="#7b4b74")
    # Right derivative/local contrast.
    text(svg, 1125, 105, "局部对比增益", size=24, weight="700", fill="#a24862")
    l2, r2, t2, b2 = 830, 1420, 155, 585
    axes(svg, l2, r2, t2, b2, "输入 x", "T′(x)")
    pts = []
    for j in range(301):
        u = j / 300
        raw = 1 / (1 + math.exp(-a * (u - 0.5)))
        deriv = a * raw * (1 - raw) / (hi - lo)
        v = min(2.0, deriv) / 2.0
        pts.append((l2 + (r2 - l2) * u, b2 - (b2 - t2) * v))
    polyline(svg, pts, stroke="#c85b73", width=5)
    y1 = b2 - (b2 - t2) * 0.5
    line(svg, l2, y1, r2, y1, stroke="#8aa2b5", width=2, dash="8 5")
    text(svg, r2 - 10, y1 - 12, "斜率 1：局部对比不变", size=15, fill="#627d98", anchor="end")
    text(svg, 1125, 630, "曝光域对比增益还可写为 xT′(x)/T(x)", size=17, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "tone_curve_geometry.svg", encoding="utf-8", xml_declaration=True)


def global_local_tonemap():
    width, height = 1500, 740
    svg = base_svg(width, height, "全局与局部色调映射及对数亮度的基底细节分解")
    text(svg, width / 2, 43, "全局映射对同一输入给同一输出；局部映射还依赖邻域", size=31, weight="700", fill="#102a43")
    # Top three concepts.
    rounded_box(svg, 35, 105, 390, 260, "#eaf4ff", "#9bc7ee", "HDR 输入", "跨越许多曝光档", "#285b7a")
    for idx, val in enumerate([0.05, 0.12, 0.3, 0.7, 1.8, 4.5, 12, 35]):
        x = 75 + idx * 39
        h = 35 + 150 * math.log1p(val) / math.log1p(35)
        shade = int(245 - 145 * math.log1p(val) / math.log1p(35))
        SubElement(svg, "rect", {"x": str(x), "y": str(320 - h), "width": "31", "height": str(h), "fill": f"#{shade:02x}{shade:02x}{shade:02x}", "stroke": "#627d98", "stroke-width": "1"})
    rounded_box(svg, 555, 105, 390, 260, "#edf8f2", "#9fd6b7", "全局 T(L)", "每个像素只看自身亮度", "#397456")
    l, r, t, b = 610, 890, 205, 325
    pts = []
    for j in range(151):
        u = 8 * j / 150
        v = u / (1 + u)
        pts.append((l + (r - l) * u / 8, b - (b - t) * v))
    polyline(svg, pts, stroke="#4d8c6a", width=4)
    text(svg, 750, 330, "T(L)=L/(1+L)", size=16, weight="700", fill="#397456")
    rounded_box(svg, 1075, 105, 390, 260, "#fff0f3", "#eab0be", "局部 T(L,x,y)", "同一输入可因邻域而不同", "#a24862")
    for idx in range(9):
        cx = 1125 + idx * 35
        base = 280 - 70 * math.sin(idx * math.pi / 8)
        SubElement(svg, "circle", {"cx": str(cx), "cy": str(base), "r": str(10 + 8 * (idx % 3)), "fill": "#c85b73", "fill-opacity": str(0.25 + 0.07 * idx)})
    text(svg, 1270, 330, "增强局部结构，也可能制造光晕", size=16, fill="#a24862")
    line(svg, 430, 235, 545, 235, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Global and local operators are parallel alternatives fed by the same HDR input.
    line(svg, 470, 235, 470, 82, stroke="#3b82b5", width=4)
    line(svg, 470, 82, 1025, 82, stroke="#3b82b5", width=4)
    line(svg, 1025, 82, 1025, 235, stroke="#3b82b5", width=4)
    line(svg, 1025, 235, 1065, 235, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Bottom decomposition.
    text(svg, 750, 420, "对数亮度的基底-细节分解", size=23, weight="700", fill="#7b4b74")
    blocks = [
        (65, "ℓ=log L", "对数亮度", "#eaf4ff", "#9bc7ee"),
        (365, "b=Gσ*ℓ", "平滑基底", "#fff7e8", "#e8c77d"),
        (665, "d=ℓ−b", "局部细节", "#f7efff", "#c9a9e8"),
        (965, "ℓ′=αb+βd", "压基底/保细节", "#edf8f2", "#9fd6b7"),
        (1265, "L′=exp ℓ′", "输出", "#fff0f3", "#eab0be"),
    ]
    for x, title_value, subtitle, fill, stroke in blocks:
        rounded_box(svg, x, 465, 190, 120, fill, stroke, title_value, subtitle)
    for x in (260, 560, 860, 1160):
        line(svg, x, 525, x + 95, 525, stroke="#527da3", width=3, marker="arrow-blue")
    rounded_box(svg, 240, 630, 1020, 68, "#fff7e8", "#e8c77d", "边缘不保持的平滑会让基底跨越物体边界，重组后形成 halo；细节增益也会放大噪声", None, "#8a5f19")
    ElementTree(svg).write(SVG_DIR / "global_local_tonemap.svg", encoding="utf-8", xml_declaration=True)


def hdr_display_mapping():
    width, height = 1500, 720
    svg = base_svg(width, height, "场景曝光范围映射到SDR与HDR显示亮度范围")
    text(svg, width / 2, 43, "色调映射压缩场景范围；它改变表达，不扩展显示器物理对比度", size=31, weight="700", fill="#102a43")
    # Scene axis.
    text(svg, 190, 105, "场景相对曝光 / EV", size=21, weight="700", fill="#285b7a")
    x_scene = 190
    y_top, y_bottom = 150, 625
    line(svg, x_scene, y_bottom, x_scene, y_top, stroke="#334e68", width=4, marker="arrow-dark")
    for k in range(-10, 7, 2):
        y = y_bottom - (k + 10) / 16 * (y_bottom - y_top)
        line(svg, x_scene - 12, y, x_scene + 12, y, stroke="#334e68", width=2)
        text(svg, x_scene - 24, y + 5, f"{k:+d}", size=14, fill="#627d98", anchor="end")
    # Two output bars.
    outputs = [
        (650, "SDR 显示", "约 0.1–100 cd/m²", "#3b82b5", 0.24),
        (1120, "HDR 显示", "约 0.005–1000 cd/m²", "#7b4b74", 0.48),
    ]
    for x, title_value, subtitle, color, span in outputs:
        text(svg, x, 105, title_value, size=22, weight="700", fill=color)
        text(svg, x, 132, subtitle, size=15, fill="#486581")
        SubElement(svg, "rect", {"x": str(x - 48), "y": str(y_top), "width": "96", "height": str(y_bottom - y_top), "rx": "20", "fill": "#eef2f5", "stroke": color, "stroke-width": "3"})
        for j in range(80):
            u = j / 79
            shade = int(18 + 230 * u)
            SubElement(svg, "rect", {"x": str(x - 42), "y": str(y_bottom - 6 - (j + 1) * (y_bottom - y_top - 12) / 80), "width": "84", "height": str((y_bottom - y_top - 12) / 80 + 1), "fill": f"#{shade:02x}{shade:02x}{shade:02x}"})
        # Mapping curves from scene axis to bar.
        for ev, label in [(-8, "阴影"), (-2, "中间调"), (5, "高光")]:
            ys = y_bottom - (ev + 10) / 16 * (y_bottom - y_top)
            if x == 650:
                u = 1 / (1 + math.exp(-0.45 * (ev + 2)))
            else:
                u = 1 / (1 + math.exp(-0.30 * (ev + 2)))
            yo = y_bottom - u * (y_bottom - y_top)
            line(svg, x_scene + 12, ys, x - 55, yo, stroke=color, width=2, dash="7 5")
            if x == 1120:
                text(svg, x + 70, yo + 5, label, size=14, fill=color, anchor="start")
    rounded_box(svg, 355, 640, 970, 58, "#fff0f3", "#eab0be", "显示黑位还会被环境反射抬高；峰值、黑位与观看环境共同决定有效对比度", None, "#a24862")
    ElementTree(svg).write(SVG_DIR / "hdr_display_mapping.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    encoding_pipeline()
    transfer_curves()
    linear_encoded_mixing()
    quantization_dither()
    bitdepth_allocation()
    tone_curve_geometry()
    global_local_tonemap()
    hdr_display_mapping()


if __name__ == "__main__":
    main()
