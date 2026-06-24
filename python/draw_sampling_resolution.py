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


def polygon(parent, points, fill, stroke="none", width=1):
    return SubElement(parent, "polygon", {
        "points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points),
        "fill": fill, "stroke": stroke, "stroke-width": str(width),
    })


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
    grad = SubElement(defs, "linearGradient", {"id": "irradiance", "x1": "0", "x2": "1", "y1": "0", "y2": "0"})
    SubElement(grad, "stop", {"offset": "0", "stop-color": "#eaf4ff"})
    SubElement(grad, "stop", {"offset": "0.45", "stop-color": "#3b82b5"})
    SubElement(grad, "stop", {"offset": "0.7", "stop-color": "#c85b73"})
    SubElement(grad, "stop", {"offset": "1", "stop-color": "#fff0f3"})


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


def grid(parent, x, y, cols, rows, cell, stroke="#9fb3c2", width=1.5):
    for j in range(cols + 1):
        line(parent, x + j * cell, y, x + j * cell, y + rows * cell, stroke=stroke, width=width)
    for j in range(rows + 1):
        line(parent, x, y + j * cell, x + cols * cell, y + j * cell, stroke=stroke, width=width)


def pixel_aperture_sampling():
    width, height = 1500, 700
    svg = base_svg(width, height, "连续像经像素孔径积分后在晶格上采样")
    text(svg, width / 2, 43, "像素不是几何点：先在有限面积上积分，再按间距 p 排列", size=31, weight="700", fill="#102a43")
    # Continuous irradiance.
    rounded_box(svg, 35, 110, 365, 420, "#f4f9fd", "#9bc7ee", "连续像面辐照度 e(x,y)", None, "#285b7a")
    for row in range(10):
        for col in range(10):
            cx, cy = 75 + col * 30, 180 + row * 28
            u = math.exp(-((col - 3.0) ** 2 + (row - 5.0) ** 2) / 12)
            v = math.exp(-((col - 7.0) ** 2 + (row - 3.0) ** 2) / 8)
            red = int(225 - 80 * v)
            blue = int(236 - 95 * u)
            green = int(241 - 50 * (u + v) / 2)
            SubElement(svg, "rect", {
                "x": str(cx), "y": str(cy), "width": "31", "height": "29",
                "fill": f"#{red:02x}{green:02x}{blue:02x}", "stroke": "none",
            })
    pts = []
    for j in range(120):
        u = j / 119
        x = 66 + 300 * u
        y = 455 - 120 * (0.25 + 0.55 * math.exp(-((u - 0.32) / 0.16) ** 2) + 0.35 * math.exp(-((u - 0.75) / 0.11) ** 2))
        pts.append((x, y))
    polyline(svg, pts, stroke="#3b82b5", width=4)
    text(svg, 218, 505, "空间连续，可含任意相位", size=17, fill="#486581")
    line(svg, 405, 320, 475, 320, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Pixel aperture.
    rounded_box(svg, 480, 110, 430, 420, "#fffaf1", "#e8c77d", "像素孔径 a(x,y)", None, "#8a5f19")
    x0, y0, pitch, aperture = 535, 180, 80, 56
    for row in range(4):
        for col in range(4):
            cx, cy = x0 + col * pitch, y0 + row * pitch
            SubElement(svg, "rect", {
                "x": str(cx + (pitch - aperture) / 2), "y": str(cy + (pitch - aperture) / 2),
                "width": str(aperture), "height": str(aperture), "rx": "7",
                "fill": "#f8d895", "stroke": "#c58a2d", "stroke-width": "2",
            })
            SubElement(svg, "circle", {"cx": str(cx + pitch / 2), "cy": str(cy + pitch / 2), "r": "4", "fill": "#8a5f19"})
    line(svg, x0, 525, x0 + pitch, 525, stroke="#c85b73", width=3)
    line(svg, x0, 514, x0, 536, stroke="#c85b73", width=2)
    line(svg, x0 + pitch, 514, x0 + pitch, 536, stroke="#c85b73", width=2)
    text(svg, x0 + pitch / 2, 562, "间距 p", size=17, weight="700", fill="#a24862")
    line(svg, x0 + (pitch - aperture) / 2, 485, x0 + (pitch + aperture) / 2, 485, stroke="#4d8c6a", width=3)
    text(svg, x0 + pitch / 2, 475, "孔径宽 a", size=16, weight="700", fill="#397456")
    text(svg, 695, 605, "面积积分 = 与孔径卷积；p 与 a 是不同参数", size=18, fill="#7b4b74")
    line(svg, 915, 320, 985, 320, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Discrete output.
    rounded_box(svg, 990, 110, 475, 420, "#f4f9fd", "#9bc7ee", "离散数组 z[m,n]", None, "#285b7a")
    gx, gy, cell = 1045, 175, 54
    values = [
        [0.12, 0.18, 0.30, 0.41, 0.35, 0.22],
        [0.18, 0.35, 0.58, 0.74, 0.51, 0.27],
        [0.25, 0.55, 0.87, 0.91, 0.63, 0.31],
        [0.22, 0.49, 0.79, 0.68, 0.46, 0.25],
        [0.15, 0.31, 0.43, 0.38, 0.28, 0.18],
        [0.10, 0.17, 0.22, 0.20, 0.16, 0.12],
    ]
    for row in range(6):
        for col in range(6):
            v = values[row][col]
            shade = int(248 - 130 * v)
            SubElement(svg, "rect", {
                "x": str(gx + col * cell), "y": str(gy + row * cell),
                "width": str(cell), "height": str(cell),
                "fill": f"#{shade:02x}{min(255, shade + 14):02x}{min(255, shade + 28):02x}",
                "stroke": "#8aa2b5", "stroke-width": "1.5",
            })
    text(svg, 1227, 535, "每格只保留一个积分值", size=17, fill="#486581")
    text(svg, width / 2, 662, "z[m,n] = ∬ e(x,y)a(x−mp,y−np) dxdy；点采样只是 a→δ 的理想极限", size=21, weight="700", fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "pixel_aperture_sampling.svg", encoding="utf-8", xml_declaration=True)


def sampling_spectrum_aliasing():
    width, height = 1500, 740
    svg = base_svg(width, height, "采样导致频谱周期复制并在欠采样时重叠")
    text(svg, width / 2, 43, "晶格采样在频域复制连续频谱；副本重叠就是混叠", size=31, weight="700", fill="#102a43")
    panels = [(45, "充分采样：B < fs/2", "#4d8c6a"), (770, "欠采样：B > fs/2", "#c85b73")]
    for x0, title_value, color in panels:
        text(svg, x0 + 330, 100, title_value, size=24, weight="700", fill=color)
        l, r, base, top = x0 + 35, x0 + 665, 315, 145
        line(svg, l, base, r, base, stroke="#334e68", width=2, marker="arrow-dark")
        for k in range(-2, 3):
            cx = (l + r) / 2 + k * 145
            line(svg, cx, base - 6, cx, base + 8, stroke="#334e68", width=2)
            label = "0" if k == 0 else ("fs" if k == 1 else ("−fs" if k == -1 else f"{k}fs"))
            text(svg, cx, base + 32, label, size=14, fill="#627d98")
            half = 50 if x0 < 100 else 93
            pts = [(cx - half, base)]
            for j in range(41):
                u = -1 + 2 * j / 40
                pts.append((cx + half * u, base - (top + 65 - top) * (math.cos(math.pi * u / 2) ** 2)))
            pts.append((cx + half, base))
            polygon(svg, pts, fill=color + "33", stroke=color, width=2.5)
        text(svg, (l + r) / 2, 375, "频谱副本间隔 fs = 1/p", size=17, fill="#486581")
        if x0 > 100:
            SubElement(svg, "rect", {"x": str((l + r) / 2 + 52), "y": "185", "width": "41", "height": "130", "fill": "#c85b73", "fill-opacity": "0.18"})
            text(svg, (l + r) / 2 + 73, 167, "重叠", size=16, weight="700", fill="#a24862")
    line(svg, 750, 80, 750, 690, stroke="#d7e0e7", width=2)
    # 2D reciprocal lattice below.
    text(svg, 375, 445, "二维方形晶格的奈奎斯特区域", size=22, weight="700", fill="#285b7a")
    cx, cy, s = 375, 570, 178
    SubElement(svg, "rect", {"x": str(cx - s / 2), "y": str(cy - s / 2), "width": str(s), "height": str(s), "fill": "#eaf4ff", "stroke": "#3b82b5", "stroke-width": "3"})
    line(svg, cx - 160, cy, cx + 160, cy, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, cx, cy + 145, cx, cy - 155, stroke="#334e68", width=2, marker="arrow-dark")
    text(svg, cx + s / 2, cy + 27, "fs/2", size=14, fill="#285b7a")
    text(svg, cx - s / 2, cy + 27, "−fs/2", size=14, fill="#285b7a")
    text(svg, cx + 12, cy - s / 2 - 10, "fs/2", size=14, fill="#285b7a", anchor="start")
    SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": "66", "fill": "#4d8c6a", "fill-opacity": "0.18", "stroke": "#4d8c6a", "stroke-width": "2"})
    text(svg, cx, 688, "无混叠支持集须落在基本频率胞元内", size=16, fill="#486581")
    # Aliased sinusoids below right.
    text(svg, 1125, 445, "相差整数 fs 的正弦给出同一组样本", size=22, weight="700", fill="#a24862")
    l, r, mid = 825, 1420, 575
    line(svg, l, mid, r, mid, stroke="#9fb3c2", width=1.5)
    for freq, color, phase in ((0.18, "#3b82b5", 0), (0.82, "#c85b73", 0)):
        pts = []
        for j in range(401):
            u = j / 400
            pts.append((l + (r - l) * u, mid - 75 * math.sin(2 * math.pi * freq * 10 * u + phase)))
        polyline(svg, pts, stroke=color, width=3, dash="8 5" if freq > 0.5 else None)
    for k in range(11):
        x = l + (r - l) * k / 10
        y = mid - 75 * math.sin(2 * math.pi * 0.18 * k)
        line(svg, x, mid, x, y, stroke="#8aa2b5", width=1)
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "6", "fill": "#102a43"})
    text(svg, 980, 680, "低频 ν", size=16, weight="700", fill="#285b7a")
    text(svg, 1270, 680, "高频 fs−ν", size=16, weight="700", fill="#a24862")
    ElementTree(svg).write(SVG_DIR / "sampling_spectrum_aliasing.svg", encoding="utf-8", xml_declaration=True)


