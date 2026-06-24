from pathlib import Path
from xml.etree.ElementTree import SubElement, ElementTree
import math
import random

from draw_raw_pipeline import base_svg, text, line, polyline, rounded_box, axes


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"


def signal_noise_overlap():
    width, height = 1500, 760
    svg = base_svg(width, height, "噪声与细节在局部变化中的重叠")
    text(svg, 750, 43, "观测只有一组像素值：快速变化既可能是结构，也可能是噪声",
         size=30, weight="700", fill="#102a43")

    panels = [
        (65, "平坦区域", "小幅起伏多半可平均", "flat"),
        (430, "真实边缘", "跨边平均会产生偏差", "edge"),
        (795, "细密纹理", "频率上可能像噪声", "texture"),
        (1160, "低信噪比", "单帧中出现多种解释", "ambiguous"),
    ]
    rng = random.Random(17)
    for x0, title_value, subtitle, mode in panels:
        rounded_box(svg, x0, 115, 275, 475, "#ffffff", "#b9c7d3", title_value, subtitle,
                    title_size=20)
        l, r, t, b = x0 + 28, x0 + 247, 255, 500
        line(svg, l, b, r, b, stroke="#c7d4df", width=2)
        clean = []
        observed = []
        for j in range(61):
            u = j / 60
            if mode == "flat":
                value = 0.52
                sigma = 0.055
            elif mode == "edge":
                value = 0.78 if u > 0.50 else 0.28
                sigma = 0.045
            elif mode == "texture":
                value = 0.52 + 0.16 * math.sin(2 * math.pi * 8 * u)
                sigma = 0.045
            else:
                value = 0.52 + 0.10 * math.sin(2 * math.pi * 4 * u)
                sigma = 0.16
            noisy = max(0.04, min(0.96, value + rng.gauss(0, sigma)))
            px = l + u * (r - l)
            clean.append((px, b - value * (b - t)))
            observed.append((px, b - noisy * (b - t)))
        polyline(svg, observed, stroke="#c85b73", width=3)
        polyline(svg, clean, stroke="#3b82b5", width=5)
        text(svg, x0 + 137, 548, "蓝：潜在信号　红：一次观测", size=14, fill="#627d98")

    rounded_box(svg, 210, 635, 1080, 72, "#fff7e8", "#e8c77d",
                "仅凭单帧局部高频，算法不能无条件知道哪些起伏应删除",
                "降噪必须引入平滑性、重复性、训练分布或多帧一致性等先验",
                "#8a5f19", 20)
    ElementTree(svg).write(SVG_DIR / "signal_noise_overlap.svg", encoding="utf-8",
                           xml_declaration=True)


