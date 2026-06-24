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


def rounded_box(parent, x, y, w, h, fill, stroke, title_value, subtitle=None,
                title_color="#102a43", title_size=21):
    SubElement(parent, "rect", {
        "x": str(x), "y": str(y), "width": str(w), "height": str(h),
        "rx": "16", "fill": fill, "stroke": stroke, "stroke-width": "2.5",
    })
    text(parent, x + w / 2, y + 42, title_value, size=title_size,
         weight="700", fill=title_color)
    if subtitle:
        text(parent, x + w / 2, y + 76, subtitle, size=15, fill="#486581")


def axes(parent, l, r, t, b, x_label=None, y_label=None):
    line(parent, l, b, r, b, stroke="#334e68", width=2, marker="arrow-dark")
    line(parent, l, b, l, t, stroke="#334e68", width=2, marker="arrow-dark")
    if x_label:
        text(parent, r, b + 31, x_label, size=15, fill="#627d98", anchor="end")
    if y_label:
        text(parent, l - 4, t - 12, y_label, size=15, fill="#627d98", anchor="start")


def raw_record_layers():
    width, height = 1500, 720
    svg = base_svg(width, height, "RAW文件由马赛克测量、校准元数据、几何元数据和预览共同组成")
    text(svg, 750, 45, "RAW 是“测量数组 + 解释它所需的条件”，不是已经完成的 RGB 图像",
         size=30, weight="700", fill="#102a43")
    layers = [
        (95, "马赛克码值", "每个像素只测一个 CFA 通道；可能压缩或打包", "#eaf4ff", "#9bc7ee"),
        (195, "辐射校准", "黑电平 · 白电平 · 线性化表 · 增益图 · 坏点", "#edf8f2", "#9fd6b7"),
        (295, "颜色条件", "CFA 光谱标签 · 白平衡 · 颜色矩阵 · 参考照明", "#fff7e8", "#e8c77d"),
        (395, "几何与拍摄元数据", "裁切区 · 方向 · 镜头信息 · 时间 · 曝光参数", "#f7efff", "#c9a9e8"),
        (495, "预览与缩略图", "快速显示用 JPEG；通常已经去马赛克和色调映射", "#fff0f3", "#eab0be"),
    ]
    for y, title_value, subtitle, fill, stroke in layers:
        rounded_box(svg, 155, y, 1190, 78, fill, stroke, title_value, subtitle)
    line(svg, 95, 95, 95, 572, stroke="#7b4b74", width=4)
    for y in (134, 234, 334, 434, 534):
        line(svg, 95, y, 145, y, stroke="#7b4b74", width=4)
    text(svg, 95, 625, "同一容器", size=18, weight="700", fill="#7b4b74")
    rounded_box(svg, 280, 620, 940, 62, "#eef5fb", "#a8c8e0",
                "缺少校准元数据时，同一整数数组可对应不同黑点、尺度、颜色与有效画幅",
                None, "#285b7a", 18)
    ElementTree(svg).write(SVG_DIR / "raw_record_layers.svg", encoding="utf-8", xml_declaration=True)


def black_white_normalization():
    width, height = 1500, 730
    svg = base_svg(width, height, "黑电平白电平线性化与归一化")
    text(svg, 750, 43, "从存储码值到相对曝光：先校正偏置，再恢复线性尺度",
         size=30, weight="700", fill="#102a43")
    # Left graph.
    l, r, t, b = 95, 695, 120, 575
    axes(svg, l, r, t, b, "存储码值 r", "归一化响应 x")
    blevel, wlevel = l + 145, r - 105
    line(svg, blevel, b, blevel, t + 35, stroke="#c85b73", width=3, dash="9 7")
    line(svg, wlevel, b, wlevel, t + 35, stroke="#c58a2d", width=3, dash="9 7")
    pts = [(l, b), (blevel, b), (wlevel, t + 70), (r, t + 70)]
    polyline(svg, pts, stroke="#3b82b5", width=6)
    text(svg, blevel, b + 45, "黑电平 b", size=17, fill="#a24862")
    text(svg, wlevel, b + 45, "白电平 w", size=17, fill="#8a5f19")
    text(svg, (blevel + wlevel) / 2, 305, "x=(r-b)/(w-b)", size=25, weight="700", fill="#285b7a")
    text(svg, l + 30, 520, "负值区", size=15, fill="#627d98")
    text(svg, r - 35, 180, "饱和区", size=15, fill="#627d98")
    # Right: calibration hierarchy.
    rounded_box(svg, 815, 115, 560, 92, "#fff0f3", "#eab0be", "标量黑电平",
                "一个 b：只能校正全局电子偏置", "#a24862")
    rounded_box(svg, 815, 245, 560, 92, "#fff7e8", "#e8c77d", "按通道/按行黑电平",
                "b_c 或 b_{c,y}：校正 CFA 与读出链差异", "#8a5f19")
    rounded_box(svg, 815, 375, 560, 92, "#edf8f2", "#9fd6b7", "逐像素暗场模型",
                "b_i(t,T)：进一步描述曝光时间与温度", "#397456")
    for y in (207, 337):
        line(svg, 1095, y, 1095, y + 30, stroke="#527da3", width=3, marker="arrow-blue")
    rounded_box(svg, 810, 535, 570, 115, "#eef5fb", "#a8c8e0", "线性化不是任意调曲线",
                "它试图让校正值重新与曝光成比例；创作色调映射属于更后阶段", "#285b7a", 20)
    ElementTree(svg).write(SVG_DIR / "black_white_normalization.svg", encoding="utf-8", xml_declaration=True)


