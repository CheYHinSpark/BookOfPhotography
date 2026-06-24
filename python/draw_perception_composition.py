from pathlib import Path
from xml.etree.ElementTree import SubElement, ElementTree
import math

from draw_raw_pipeline import base_svg, text, line, polyline, rounded_box, axes


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"


def adaptation_context():
    width, height = 1500, 780
    svg = base_svg(width, height, "视觉适应与同时对比使相同像素产生不同外观")
    text(svg, 750, 43, "同一数值不保证同一外观：视觉会按环境与邻域重新归一化",
         size=30, weight="700", fill="#102a43")
    panels = [
        (55, "暗背景", "同一灰块显得更亮", "#1f2937", "#888888"),
        (510, "亮背景", "同一灰块显得更暗", "#e5e7eb", "#888888"),
        (965, "局部渐变", "边界与局部对比改变读数感", "gradient", "#888888"),
    ]
    for x0, title_value, subtitle, bg, patch in panels:
        rounded_box(svg, x0, 110, 410, 480, "#ffffff", "#b9c7d3", title_value, subtitle,
                    title_size=21)
        if bg == "gradient":
            for k in range(24):
                c = int(35 + 205 * k / 23)
                SubElement(svg, "rect", {"x": str(x0 + 45 + k * 13), "y": "255",
                                          "width": "14", "height": "210",
                                          "fill": f"rgb({c},{c},{c})"})
        else:
            SubElement(svg, "rect", {"x": str(x0 + 45), "y": "255", "width": "320",
                                      "height": "210", "rx": "8", "fill": bg})
        SubElement(svg, "rect", {"x": str(x0 + 150), "y": "310", "width": "110",
                                  "height": "100", "rx": "7", "fill": patch,
                                  "stroke": "#f8fafc", "stroke-width": "2"})
        text(svg, x0 + 205, 510, "中心块均为 RGB 136,136,136", size=15, fill="#486581")
    rounded_box(svg, 210, 650, 1080, 65, "#eef5fb", "#a8c8e0",
                "校色能约束设备输出；适应、周围亮度和观看时间仍会改变主观明暗与彩度",
                None, "#285b7a", 18)
    ElementTree(svg).write(SVG_DIR / "adaptation_context.svg", encoding="utf-8",
                           xml_declaration=True)


def csf_viewing_scale():
    width, height = 1500, 790
    svg = base_svg(width, height, "对比敏感度观看距离与主观清晰感")
    text(svg, 750, 43, "可见细节由角频率与对比共同决定：文件像素只是中间尺度",
         size=30, weight="700", fill="#102a43")
    l, r, t, b = 110, 800, 130, 585
    axes(svg, l, r, t, b, "空间频率（cycles/degree，对数）", "对比敏感度")
    pts = []
    for j in range(241):
        u = j / 240
        logf = -0.5 + 2.4 * u
        f = 10 ** logf
        sensitivity = (f ** 0.8) * math.exp(-f / 8.5)
        sensitivity /= 1.35
        x = l + u * (r - l)
        y = b - min(.92, sensitivity) * (b - t)
        pts.append((x, y))
    polyline(svg, pts, stroke="#3b82b5", width=6)
    text(svg, 375, 205, "中频最敏感", size=18, weight="700", fill="#285b7a")
    text(svg, 160, 535, "低频：需较大对比", size=15, fill="#627d98", anchor="start")
    text(svg, 650, 535, "高频：细到不可见", size=15, fill="#627d98", anchor="start")

    rounded_box(svg, 910, 125, 485, 170, "#eaf4ff", "#9bc7ee", "同一输出，靠近观看",
                "特征张角增大；细节进入可见频带", "#285b7a", 20)
    rounded_box(svg, 910, 350, 485, 170, "#fff7e8", "#e8c77d", "同一输出，远离观看",
                "高频细节合并；噪声和光晕也可能减弱", "#8a5f19", 20)
    # eye and output geometry
    for y, dist, color in ((245, 300, "#3b82b5"), (470, 390, "#c58a2d")):
        SubElement(svg, "circle", {"cx": "975", "cy": str(y), "r": "12", "fill": color})
        SubElement(svg, "rect", {"x": str(975 + dist), "y": str(y - 45), "width": "12",
                                  "height": "90", "fill": "#829ab1"})
        line(svg, 990, y, 970 + dist, y - 45, stroke=color, width=2)
        line(svg, 990, y, 970 + dist, y + 45, stroke=color, width=2)
    rounded_box(svg, 870, 610, 565, 105, "#edf8f2", "#9fd6b7", "角频率换算",
                "周期 p、观看距离 d：ν ≈ πd/(180p) cycles/degree", "#397456", 19)
    ElementTree(svg).write(SVG_DIR / "csf_viewing_scale.svg", encoding="utf-8",
                           xml_declaration=True)