def pixel_aperture_mtf():
    width, height = 1500, 690
    svg = base_svg(width, height, "不同像素孔径和方向的sinc调制传递函数")
    text(svg, width / 2, 43, "像素面积积分是采样前低通：孔径越大，抗混叠越强但高频衰减越早", size=31, weight="700", fill="#102a43")
    l, r, t, b = 120, 1380, 120, 545
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    for q in (0, 0.25, 0.5, 0.75, 1.0):
        y = b - (b - t) * q
        line(svg, l, y, r, y, stroke="#e0e7ec", width=1.2)
        text(svg, l - 18, y + 5, f"{q:.2f}", size=15, fill="#627d98", anchor="end")
    for q in (0, 0.25, 0.5, 0.75, 1.0):
        x = l + (r - l) * q
        line(svg, x, t, x, b, stroke="#e0e7ec", width=1.2)
        text(svg, x, b + 32, f"{q:.2f}", size=15, fill="#627d98")
    def sinc(x):
        return 1.0 if abs(x) < 1e-10 else math.sin(math.pi * x) / (math.pi * x)
    curves = [
        (0.5, False, "a/p=0.5，轴向", "#c58a2d", None),
        (0.75, False, "a/p=0.75，轴向", "#4d8c6a", None),
        (1.0, False, "a/p=1，轴向", "#3b82b5", None),
        (1.0, True, "a/p=1，对角", "#7b4b74", "10 6"),
    ]
    for ratio, diagonal, label, color, dash in curves:
        pts = []
        for j in range(321):
            nu = j / 320
            value = abs(sinc(ratio * nu))
            if diagonal:
                value = value * value
            pts.append((l + (r - l) * nu, b - (b - t) * value))
        polyline(svg, pts, stroke=color, width=4, dash=dash)
    ny = l + (r - l) * 0.5
    line(svg, ny, t, ny, b, stroke="#c85b73", width=2.5, dash="9 6")
    text(svg, ny, t - 15, "奈奎斯特 0.5 cycle/pixel", size=17, weight="700", fill="#a24862")
    # Mark exact values for full aperture.
    axis_val = 2 / math.pi
    diag_val = axis_val ** 2
    for value, color, label, dx in ((axis_val, "#3b82b5", "2/π≈0.637", 130), (diag_val, "#7b4b74", "(2/π)²≈0.405", 185)):
        y = b - (b - t) * value
        SubElement(svg, "circle", {"cx": str(ny), "cy": str(y), "r": "6", "fill": color})
        line(svg, ny + 8, y, ny + dx - 8, y, stroke=color, width=1.5, dash="5 4")
        text(svg, ny + dx, y + 6, label, size=16, weight="700", fill=color, anchor="start")
    # Legend.
    legend = [(925, 175, "a/p=0.5", "#c58a2d", None), (1085, 175, "a/p=0.75", "#4d8c6a", None), (1255, 175, "a/p=1 轴向", "#3b82b5", None), (1255, 215, "a/p=1 对角", "#7b4b74", "8 5")]
    for x, y, label, color, dash in legend:
        line(svg, x - 60, y - 6, x - 12, y - 6, stroke=color, width=4, dash=dash)
        text(svg, x, y, label, size=15, weight="700", fill=color, anchor="start")
    text(svg, r, b + 68, "归一化空间频率 νp / cycle·pixel⁻¹", size=18, fill="#627d98", anchor="end")
    text(svg, l - 5, t - 18, "|Hpixel|", size=17, fill="#627d98", anchor="start")
    text(svg, width / 2, 640, "矩形孔径 Hpixel(νx,νy)=sinc(aνx)sinc(aνy)；二维对角响应是两个方向因子的乘积", size=20, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "pixel_aperture_mtf.svg", encoding="utf-8", xml_declaration=True)