def raw_pipeline_dag():
    width, height = 1500, 760
    svg = base_svg(width, height, "RAW处理链的有向无环图")
    text(svg, 750, 43, "一条典型 RAW 管线：数据域、空间分辨率与噪声模型持续变化",
         size=30, weight="700", fill="#102a43")
    blocks = [
        (35, "原始码值", "CFA / DN", "#eaf4ff", "#9bc7ee"),
        (260, "黑电平/线性化", "线性 CFA", "#edf8f2", "#9fd6b7"),
        (545, "缺陷与增益图", "校准 CFA", "#fff7e8", "#e8c77d"),
        (830, "白平衡", "通道缩放", "#f7efff", "#c9a9e8"),
        (1055, "去马赛克", "相机 RGB", "#fff0f3", "#eab0be"),
        (1280, "颜色变换", "工作 RGB", "#eef5fb", "#a8c8e0"),
    ]
    for x, title_value, subtitle, fill, stroke in blocks:
        rounded_box(svg, x, 130, 185, 112, fill, stroke, title_value, subtitle, title_size=18)
    for x1, x2 in ((220, 250), (445, 535), (730, 820), (1015, 1045), (1240, 1270)):
        line(svg, x1, 186, x2, 186, stroke="#527da3", width=3, marker="arrow-blue")
    # second row
    lower = [
        (230, "降噪", "信号相关", "#edf8f2", "#9fd6b7"),
        (495, "外观/色调", "场景→显示", "#fff7e8", "#e8c77d"),
        (760, "锐化/缩放", "输出相关", "#f7efff", "#c9a9e8"),
        (1025, "OETF/量化", "编码码值", "#fff0f3", "#eab0be"),
        (1290, "文件/显示", "JPEG/HEIF…", "#eef5fb", "#a8c8e0"),
    ]
    for x, title_value, subtitle, fill, stroke in lower:
        rounded_box(svg, x, 390, 185, 112, fill, stroke, title_value, subtitle, title_size=18)
    for x1, x2 in ((415, 485), (680, 750), (945, 1015), (1210, 1280)):
        line(svg, x1, 446, x2, 446, stroke="#527da3", width=3, marker="arrow-blue")
    line(svg, 1372, 242, 1372, 335, stroke="#527da3", width=3)
    line(svg, 1372, 335, 322, 335, stroke="#527da3", width=3)
    line(svg, 322, 335, 322, 380, stroke="#527da3", width=3, marker="arrow-blue")
    # Metadata bus.
    rounded_box(svg, 150, 610, 1200, 78, "#ffffff", "#b9c7d3", "元数据与相机配置文件",
                "黑/白电平、增益图、噪声模型、CFA 排列、颜色矩阵、裁切与方向分别约束不同节点",
                "#334e68", 20)
    for x in (350, 650, 915, 1150, 1370):
        line(svg, x, 600, x, 520 if x < 1200 else 255, stroke="#9aa9b5", width=2, dash="7 7")
    text(svg, 750, 735, "实际实现可合并、拆分或迭代节点；这不是唯一顺序，但每次换序都必须证明等价",
         size=18, weight="700", fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "raw_pipeline_dag.svg", encoding="utf-8", xml_declaration=True)