def depth_cues():
    width, height = 1500, 790
    svg = base_svg(width, height, "单张照片中的多种深度线索")
    text(svg, 750, 43, "平面照片没有真实纵深；遮挡、尺度、透视、清晰度与空气共同制造深度解释",
         size=30, weight="700", fill="#102a43")
    cards = [
        (40, "遮挡与相对大小", "前物覆盖后物；熟悉尺度帮助判断", "occlusion"),
        (405, "线性透视与纹理梯度", "平行线汇聚；纹理随距离变密", "perspective"),
        (770, "空气透视与色彩分离", "远处对比降低、偏向环境光色", "air"),
        (1135, "清晰度与虚化", "焦点选择提示层级，但可被后期伪造", "blur"),
    ]
    for x0, title_value, subtitle, mode in cards:
        rounded_box(svg, x0, 110, 325, 535, "#ffffff", "#b9c7d3", title_value, subtitle,
                    title_size=19)
        if mode == "occlusion":
            SubElement(svg, "circle", {"cx": str(x0 + 205), "cy": "410", "r": "78",
                                        "fill": "#8fb7d9"})
            SubElement(svg, "circle", {"cx": str(x0 + 130), "cy": "435", "r": "58",
                                        "fill": "#d69b67"})
            text(svg, x0 + 165, 545, "覆盖关系给出前后顺序", size=15, fill="#486581")
        elif mode == "perspective":
            vx, vy = x0 + 165, 305
            for y in (355, 410, 470, 535):
                line(svg, x0 + 55, y, vx, vy, stroke="#527da3", width=2)
                line(svg, x0 + 270, y, vx, vy, stroke="#527da3", width=2)
            for k in range(7):
                yy = 335 + 35 * (k ** 1.25)
                if yy < 555:
                    line(svg, x0 + 85, yy, x0 + 245, yy, stroke="#9ab3c6", width=2)
        elif mode == "air":
            for k, (w, h, op) in enumerate(((210, 145, .9), (155, 105, .58), (105, 72, .30))):
                SubElement(svg, "path", {"d": f"M {x0+55+k*45} {520-k*70} l {w/2} {-h} l {w/2} {h} z",
                                          "fill": "#4d8c6a", "fill-opacity": str(op)})
            SubElement(svg, "rect", {"x": str(x0 + 35), "y": "280", "width": "255", "height": "280",
                                      "fill": "#a8d5e8", "fill-opacity": ".20"})
        else:
            for cx, rr, op in ((x0 + 105, 45, .22), (x0 + 165, 38, .45), (x0 + 230, 30, .88)):
                for scale in (1.8, 1.35, 1.0):
                    SubElement(svg, "circle", {"cx": str(cx), "cy": "420", "r": str(rr * scale),
                                                "fill": "#7b4b74", "fill-opacity": str(op / (scale * 2))})
            text(svg, x0 + 165, 540, "最清晰处常被解释为主体层", size=15, fill="#486581")
    rounded_box(svg, 225, 700, 1050, 58, "#fff7e8", "#e8c77d",
                "单一线索可能歧义；多种线索方向一致时，深度感通常更稳定",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "depth_cues.svg", encoding="utf-8",
                           xml_declaration=True)