def denoiser_weight_maps():
    width, height = 1500, 780
    svg = base_svg(width, height, "均值双边和非局部降噪的权重来源")
    text(svg, 750, 43, "三类方法的差别，不在于是否平均，而在于把权重给了谁",
         size=30, weight="700", fill="#102a43")

    configs = [
        (55, "局部均值 / 高斯", "只看空间距离", "local"),
        (520, "双边滤波", "空间近且像素值相近", "bilateral"),
        (985, "非局部平均", "整图寻找相似小块", "nonlocal"),
    ]
    rng = random.Random(23)
    for x0, title_value, subtitle, mode in configs:
        rounded_box(svg, x0, 105, 410, 515, "#ffffff", "#b9c7d3", title_value, subtitle,
                    title_size=21)
        gx, gy, cell = x0 + 74, 250, 38
        values = []
        for row in range(7):
            row_values = []
            for col in range(7):
                base = 0.28 if col < 4 else 0.74
                if mode == "nonlocal" and 1 <= row <= 2 and 1 <= col <= 2:
                    base = 0.74
                row_values.append(max(0.08, min(0.92, base + rng.gauss(0, .055))))
            values.append(row_values)
        for row in range(7):
            for col in range(7):
                v = values[row][col]
                c = int(246 - 135 * v)
                fill = f"rgb({c},{c + 10},{min(255, c + 22)})"
                SubElement(svg, "rect", {
                    "x": str(gx + col * cell), "y": str(gy + row * cell),
                    "width": str(cell - 2), "height": str(cell - 2),
                    "rx": "4", "fill": fill, "stroke": "#d7e2ea", "stroke-width": "1",
                })
        target_col, target_row = 3, 3
        tx = gx + target_col * cell + (cell - 2) / 2
        ty = gy + target_row * cell + (cell - 2) / 2
        SubElement(svg, "circle", {
            "cx": str(tx), "cy": str(ty), "r": "13", "fill": "none",
            "stroke": "#c85b73", "stroke-width": "4",
        })

        if mode == "local":
            SubElement(svg, "circle", {
                "cx": str(tx), "cy": str(ty), "r": "82", "fill": "#3b82b5",
                "fill-opacity": ".10", "stroke": "#3b82b5", "stroke-width": "3",
            })
            explanation = "邻域内都参与；边缘两侧会混合"
        elif mode == "bilateral":
            for row in range(7):
                for col in range(7):
                    if col >= 4 and abs(row - 3) <= 2:
                        SubElement(svg, "circle", {
                            "cx": str(gx + col * cell + 18),
                            "cy": str(gy + row * cell + 18), "r": "8",
                            "fill": "#4d8c6a", "fill-opacity": ".75",
                        })
            explanation = "拒绝跨强度边缘，但会误判弱纹理"
        else:
            matches = [(1, 1), (2, 1), (5, 4), (4, 5), (5, 5)]
            for col, row in matches:
                SubElement(svg, "rect", {
                    "x": str(gx + col * cell - 3), "y": str(gy + row * cell - 3),
                    "width": str(cell * 2 + 4), "height": str(cell * 2 + 4),
                    "rx": "7", "fill": "none", "stroke": "#7b4b74", "stroke-width": "3",
                })
            explanation = "重复结构提供更多样本；独特结构收益小"
        text(svg, x0 + 205, 565, explanation, size=15, fill="#486581")

    rounded_box(svg, 250, 665, 1000, 68, "#eef5fb", "#a8c8e0",
                "权重越依赖图像内容，边缘保护越强；错误匹配和选择偏差也越值得检查",
                None, "#285b7a", 18)
    ElementTree(svg).write(SVG_DIR / "denoiser_weight_maps.svg", encoding="utf-8",
                           xml_declaration=True)


def bias_variance_denoising():
    width, height = 1500, 760
    svg = base_svg(width, height, "降噪强度的偏差方差权衡")
    text(svg, 750, 43, "降噪强度增加时：随机起伏下降，结构偏差上升",
         size=30, weight="700", fill="#102a43")
    l, r, t, b = 125, 1010, 125, 590
    axes(svg, l, r, t, b, "降噪强度 λ", "平均误差")
    variance_pts, bias_pts, total_pts = [], [], []
    min_total = (None, 1e9, None)
    for j in range(201):
        u = j / 200
        variance = 0.78 * math.exp(-4.0 * u) + 0.06
        bias = 0.05 + 0.74 * (u ** 2.2)
        total = variance + bias
        x = l + u * (r - l)
        scale = 0.62 * (b - t)
        variance_pts.append((x, b - variance * scale))
        bias_pts.append((x, b - bias * scale))
        total_pts.append((x, b - total * scale))
        if total < min_total[1]:
            min_total = (x, total, b - total * scale)
    polyline(svg, variance_pts, stroke="#3b82b5", width=5)
    polyline(svg, bias_pts, stroke="#c85b73", width=5)
    polyline(svg, total_pts, stroke="#4d8c6a", width=6)
    x_min, _, y_min = min_total
    line(svg, x_min, b, x_min, y_min, stroke="#c58a2d", width=3, dash="9 7")
    SubElement(svg, "circle", {"cx": str(x_min), "cy": str(y_min), "r": "8", "fill": "#c58a2d"})
    text(svg, x_min + 18, y_min - 20, "示意最小点", size=16, weight="700",
         fill="#8a5f19", anchor="start")
    legend = [("残余噪声 / 方差", "#3b82b5"), ("细节损失 / 偏差²", "#c85b73"),
              ("总均方误差", "#4d8c6a")]
    y = 190
    for name, color in legend:
        line(svg, 1080, y, 1160, y, stroke=color, width=6)
        text(svg, 1180, y + 7, name, size=18, weight="700", fill=color, anchor="start")
        y += 62
    rounded_box(svg, 1060, 395, 360, 160, "#fff7e8", "#e8c77d", "不存在脱离任务的最佳 λ",
                "皮肤、星点、文字与打印输出，对偏差和方差的代价不同", "#8a5f19", 19)
    rounded_box(svg, 275, 650, 950, 65, "#ffffff", "#b9c7d3",
                "曲线是决策模型，不是所有算法共享的固定形状；正确位置还随输出尺寸改变",
                None, "#334e68", 17)
    ElementTree(svg).write(SVG_DIR / "bias_variance_denoising.svg", encoding="utf-8",
                           xml_declaration=True)