def operator_commutator():
    width, height = 1500, 720
    svg = base_svg(width, height, "两个图像算子换序与交换子")
    text(svg, 750, 43, "操作顺序的数学判据：交换子 [A,B]=AB−BA 是否为零",
         size=30, weight="700", fill="#102a43")
    rounded_box(svg, 55, 275, 190, 110, "#eaf4ff", "#9bc7ee", "输入 x", "某一数据域")
    # upper path
    rounded_box(svg, 390, 115, 230, 110, "#edf8f2", "#9fd6b7", "先 A", "例如白平衡 G")
    rounded_box(svg, 790, 115, 230, 110, "#fff7e8", "#e8c77d", "再 B", "例如颜色矩阵 M")
    rounded_box(svg, 1190, 115, 250, 110, "#eef5fb", "#a8c8e0", "BAx", "路径 1")
    # lower path
    rounded_box(svg, 390, 445, 230, 110, "#fff7e8", "#e8c77d", "先 B", "例如颜色矩阵 M")
    rounded_box(svg, 790, 445, 230, 110, "#edf8f2", "#9fd6b7", "再 A", "例如白平衡 G")
    rounded_box(svg, 1190, 445, 250, 110, "#fff0f3", "#eab0be", "ABx", "路径 2")
    # branch arrows
    line(svg, 245, 330, 315, 330, stroke="#527da3", width=4)
    line(svg, 315, 330, 315, 170, stroke="#527da3", width=4)
    line(svg, 315, 170, 380, 170, stroke="#527da3", width=4, marker="arrow-blue")
    line(svg, 315, 330, 315, 500, stroke="#527da3", width=4)
    line(svg, 315, 500, 380, 500, stroke="#527da3", width=4, marker="arrow-blue")
    for y in (170, 500):
        line(svg, 620, y, 780, y, stroke="#527da3", width=4, marker="arrow-blue")
        line(svg, 1020, y, 1180, y, stroke="#527da3", width=4, marker="arrow-blue")
    text(svg, 750, 330, "差值：BAx − ABx = −[A,B]x", size=27, weight="700", fill="#7b4b74")
    rounded_box(svg, 405, 620, 690, 65, "#fff0f3", "#eab0be",
                "对角增益 G 与通道混合矩阵 M 一般不交换；裁切与任何会越界的算子也通常不交换",
                None, "#a24862", 18)
    ElementTree(svg).write(SVG_DIR / "operator_commutator.svg", encoding="utf-8", xml_declaration=True)


def cfa_measurement_reconstruction():
    width, height = 1500, 720
    svg = base_svg(width, height, "CFA测量并不是低分辨率RGB缩略图")
    text(svg, 750, 43, "去马赛克是在欠采样颜色场上做估计，不是在黑色空格中“补颜色”",
         size=30, weight="700", fill="#102a43")
    panels = [(55, "连续三通道场", "每个位置潜在有 R,G,B"),
              (540, "CFA 单通道观测", "每个像素只保留一个投影"),
              (1025, "估计的 RGB 场", "利用空间与跨通道先验")]
    for px, title_value, subtitle in panels:
        text(svg, px + 190, 105, title_value, size=23, weight="700", fill="#285b7a")
        text(svg, px + 190, 135, subtitle, size=15, fill="#627d98")
    colors = {"R": "#d86b7e", "G": "#68a879", "B": "#5e8fc7"}
    # left RGB mixtures
    for row in range(6):
        for col in range(6):
            x, y = 95 + col * 48, 180 + row * 58
            rr = 90 + col * 20
            gg = 145 + row * 12
            bb = 205 - col * 10
            fill = f"rgb({min(rr,235)},{min(gg,220)},{max(bb,90)})"
            SubElement(svg, "rect", {"x": str(x), "y": str(y), "width": "44", "height": "54",
                                      "rx": "5", "fill": fill, "stroke": "#ffffff"})
    # Bayer samples
    pattern = [["R", "G"], ["G", "B"]]
    for row in range(6):
        for col in range(6):
            x, y = 580 + col * 48, 180 + row * 58
            c = pattern[row % 2][col % 2]
            SubElement(svg, "rect", {"x": str(x), "y": str(y), "width": "44", "height": "54",
                                      "rx": "5", "fill": colors[c], "stroke": "#ffffff"})
            text(svg, x + 22, y + 35, c, size=18, weight="700", fill="#ffffff")
    # reconstructed mixtures with a false-color edge warning
    for row in range(6):
        for col in range(6):
            x, y = 1065 + col * 48, 180 + row * 58
            rr = 92 + col * 20
            gg = 143 + row * 12
            bb = 202 - col * 10
            fill = f"rgb({min(rr,235)},{min(gg,220)},{max(bb,90)})"
            if row == 2 and col in (2, 3):
                fill = "#bb72b8"
            SubElement(svg, "rect", {"x": str(x), "y": str(y), "width": "44", "height": "54",
                                      "rx": "5", "fill": fill, "stroke": "#ffffff"})
    line(svg, 390, 350, 520, 350, stroke="#527da3", width=4, marker="arrow-blue")
    line(svg, 875, 350, 1005, 350, stroke="#527da3", width=4, marker="arrow-blue")
    rounded_box(svg, 235, 590, 1030, 80, "#fff7e8", "#e8c77d",
                "边缘方向、纹理周期与通道相关性构成先验；高频超出采样带宽时，假色和摩尔纹不可被唯一消除",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "cfa_measurement_reconstruction.svg", encoding="utf-8", xml_declaration=True)


