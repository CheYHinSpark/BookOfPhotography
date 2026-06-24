from pathlib import Path
from xml.etree.ElementTree import SubElement, ElementTree
import math

from draw_raw_pipeline import base_svg, text, line, polyline, rounded_box, axes


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"


def path_curve(parent, points, stroke, width=4, fill="none", dash=None):
    attrs = {
        "points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points),
        "fill": fill, "stroke": stroke, "stroke-width": str(width),
        "stroke-linecap": "round", "stroke-linejoin": "round",
    }
    if dash:
        attrs["stroke-dasharray"] = dash
    return SubElement(parent, "polyline", attrs)


def gaussian(x, sigma):
    return math.exp(-0.5 * (x / sigma) ** 2)


def convolution_psf():
    width, height = 1500, 720
    svg = base_svg(width, height, "点扩散函数与卷积成像")
    text(svg, 750, 43, "线性移不变成像：每个物点复制同一个 PSF，整幅图像由平移副本叠加",
         size=30, weight="700", fill="#102a43")
    # Object points.
    rounded_box(svg, 45, 115, 360, 435, "#eaf4ff", "#9bc7ee", "物体 f(x)", "若干加权点源")
    obj = [(125, 425, 9), (190, 270, 16), (260, 370, 12), (330, 220, 20)]
    for x, y, r in obj:
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": str(r), "fill": "#3b82b5"})
        line(svg, x, y + r + 5, x, 510, stroke="#a8c8e0", width=2, dash="5 6")
    # PSF panel.
    rounded_box(svg, 570, 115, 360, 435, "#edf8f2", "#9fd6b7", "系统 h(x)", "单个点的像")
    cx, cy = 750, 340
    for rr, op in ((95, .05), (68, .10), (43, .20), (22, .45), (8, .85)):
        SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": str(rr),
                                    "fill": "#4d8c6a", "fill-opacity": str(op)})
    text(svg, cx, 495, "∫h(x)dx = 1", size=20, weight="700", fill="#397456")
    # Image panel.
    rounded_box(svg, 1095, 115, 360, 435, "#fff0f3", "#eab0be", "图像 g=f*h+n", "平移 PSF 的加权和")
    for x, y, r in obj:
        xx = 1050 + x
        for rr, op in ((r * 3.0, .07), (r * 2.0, .14), (r * 1.1, .32)):
            SubElement(svg, "circle", {"cx": str(xx), "cy": str(y), "r": str(rr),
                                        "fill": "#c85b73", "fill-opacity": str(op)})
    line(svg, 405, 330, 560, 330, stroke="#527da3", width=4, marker="arrow-blue")
    text(svg, 482, 305, "作用 h", size=17, weight="700", fill="#285b7a")
    line(svg, 930, 330, 1085, 330, stroke="#527da3", width=4, marker="arrow-blue")
    text(svg, 1007, 305, "叠加", size=17, weight="700", fill="#285b7a")
    rounded_box(svg, 230, 615, 1040, 65, "#fff7e8", "#e8c77d",
                "若 PSF 随位置、亮度或时间改变，单个卷积核不再足以描述整幅图像",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "convolution_psf.svg", encoding="utf-8", xml_declaration=True)


def spatial_frequency_duality():
    width, height = 1500, 720
    svg = base_svg(width, height, "空域卷积与频域乘法")
    text(svg, 750, 43, "同一线性系统的两种坐标：空域看邻域叠加，频域看各频率的复增益",
         size=30, weight="700", fill="#102a43")
    # top spatial branch
    rounded_box(svg, 80, 135, 260, 110, "#eaf4ff", "#9bc7ee", "物体 f(x)", "空间结构")
    rounded_box(svg, 480, 135, 260, 110, "#edf8f2", "#9fd6b7", "卷积 h(x)", "PSF")
    rounded_box(svg, 880, 135, 260, 110, "#fff0f3", "#eab0be", "图像 g(x)", "模糊 + 噪声")
    for x1, x2 in ((340, 470), (740, 870)):
        line(svg, x1, 190, x2, 190, stroke="#527da3", width=4, marker="arrow-blue")
    text(svg, 410, 166, "*", size=28, weight="700", fill="#7b4b74")
    # Fourier arrows
    for x in (210, 610, 1010):
        line(svg, x, 260, x, 390, stroke="#7b4b74", width=3, marker="arrow-purple")
        text(svg, x + 18, 335, "ℱ", size=23, weight="700", fill="#7b4b74", anchor="start")
    # bottom frequency branch
    rounded_box(svg, 80, 420, 260, 110, "#eaf4ff", "#9bc7ee", "F(ν)", "物体频谱")
    rounded_box(svg, 480, 420, 260, 110, "#edf8f2", "#9fd6b7", "H(ν)", "OTF：复数")
    rounded_box(svg, 880, 420, 260, 110, "#fff0f3", "#eab0be", "G(ν)=HF+N", "逐频率乘法")
    for x1, x2 in ((340, 470), (740, 870)):
        line(svg, x1, 475, x2, 475, stroke="#527da3", width=4, marker="arrow-blue")
    text(svg, 410, 451, "×", size=28, weight="700", fill="#7b4b74")
    rounded_box(svg, 1215, 145, 235, 385, "#fff7e8", "#e8c77d", "必须保留相位",
                "MTF=|H| 只给幅度", "#8a5f19")
    text(svg, 1332, 330, "H=|H|e^{iφ}", size=23, weight="700", fill="#8a5f19")
    text(svg, 1332, 390, "零点：信息模态消失", size=16, fill="#486581")
    text(svg, 1332, 430, "相位：结构位置改变", size=16, fill="#486581")
    rounded_box(svg, 250, 620, 1000, 62, "#eef5fb", "#a8c8e0",
                "离散 DFT 默认循环卷积；线性卷积需要正确填充与边界模型",
                None, "#285b7a", 18)
    ElementTree(svg).write(SVG_DIR / "spatial_frequency_duality.svg", encoding="utf-8", xml_declaration=True)