def sampling_phase_moire():
    width, height = 1500, 720
    svg = base_svg(width, height, "采样相位不确定性与摩尔纹拍频")
    text(svg, width / 2, 43, "接近奈奎斯特边界时，相位决定样本对比；相近栅格产生低频摩尔纹", size=31, weight="700", fill="#102a43")
    line(svg, 750, 82, 750, 660, stroke="#d7e0e7", width=2)
    # Phase ambiguity.
    text(svg, 375, 100, "同一高频，不同采样相位", size=24, weight="700", fill="#285b7a")
    for row, phase in enumerate((0, math.pi / 2)):
        l, r = 85, 680
        mid = 225 + row * 220
        line(svg, l, mid, r, mid, stroke="#9fb3c2", width=1.5)
        pts = []
        for j in range(401):
            u = j / 400
            y = mid - 70 * math.sin(2 * math.pi * 0.5 * 10 * u + phase)
            pts.append((l + (r - l) * u, y))
        polyline(svg, pts, stroke="#3b82b5", width=3)
        for k in range(11):
            x = l + (r - l) * k / 10
            y = mid - 70 * math.sin(math.pi * k + phase)
            SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "7", "fill": "#c85b73"})
        label = "相位 0：样本恰落零点，观测对比为 0" if row == 0 else "相位 π/2：样本在 ±峰值，观测对比最大"
        text(svg, 375, mid + 108, label, size=17, weight="700", fill="#7b4b74")
    # Moire pattern: two line gratings and product/beat.
    text(svg, 1125, 100, "两组近频栅格的拍频", size=24, weight="700", fill="#a24862")
    x0, y0, w, h = 825, 155, 600, 360
    SubElement(svg, "rect", {"x": str(x0), "y": str(y0), "width": str(w), "height": str(h), "fill": "#f7f9fb", "stroke": "#9fb3c2", "stroke-width": "2"})
    clip_defs = SubElement(svg, "defs")
    clip = SubElement(clip_defs, "clipPath", {"id": "moire-clip"})
    SubElement(clip, "rect", {"x": str(x0), "y": str(y0), "width": str(w), "height": str(h)})
    grating_group = SubElement(svg, "g", {"clip-path": "url(#moire-clip)"})
    # Draw two slightly rotated families with opacity.
    for j in range(-18, 30):
        xa = x0 + j * 26
        line(grating_group, xa, y0, xa + 130, y0 + h, stroke="#334e68", width=5)
    for j in range(-18, 30):
        xa = x0 + j * 27 + 70
        line(grating_group, xa, y0, xa - 105, y0 + h, stroke="#3b82b5", width=4)
    text(svg, 1125, 555, "场景频率 ν1 与采样/第二栅格 ν2", size=18, fill="#486581")
    text(svg, 1125, 598, "产生低频包络 |ν1−ν2|", size=22, weight="700", fill="#a24862")
    rounded_box(svg, 865, 625, 520, 62, "#fff0f3", "#eab0be", "微小位移即可让摩尔纹相位和颜色显著改变", None, "#a24862")
    ElementTree(svg).write(SVG_DIR / "sampling_phase_moire.svg", encoding="utf-8", xml_declaration=True)