def noise_jacobian_propagation():
    width, height = 1500, 720
    svg = base_svg(width, height, "图像处理管线中的均值协方差与雅可比传播")
    text(svg, 750, 43, "数值被变换时，噪声的均值、方差、相关性和分布也一起被变换",
         size=30, weight="700", fill="#102a43")
    stages = [
        (55, "传感器域", "μ, Σ", "#eaf4ff", "#9bc7ee"),
        (365, "线性算子 A", "μ′=Aμ", "#edf8f2", "#9fd6b7"),
        (675, "非线性算子 f", "局部雅可比 J", "#fff7e8", "#e8c77d"),
        (985, "重采样/锐化", "产生空间相关", "#f7efff", "#c9a9e8"),
        (1295, "输出域", "信号相关噪声", "#fff0f3", "#eab0be"),
    ]
    for x, title_value, subtitle, fill, stroke in stages:
        rounded_box(svg, x, 120, 155, 105, fill, stroke, title_value, subtitle, title_size=17)
    for x1, x2 in ((210, 355), (520, 665), (830, 975), (1140, 1285)):
        line(svg, x1, 172, x2, 172, stroke="#527da3", width=3, marker="arrow-blue")
    # Ellipses as covariance cartoons.
    ellipses = [(135, 410, 55, 95, -10, "#5e8fc7"), (445, 410, 100, 42, 25, "#68a879"),
                (755, 410, 82, 34, -25, "#d0a04b"), (1065, 410, 120, 25, 0, "#9670bb"),
                (1375, 410, 100, 50, 35, "#d86b7e")]
    for cx, cy, rx, ry, rot, color in ellipses:
        SubElement(svg, "ellipse", {"cx": str(cx), "cy": str(cy), "rx": str(rx), "ry": str(ry),
                                    "transform": f"rotate({rot} {cx} {cy})", "fill": color,
                                    "fill-opacity": "0.20", "stroke": color, "stroke-width": "4"})
        SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": "7", "fill": color})
    formulas = ["Σ", "AΣAᵀ", "JΣJᵀ", "HΣHᵀ", "Σout"]
    for x, value in zip((135, 445, 755, 1065, 1375), formulas):
        text(svg, x, 545, value, size=24, weight="700", fill="#334e68")
    rounded_box(svg, 250, 610, 1000, 68, "#eef5fb", "#a8c8e0",
                "只给图像乘增益却沿用原噪声参数，会让降噪阈值、置信区间和数据保真项同时失配",
                None, "#285b7a", 18)
    ElementTree(svg).write(SVG_DIR / "noise_jacobian_propagation.svg", encoding="utf-8", xml_declaration=True)