def lsi_failure_modes():
    width, height = 1500, 740
    svg = base_svg(width, height, "线性移不变卷积模型的成立条件与失效方式")
    text(svg, 750, 43, "卷积模型是一种局部近似：线性、移不变、单一曝光与已知边界缺一不可",
         size=30, weight="700", fill="#102a43")
    cards = [
        (55, 120, "空间变化 PSF", "像差、场曲、数字畸变校正", "h(x,ξ) 依赖像点位置", "#eaf4ff", "#9bc7ee"),
        (520, 120, "亮度非线性", "饱和、色调曲线、局部 HDR", "h*(af) ≠ a(h*f)", "#fff0f3", "#eab0be"),
        (985, 120, "时间变化", "滚动快门、抖动路径、主体运动", "每行/每物体具有不同核", "#f7efff", "#c9a9e8"),
        (55, 385, "边界未知", "零填充、镜像、周期延拓", "图外内容影响卷积结果", "#fff7e8", "#e8c77d"),
        (520, 385, "采样与混叠", "先模糊再采样并非可逆", "高频折叠后不再独立", "#edf8f2", "#9fd6b7"),
        (985, 385, "空间耦合处理", "去马赛克、降噪、锐化", "有效核依赖内容和通道", "#eef5fb", "#a8c8e0"),
    ]
    for x, y, title_value, subtitle, detail, fill, stroke in cards:
        rounded_box(svg, x, y, 410, 205, fill, stroke, title_value, subtitle)
        text(svg, x + 205, y + 135, detail, size=17, weight="700", fill="#486581")
        line(svg, x + 70, y + 165, x + 340, y + 165, stroke=stroke, width=3)
    rounded_box(svg, 260, 650, 980, 62, "#ffffff", "#b9c7d3",
                "实际复原常把图像分块、估计局部 PSF 或直接使用一般线性算子 H，而不是强行假设全局卷积",
                None, "#334e68", 18)
    ElementTree(svg).write(SVG_DIR / "lsi_failure_modes.svg", encoding="utf-8", xml_declaration=True)


def unsharp_frequency_response():
    width, height = 1500, 740
    svg = base_svg(width, height, "反遮罩锐化的空域结构和频率响应")
    text(svg, 750, 43, "反遮罩锐化：从原图减去低通得到高频掩模，再按增益加回",
         size=30, weight="700", fill="#102a43")
    blocks = [(45, "输入 f", "#eaf4ff", "#9bc7ee"), (345, "低通 Gσ*f", "#edf8f2", "#9fd6b7"),
              (645, "掩模 f−Gσ*f", "#fff7e8", "#e8c77d"), (1005, "输出 f+αm", "#fff0f3", "#eab0be")]
    for x, title_value, fill, stroke in blocks:
        rounded_box(svg, x, 105, 240, 105, fill, stroke, title_value, None, title_size=18)
    line(svg, 285, 157, 335, 157, stroke="#527da3", width=3, marker="arrow-blue")
    line(svg, 585, 157, 635, 157, stroke="#527da3", width=3, marker="arrow-blue")
    line(svg, 885, 157, 995, 157, stroke="#527da3", width=3, marker="arrow-blue")
    line(svg, 165, 220, 165, 275, stroke="#527da3", width=3)
    line(svg, 165, 275, 1125, 275, stroke="#527da3", width=3)
    line(svg, 1125, 275, 1125, 220, stroke="#527da3", width=3, marker="arrow-blue")
    text(svg, 935, 250, "原图直通", size=16, fill="#627d98")
    # Frequency response graph.
    l, r, t, b = 160, 1340, 350, 635
    axes(svg, l, r, t, b, "归一化空间频率 ν", "增益 K(ν)")
    line(svg, l, b - 80, r, b - 80, stroke="#9aa9b5", width=2, dash="8 8")
    text(svg, l - 10, b - 73, "1", size=15, fill="#627d98", anchor="end")
    colors = [(0.5, "#4d8c6a"), (1.0, "#3b82b5"), (2.0, "#c85b73")]
    for alpha, color in colors:
        pts = []
        for j in range(201):
            nu = j / 200
            blur = math.exp(-3.6 * nu * nu)
            gain = 1 + alpha * (1 - blur)
            x = l + nu * (r - l)
            y = b - 80 * gain
            pts.append((x, y))
        path_curve(svg, pts, color, 4)
        text(svg, r - 10, pts[-1][1] - 8, f"α={alpha:g}", size=16, weight="700", fill=color, anchor="end")
    text(svg, 750, 690, "K(0)=1：平均亮度不变；高频平台趋近 1+α，但噪声也按同一增益放大",
         size=18, weight="700", fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "unsharp_frequency_response.svg", encoding="utf-8", xml_declaration=True)