def ai_posterior_ambiguity():
    width, height = 1500, 800
    svg = base_svg(width, height, "学习型恢复中的后验歧义与输出选择")
    text(svg, 750, 43, "同一低质量观测可能对应多种干净图像；损失函数决定输出哪一种",
         size=30, weight="700", fill="#102a43")
    rounded_box(svg, 55, 280, 270, 170, "#fff0f3", "#eab0be", "观测 y",
                "噪声 + 模糊 + 采样损失", "#a24862")
    # noisy mini-grid
    rng = random.Random(31)
    for row in range(4):
        for col in range(6):
            val = max(0.1, min(.9, .5 + .19 * math.sin((row + col) * 1.4) + rng.gauss(0, .15)))
            c = int(250 - 150 * val)
            SubElement(svg, "rect", {
                "x": str(95 + col * 29), "y": str(365 + row * 18), "width": "27", "height": "16",
                "rx": "2", "fill": f"rgb({c},{c+8},{min(255,c+18)})",
            })
    line(svg, 325, 365, 470, 365, stroke="#527da3", width=4, marker="arrow-blue")
    text(svg, 397, 337, "p(x|y)", size=20, weight="700", fill="#285b7a")

    candidates = [
        (500, 115, "候选 A", "细线纹理", "#eaf4ff", "#9bc7ee", "stripes"),
        (500, 315, "候选 B", "平滑表面", "#edf8f2", "#9fd6b7", "smooth"),
        (500, 515, "候选 C", "颗粒结构", "#f7efff", "#c9a9e8", "dots"),
    ]
    for x0, y0, title_value, subtitle, fill, stroke, mode in candidates:
        rounded_box(svg, x0, y0, 310, 145, fill, stroke, title_value, subtitle, title_size=19)
        if mode == "stripes":
            for xx in range(x0 + 55, x0 + 270, 18):
                line(svg, xx, y0 + 90, xx + 25, y0 + 122, stroke="#3b82b5", width=3)
        elif mode == "smooth":
            for k in range(8):
                line(svg, x0 + 55, y0 + 92 + k * 4, x0 + 270, y0 + 92 + k * 4,
                     stroke="#4d8c6a", width=3)
        else:
            for row in range(3):
                for col in range(8):
                    SubElement(svg, "circle", {
                        "cx": str(x0 + 62 + col * 28 + (row % 2) * 8),
                        "cy": str(y0 + 92 + row * 14), "r": "5", "fill": "#7b4b74",
                    })
    for yy in (187, 387, 587):
        line(svg, 470, 365, 490, yy, stroke="#9ab3c6", width=3, marker="arrow-blue")

    rounded_box(svg, 900, 125, 520, 150, "#eef5fb", "#a8c8e0", "平方误差：条件均值",
                "多种候选被平均，通常稳健，但细纹理可能变软", "#285b7a", 20)
    rounded_box(svg, 900, 335, 520, 150, "#fff7e8", "#e8c77d", "生成式输出：抽取或偏向高概率样本",
                "外观更锐利，却可能选择了并未发生的具体纹理", "#8a5f19", 19)
    rounded_box(svg, 900, 545, 520, 150, "#fff0f3", "#eab0be", "证据要求：保留观测与处理记录",
                "区分数据约束的结构、先验补全的结构与人工编辑", "#a24862", 19)
    rounded_box(svg, 240, 735, 1020, 48, "#ffffff", "#b9c7d3",
                "看起来更像真实照片，是感知质量；能由这一份观测唯一支持，是证据强度",
                None, "#334e68", 17)
    ElementTree(svg).write(SVG_DIR / "ai_posterior_ambiguity.svg", encoding="utf-8",
                           xml_declaration=True)