def resolution_chain():
    width, height = 1500, 720
    svg = base_svg(width, height, "光学像素采样处理与输出共同决定有效分辨率")
    text(svg, width / 2, 43, "有效分辨率是一条传递链，不等于传感器像素总数", size=31, weight="700", fill="#102a43")
    blocks = [
        (35, "光学", "衍射 · 像差 · 对焦", "#eaf4ff", "#9bc7ee"),
        (330, "运动", "曝光积分 · 抖动", "#fff0f3", "#eab0be"),
        (625, "像素孔径", "面积预滤波", "#fff7e8", "#e8c77d"),
        (920, "晶格与 CFA", "采样 · 混叠", "#edf8f2", "#9fd6b7"),
        (1215, "重建与输出", "去马赛克 · 缩放", "#f7efff", "#c9a9e8"),
    ]
    for x, title_value, subtitle, fill, stroke in blocks:
        rounded_box(svg, x, 115, 250, 125, fill, stroke, title_value, subtitle)
    for x in (285, 580, 875, 1170):
        line(svg, x, 177, x + 38, 177, stroke="#527da3", width=3, marker="arrow-blue")
    text(svg, 750, 278, "连续环节的 OTF 近似相乘；采样后出现频谱复制，不能再用单一低通曲线概括", size=19, fill="#7b4b74")
    # Diminishing pixel return curves.
    l, r, t, b = 110, 760, 360, 625
    text(svg, 435, 335, "提高像素数的边际收益", size=22, weight="700", fill="#285b7a")
    line(svg, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    curves = [(1.0, "高带宽光学", "#4d8c6a"), (0.72, "中等光学", "#3b82b5"), (0.45, "低带宽/运动", "#c85b73")]
    for ceiling, label, color in curves:
        pts = []
        for j in range(201):
            u = j / 200
            value = ceiling * (1 - math.exp(-3 * u / ceiling))
            pts.append((l + (r - l) * u, b - (b - t) * value))
        polyline(svg, pts, stroke=color, width=4)
    text(svg, r, b + 38, "线性像素密度", size=16, fill="#627d98", anchor="end")
    text(svg, l - 4, t - 14, "有效细节", size=16, fill="#627d98", anchor="start")
    text(svg, 635, 385, "高带宽光学", size=15, weight="700", fill="#397456")
    text(svg, 600, 455, "中等光学", size=15, weight="700", fill="#285b7a")
    text(svg, 500, 530, "低带宽/运动", size=15, weight="700", fill="#a24862")
    # Metric conversion panel.
    rounded_box(svg, 825, 330, 600, 315, "#f4f9fd", "#9bc7ee", "三个尺度必须分开报告", None, "#285b7a")
    metrics = [
        (390, "传感器尺度", "νN = 1/(2p)  cycle/mm"),
        (470, "画面尺度", "LW/PH = 2ν · 画面高度"),
        (550, "输出尺度", "受缩放像素、打印与观看共同限制"),
    ]
    for y, title_value, formula in metrics:
        SubElement(svg, "circle", {"cx": "885", "cy": str(y - 6), "r": "10", "fill": "#3b82b5"})
        text(svg, 915, y, title_value, size=18, weight="700", fill="#102a43", anchor="start")
        text(svg, 1060, y + 33, formula, size=17, fill="#486581", anchor="start")
    text(svg, width / 2, 690, "“2400 万像素”描述数组大小；它不自动证明 2400 万个独立、无混叠且高 SNR 的场景自由度", size=20, weight="700", fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "resolution_chain.svg", encoding="utf-8", xml_declaration=True)


def cfa_demosaic_model():
    width, height = 1500, 740
    svg = base_svg(width, height, "彩色滤波阵列将三通道场欠采样为单通道马赛克并通过先验重建")
    text(svg, width / 2, 43, "CFA 每个位置只给出一个光谱加权值；去马赛克是欠定逆问题", size=31, weight="700", fill="#102a43")
    # Full color unknowns.
    rounded_box(svg, 35, 105, 285, 475, "#f7f9fb", "#9fb3c2", "未知三通道场", "每个位置有 R、G、B 三个未知量")
    cols = ["#d76a7d", "#58a879", "#4d89bd"]
    for row in range(5):
        for col in range(5):
            x, y = 70 + col * 47, 225 + row * 55
            for k, color in enumerate(cols):
                SubElement(svg, "circle", {"cx": str(x + k * 10), "cy": str(y), "r": "7", "fill": color, "fill-opacity": str(0.45 + 0.1 * ((row + col + k) % 3))})
    text(svg, 177, 545, "3MN 个未知量", size=18, weight="700", fill="#7b4b74")
    line(svg, 325, 335, 385, 335, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Bayer mosaic.
    rounded_box(svg, 390, 105, 320, 475, "#f4f9fd", "#9bc7ee", "2×2 Bayer 周期掩模", "G 占 1/2；R、B 各占 1/4", "#285b7a")
    gx, gy, cell = 435, 215, 54
    cfa = [["R", "G"], ["G", "B"]]
    fills = {"R": "#d76a7d", "G": "#58a879", "B": "#4d89bd"}
    for row in range(6):
        for col in range(4):
            ch = cfa[row % 2][col % 2]
            SubElement(svg, "rect", {"x": str(gx + col * cell), "y": str(gy + row * cell), "width": str(cell), "height": str(cell), "fill": fills[ch], "fill-opacity": "0.78", "stroke": "#ffffff", "stroke-width": "2"})
            text(svg, gx + (col + 0.5) * cell, gy + (row + 0.63) * cell, ch, size=18, weight="700", fill="#ffffff")
    text(svg, 550, 560, "只有 MN 个观测值", size=18, weight="700", fill="#7b4b74")
    line(svg, 715, 335, 775, 335, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Priors.
    rounded_box(svg, 780, 105, 300, 475, "#fff7e8", "#e8c77d", "重建先验", "决定无观测位置如何补值", "#8a5f19")
    prior_items = [(230, "局部平滑", "低频色度"), (310, "边缘同向", "避免跨边缘插值"), (390, "通道相关", "亮度/色差分解"), (470, "数据先验", "学习型统计规律")]
    for y, title_value, subtitle in prior_items:
        SubElement(svg, "circle", {"cx": "835", "cy": str(y - 5), "r": "10", "fill": "#c58a2d"})
        text(svg, 860, y, title_value, size=18, weight="700", fill="#8a5f19", anchor="start")
        text(svg, 860, y + 28, subtitle, size=15, fill="#627d98", anchor="start")
    line(svg, 1085, 335, 1145, 335, stroke="#3b82b5", width=4, marker="arrow-blue")
    # Reconstructed output and artifacts.
    rounded_box(svg, 1150, 105, 315, 475, "#f7efff", "#c9a9e8", "全彩图像估计", "结果依赖算法，不是直接测量", "#7b4b74")
    ox, oy, cell2 = 1195, 225, 44
    for row in range(6):
        for col in range(5):
            red = 120 + int(100 * col / 4)
            green = 170 - int(45 * row / 5)
            blue = 210 - int(80 * col / 4)
            if row in (2, 3) and col in (2, 3):
                red, green, blue = 210, 85, 145
            SubElement(svg, "rect", {"x": str(ox + col * cell2), "y": str(oy + row * cell2), "width": str(cell2), "height": str(cell2), "fill": f"#{red:02x}{green:02x}{blue:02x}", "stroke": "#ffffff", "stroke-width": "1"})
    text(svg, 1307, 530, "可能出现假色、拉链、迷宫纹", size=16, weight="700", fill="#a24862")
    # Equation strip.
    rounded_box(svg, 115, 625, 1270, 78, "#edf8f2", "#9fd6b7", "y[m,n] = MR[m,n]R[m,n] + MG[m,n]G[m,n] + MB[m,n]B[m,n] + ε", None, "#397456")
    text(svg, 750, 727, "一条标量方程不能逐像素唯一确定三个通道；阵列设计只是在频谱布局、光子效率与重建难度之间换取不同折衷", size=18, fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "cfa_demosaic_model.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    pixel_aperture_sampling()
    sampling_spectrum_aliasing()
    pixel_aperture_mtf()
    sampling_phase_moire()
    resolution_chain()
    cfa_demosaic_model()


if __name__ == "__main__":
    main()