def derivative_noise_amplification():
    width, height = 1500, 720
    svg = base_svg(width, height, "微分锐化对信号与噪声的频率加权")
    text(svg, 750, 43, "微分强调快速变化；白噪声恰好在高频仍有功率，因此二者不可分开增益",
         size=30, weight="700", fill="#102a43")
    panels = [(70, 700, "一阶差分 |D(ν)|", 1), (800, 1430, "拉普拉斯 |L(ν)|", 2)]
    for l0, r0, title_value, power in panels:
        text(svg, (l0+r0)/2, 105, title_value, size=22, weight="700", fill="#285b7a")
        l, r, t, b = l0 + 50, r0 - 25, 150, 530
        axes(svg, l, r, t, b, "ν / νN", "幅度")
        pts = []
        noise_pts = []
        for j in range(201):
            nu = j / 200
            amp = (2 * math.sin(math.pi * nu / 2)) ** power
            x = l + nu * (r-l)
            y = b - amp / (4 if power == 2 else 2) * (b-t-35)
            pts.append((x, y))
            noise_y = b - (amp ** 2) / (16 if power == 2 else 4) * (b-t-35)
            noise_pts.append((x, noise_y))
        path_curve(svg, pts, "#3b82b5", 5)
        path_curve(svg, noise_pts, "#c85b73", 3, dash="9 7")
        text(svg, r-10, t+45, "算子幅度", size=16, weight="700", fill="#3b82b5", anchor="end")
        text(svg, r-10, t+78, "白噪声输出功率 ∝ |K|²", size=16, weight="700", fill="#c85b73", anchor="end")
    rounded_box(svg, 250, 600, 1000, 70, "#fff7e8", "#e8c77d",
                "边缘与噪声共享高频带；阈值、正则化或多尺度先验只能作统计区分，不能作绝对分离",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "derivative_noise_amplification.svg", encoding="utf-8", xml_declaration=True)


def inverse_filter_instability():
    width, height = 1500, 740
    svg = base_svg(width, height, "逆滤波在传递函数零点附近放大噪声")
    text(svg, 750, 43, "逆滤波的不稳定性：当 |H| 很小时，除法同时放大测量噪声与模型误差",
         size=30, weight="700", fill="#102a43")
    panels = [(70, 700, "模糊传递 |H(ν)|"), (800, 1430, "逆增益 1/|H(ν)|")]
    for idx, (l0, r0, title_value) in enumerate(panels):
        text(svg, (l0+r0)/2, 105, title_value, size=22, weight="700", fill="#285b7a" if idx == 0 else "#a24862")
        l, r, t, b = l0+50, r0-25, 150, 540
        axes(svg, l, r, t, b, "ν", "幅度")
        pts = []
        for j in range(201):
            nu = j / 200
            h = abs(math.cos(math.pi * nu / 2.0)) * math.exp(-0.8 * nu * nu)
            if idx == 0:
                value = h
                y = b - value * (b-t-30)
            else:
                value = min(8, 1 / max(h, 0.02))
                y = b - value / 8 * (b-t-30)
            x = l + nu*(r-l)
            pts.append((x,y))
        path_curve(svg, pts, "#3b82b5" if idx == 0 else "#c85b73", 5)
        line(svg, r-35, b, r-35, t+15, stroke="#c58a2d", width=3, dash="8 7")
        text(svg, r-45, t+42, "近零点", size=16, weight="700", fill="#8a5f19", anchor="end")
    rounded_box(svg, 210, 610, 1080, 75, "#fff0f3", "#eab0be",
                "G=HF+N  ⇒  G/H = F+N/H；即使 N 很小，N/H 也可在弱响应频带占主导",
                None, "#a24862", 19)
    ElementTree(svg).write(SVG_DIR / "inverse_filter_instability.svg", encoding="utf-8", xml_declaration=True)