def scene_display_reference():
    width, height = 1500, 740
    svg = base_svg(width, height, "场景参照与显示参照工作流")
    text(svg, 750, 43, "场景参照保留相对曝光关系；显示参照规定设备实际应产生的外观",
         size=30, weight="700", fill="#102a43")
    # Scene branch.
    rounded_box(svg, 55, 130, 250, 115, "#eaf4ff", "#9bc7ee", "线性场景 RGB", "可大于 1，也可为负")
    rounded_box(svg, 445, 130, 250, 115, "#edf8f2", "#9fd6b7", "场景参照编辑", "曝光 · 白平衡 · 合成")
    rounded_box(svg, 835, 130, 250, 115, "#fff7e8", "#e8c77d", "外观变换", "色调与色域映射")
    rounded_box(svg, 1225, 130, 220, 115, "#fff0f3", "#eab0be", "显示 RGB", "有限峰值与色域")
    for x1, x2 in ((305, 435), (695, 825), (1085, 1215)):
        line(svg, x1, 187, x2, 187, stroke="#527da3", width=4, marker="arrow-blue")
    text(svg, 750, 315, "不可省略的方向变化：scene → appearance → display", size=25, weight="700", fill="#7b4b74")
    # Two examples.
    rounded_box(svg, 110, 390, 560, 185, "#eef5fb", "#a8c8e0", "场景参照问题",
                "“两个像素的曝光比是多少？”", "#285b7a")
    text(svg, 390, 520, "线性叠加、曝光合成与颜色矩阵在这里定义", size=17, fill="#486581")
    rounded_box(svg, 830, 390, 560, 185, "#fff0f3", "#eab0be", "显示参照问题",
                "“这个码值在目标屏幕上多亮？”", "#a24862")
    text(svg, 1110, 520, "黑白点、EOTF、环境光和输出介质在这里定义", size=17, fill="#486581")
    rounded_box(svg, 250, 635, 1000, 65, "#fff7e8", "#e8c77d",
                "把显示参照像素重新当作场景辐射量，会把已经烘焙的外观曲线误当成物理光比",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "scene_display_reference.svg", encoding="utf-8", xml_declaration=True)


def format_information_layers():
    width, height = 1500, 780
    svg = base_svg(width, height, "图像格式需要分开比较容器编码像素模型和元数据")
    text(svg, 750, 43, "文件后缀不是信息量：容器、编码、像素模型与处理状态必须分层比较",
         size=30, weight="700", fill="#102a43")
    headers = [(55, 350, "格式族"), (350, 615, "典型像素状态"), (615, 900, "编码与精度"),
               (900, 1180, "元数据/可编辑性"), (1180, 1445, "主要角色")]
    for x1, x2, label in headers:
        SubElement(svg, "rect", {"x": str(x1), "y": "95", "width": str(x2-x1), "height": "65",
                                  "rx": "10", "fill": "#334e68"})
        text(svg, (x1+x2)/2, 137, label, size=18, weight="700", fill="#ffffff")
    rows = [
        ("相机 RAW / DNG", "CFA 或传感器域", "打包整数；可无损/有损", "校准元数据丰富", "原始测量与再解释"),
        ("TIFF / OpenEXR", "RGB/灰度；常为场景参照", "整数或浮点；可无损", "配置文件与辅助通道", "中间交换与高精度母版"),
        ("JPEG", "通常显示参照 YCbCr", "8 位常见；有损 DCT", "EXIF/ICC 可携带", "兼容交付与网络传输"),
        ("HEIF/AVIF", "显示参照或 HDR 图像", "高效有损/无损；可高位深", "序列、辅助图与色彩信息", "现代交付与计算照片容器"),
        ("参数文件/sidecar", "不存完整像素", "操作图与参数", "依赖原始文件和软件语义", "非破坏编辑的决策记录"),
    ]
    y = 175
    fills = ["#eaf4ff", "#edf8f2", "#fff7e8", "#f7efff", "#fff0f3"]
    bounds = [(55,350), (350,615), (615,900), (900,1180), (1180,1445)]
    for row, fill in zip(rows, fills):
        for (x1, x2), value in zip(bounds, row):
            SubElement(svg, "rect", {"x": str(x1), "y": str(y), "width": str(x2-x1), "height": "92",
                                      "fill": fill, "stroke": "#ffffff", "stroke-width": "3"})
            text(svg, (x1+x2)/2, y+40, value, size=16, weight="700" if x1==55 else "400", fill="#243b53")
        y += 96
    rounded_box(svg, 200, 685, 1100, 62, "#ffffff", "#b9c7d3",
                "“无损”只说明给定编码的比特可逆；若像素此前已裁切、去马赛克或色调映射，早期信息仍不会回来",
                None, "#7b4b74", 18)
    ElementTree(svg).write(SVG_DIR / "format_information_layers.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    raw_record_layers()
    black_white_normalization()
    raw_pipeline_dag()
    operator_commutator()
    cfa_measurement_reconstruction()
    noise_jacobian_propagation()
    scene_display_reference()
    format_information_layers()


if __name__ == "__main__":
    main()