def denoising_pipeline_diagnostics():
    width, height = 1500, 780
    svg = base_svg(width, height, "摄影降噪的诊断流程")
    text(svg, 750, 43, "先识别噪声和输出目标，再调强度；不要从“套一个模型”开始",
         size=30, weight="700", fill="#102a43")
    blocks = [
        (55, 120, "1　确认输入", "RAW/JPEG · 是否锐化\n是否缩放或压缩", "#eaf4ff", "#9bc7ee"),
        (380, 120, "2　定位来源", "光子不足 · 读出\n去马赛克 · 处理放大", "#edf8f2", "#9fd6b7"),
        (705, 120, "3　定义输出", "尺寸 · 观看距离\n打印或屏幕", "#fff7e8", "#e8c77d"),
        (1030, 120, "4　选择域与方法", "线性/编码 · 亮度/色彩\n局部/非局部/学习型", "#f7efff", "#c9a9e8"),
    ]
    for x0, y0, title_value, subtitle, fill, stroke in blocks:
        rounded_box(svg, x0, y0, 275, 150, fill, stroke, title_value, None, title_size=19)
        a, b = subtitle.split("\n")
        text(svg, x0 + 137, y0 + 92, a, size=15, fill="#486581")
        text(svg, x0 + 137, y0 + 120, b, size=15, fill="#486581")
    for x1, x2 in ((330, 370), (655, 695), (980, 1020)):
        line(svg, x1, 195, x2, 195, stroke="#527da3", width=4, marker="arrow-blue")

    rounded_box(svg, 160, 370, 500, 180, "#eef5fb", "#a8c8e0", "5　检查残差",
                "残差应像预期噪声，而不是仍含边缘、毛发、星点或文字", "#285b7a", 21)
    rounded_box(svg, 840, 370, 500, 180, "#fff0f3", "#eab0be", "6　检查最终输出",
                "在交付尺寸比较细节、色斑、涂抹、光晕与重复纹理", "#a24862", 21)
    line(svg, 1167, 270, 1167, 350, stroke="#527da3", width=4, marker="arrow-blue")
    line(svg, 840, 460, 680, 460, stroke="#527da3", width=4, marker="arrow-blue")
    line(svg, 410, 550, 410, 620, stroke="#c58a2d", width=4)
    line(svg, 410, 620, 1090, 620, stroke="#c58a2d", width=4)
    line(svg, 1090, 620, 1090, 560, stroke="#c58a2d", width=4, marker="arrow-gold")
    text(svg, 750, 648, "若残差有结构或输出出现伪影，回退参数、掩模或处理域", size=17,
         weight="700", fill="#8a5f19")
    rounded_box(svg, 260, 690, 980, 55, "#ffffff", "#b9c7d3",
                "保留原始文件与可逆参数；降噪结果是面向任务的版本，不是新的原始证据",
                None, "#334e68", 17)
    ElementTree(svg).write(SVG_DIR / "denoising_pipeline_diagnostics.svg", encoding="utf-8",
                           xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    signal_noise_overlap()
    denoiser_weight_maps()
    bias_variance_denoising()
    ai_posterior_ambiguity()
    denoising_pipeline_diagnostics()


if __name__ == "__main__":
    main()