def regularized_filter_gains():
    width, height = 1500, 740
    svg = base_svg(width, height, "逆滤波维纳滤波和Tikhonov滤波的频率增益")
    text(svg, 750, 43, "正则化不是“少恢复一点”，而是按可观测性与先验给不同模态不同信任",
         size=30, weight="700", fill="#102a43")
    l, r, t, b = 120, 1380, 135, 565
    axes(svg, l, r, t, b, "归一化频率 ν", "复原增益 |W(ν)|")
    curves = {"逆滤波": [], "维纳": [], "Tikhonov": []}
    for j in range(301):
        nu = j / 300
        h = math.exp(-3.8 * nu * nu)
        inv = min(8, 1 / h)
        snr = 45 * math.exp(-4 * nu) + 0.15
        wiener = h / (h*h + 1/snr)
        reg = h / (h*h + 0.025 * (2*math.sin(math.pi*nu/2))**2)
        x = l + nu*(r-l)
        curves["逆滤波"].append((x, b - inv/8*(b-t-25)))
        curves["维纳"].append((x, b - wiener/8*(b-t-25)))
        curves["Tikhonov"].append((x, b - reg/8*(b-t-25)))
    styles = [("逆滤波", "#c85b73", None), ("维纳", "#3b82b5", None), ("Tikhonov", "#4d8c6a", "10 7")]
    for name, color, dash in styles:
        path_curve(svg, curves[name], color, 5 if not dash else 4, dash=dash)
    # legend
    lx = 220
    for name, color, dash in styles:
        line(svg, lx, 625, lx+70, 625, stroke=color, width=5, dash=dash)
        text(svg, lx+85, 632, name, size=18, weight="700", fill=color, anchor="start")
        lx += 310
    rounded_box(svg, 1040, 595, 330, 75, "#fff7e8", "#e8c77d", "λ 或 PSD 决定偏差—方差权衡",
                None, "#8a5f19", 16)
    ElementTree(svg).write(SVG_DIR / "regularized_filter_gains.svg", encoding="utf-8", xml_declaration=True)


def singular_modes_regularization():
    width, height = 1500, 760
    svg = base_svg(width, height, "成像算子的奇异模态与正则化")
    text(svg, 750, 43, "一般线性算子 H 的奇异值分解：弱奇异模态是复原不确定度的来源",
         size=30, weight="700", fill="#102a43")
    # Singular value bars.
    text(svg, 360, 105, "奇异值 σk", size=23, weight="700", fill="#285b7a")
    base_y = 570
    for k in range(12):
        val = math.exp(-0.35*k)
        x = 95 + k*48
        h = 380*val
        color = "#3b82b5" if val > .15 else "#c85b73"
        SubElement(svg, "rect", {"x": str(x), "y": str(base_y-h), "width": "34", "height": str(h),
                                  "rx": "5", "fill": color, "fill-opacity": "0.82"})
        text(svg, x+17, base_y+28, str(k+1), size=13, fill="#627d98")
    line(svg, 75, base_y, 690, base_y, stroke="#334e68", width=2)
    line(svg, 75, base_y-58, 690, base_y-58, stroke="#c58a2d", width=3, dash="8 7")
    text(svg, 680, base_y-68, "噪声/可信阈值", size=15, fill="#8a5f19", anchor="end")
    # mode flow
    rounded_box(svg, 770, 130, 630, 110, "#eaf4ff", "#9bc7ee", "观测系数 〈uₖ,g〉",
                "由左奇异向量投影")
    rounded_box(svg, 770, 300, 630, 110, "#fff0f3", "#eab0be", "朴素逆：除以 σₖ",
                "小 σₖ 导致噪声爆炸", "#a24862")
    rounded_box(svg, 770, 470, 630, 110, "#edf8f2", "#9fd6b7", "正则化：乘滤波因子 φₖ/σₖ",
                "弱模态被衰减或截断", "#397456")
    for y in (240, 410):
        line(svg, 1085, y, 1085, y+50, stroke="#527da3", width=4, marker="arrow-blue")
    rounded_box(svg, 265, 660, 970, 62, "#ffffff", "#b9c7d3",
                "σₖ=0 的空空间模态从观测中完全消失；任何输出都来自先验、约束或外部信息",
                None, "#334e68", 18)
    ElementTree(svg).write(SVG_DIR / "singular_modes_regularization.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    convolution_psf()
    spatial_frequency_duality()
    lsi_failure_modes()
    unsharp_frequency_response()
    derivative_noise_amplification()
    inverse_filter_instability()
    regularized_filter_gains()
    singular_modes_regularization()


if __name__ == "__main__":
    main()