def attention_composition():
    width, height = 1500, 800
    svg = base_svg(width, height, "构图作为注意力竞争与关系组织")
    text(svg, 750, 43, "构图不是把主体放进格子：它在有限画面内分配对比、尺度、方向与边界关系",
         size=30, weight="700", fill="#102a43")
    rounded_box(svg, 55, 105, 760, 560, "#ffffff", "#b9c7d3", "画面中的竞争线索",
                "亮度 · 色彩 · 尺度 · 清晰度 · 人脸 · 方向", "#285b7a", 21)
    # frame
    SubElement(svg, "rect", {"x": "115", "y": "235", "width": "640", "height": "350",
                              "fill": "#edf3f7", "stroke": "#829ab1", "stroke-width": "3"})
    # main subject
    SubElement(svg, "circle", {"cx": "405", "cy": "395", "r": "72", "fill": "#c85b73"})
    SubElement(svg, "circle", {"cx": "380", "cy": "380", "r": "7", "fill": "#ffffff"})
    SubElement(svg, "circle", {"cx": "430", "cy": "380", "r": "7", "fill": "#ffffff"})
    # competitors and directional lines
    SubElement(svg, "rect", {"x": "620", "y": "270", "width": "90", "height": "70",
                              "fill": "#f1c75b"})
    SubElement(svg, "circle", {"cx": "220", "cy": "505", "r": "38", "fill": "#3b82b5"})
    line(svg, 135, 300, 370, 390, stroke="#4d8c6a", width=5, marker="arrow-green")
    line(svg, 705, 545, 465, 420, stroke="#7b4b74", width=5, marker="arrow-purple")
    text(svg, 405, 625, "主体由观看任务与关系共同指定", size=17, weight="700", fill="#486581")

    rounded_box(svg, 900, 110, 525, 125, "#eaf4ff", "#9bc7ee", "自下而上显著性",
                "局部差异、孤立特征和人脸可快速吸引注意", "#285b7a", 20)
    rounded_box(svg, 900, 285, 525, 125, "#edf8f2", "#9fd6b7", "自上而下任务",
                "标题、题材知识与寻找目标改变观看顺序", "#397456", 20)
    rounded_box(svg, 900, 460, 525, 125, "#fff7e8", "#e8c77d", "边界与裁切",
                "切断、接触、方向延续与画外空间改变关系", "#8a5f19", 20)
    rounded_box(svg, 250, 710, 1000, 52, "#fff0f3", "#eab0be",
                "减少背景竞争通常比继续增强主体更自然；显著性模型不能推出审美评分",
                None, "#a24862", 17)
    ElementTree(svg).write(SVG_DIR / "attention_composition.svg", encoding="utf-8",
                           xml_declaration=True)


def tone_style_structure():
    width, height = 1500, 810
    svg = base_svg(width, height, "空间影调结构与跨作品风格")
    text(svg, 750, 43, "直方图只统计有多少，不记录在哪里；风格则来自跨作品重复出现的选择",
         size=30, weight="700", fill="#102a43")
    # Same histogram, different spatial arrangement
    rounded_box(svg, 45, 110, 650, 510, "#ffffff", "#b9c7d3", "相同全局直方图，不同空间结构",
                "亮暗面积一致，视线与层次可以完全不同", "#285b7a", 21)
    layouts = [(105, "亮主体 / 暗背景", True), (385, "暗主体 / 亮背景", False)]
    for x0, label, bright_subject in layouts:
        bg = "#2f3b46" if bright_subject else "#d9e2e8"
        fg = "#d9e2e8" if bright_subject else "#2f3b46"
        SubElement(svg, "rect", {"x": str(x0), "y": "275", "width": "230", "height": "220",
                                  "rx": "7", "fill": bg})
        SubElement(svg, "circle", {"cx": str(x0 + 115), "cy": "385", "r": "70", "fill": fg})
        text(svg, x0 + 115, 535, label, size=16, weight="700", fill="#486581")
    # histogram bars same
    for base_x in (120, 400):
        heights = [35, 65, 92, 75, 48]
        for k, h in enumerate(heights):
            SubElement(svg, "rect", {"x": str(base_x + k * 38), "y": str(235 - h),
                                      "width": "28", "height": str(h), "fill": "#829ab1"})

    rounded_box(svg, 780, 110, 675, 510, "#ffffff", "#b9c7d3", "风格是一组稳定选择的联合分布",
                "题材 · 机位 · 光线 · 时机 · 色彩 · 影调 · 编辑", "#8a5f19", 21)
    stages = [
        (825, "拍什么", "题材/时机", "#eaf4ff", "#9bc7ee"),
        (1030, "怎样拍", "机位/光线", "#edf8f2", "#9fd6b7"),
        (1235, "怎样呈现", "色调/编辑", "#fff7e8", "#e8c77d"),
    ]
    for x0, title_value, subtitle, fill, stroke in stages:
        rounded_box(svg, x0, 275, 175, 120, fill, stroke, title_value, subtitle, title_size=18)
    line(svg, 1000, 335, 1020, 335, stroke="#527da3", width=3, marker="arrow-blue")
    line(svg, 1205, 335, 1225, 335, stroke="#527da3", width=3, marker="arrow-blue")
    rounded_box(svg, 880, 455, 475, 105, "#fff0f3", "#eab0be", "预设只作用于最后一段",
                "能复制曲线与颜色，不能替代题材、机位和光线", "#a24862", 18)
    rounded_box(svg, 225, 690, 1050, 68, "#eef5fb", "#a8c8e0",
                "高调/低调描述画面调性与面积分布，不等同于拍摄时过曝/欠曝",
                None, "#285b7a", 18)
    ElementTree(svg).write(SVG_DIR / "tone_style_structure.svg", encoding="utf-8",
                           xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    adaptation_context()
    csf_viewing_scale()
    depth_cues()
    attention_composition()
    tone_style_structure()


if __name__ == "__main__":
    main()
