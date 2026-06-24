from pathlib import Path
from xml.etree.ElementTree import SubElement, ElementTree

from draw_raw_pipeline import base_svg, text, line, rounded_box


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"


def color_management_chain():
    width, height = 1500, 790
    svg = base_svg(width, height, "ICC色彩管理的源配置连接空间与目标设备链路")
    text(svg, 750, 43, "颜色管理不是“统一 RGB 数字”，而是借助配置文件保持颜色含义",
         size=30, weight="700", fill="#102a43")
    blocks = [
        (45, "源数据", "相机 RGB / 工作 RGB\n带源配置文件", "#eaf4ff", "#9bc7ee"),
        (330, "源变换", "矩阵 / TRC / LUT\n源状态 → PCS", "#edf8f2", "#9fd6b7"),
        (615, "连接空间 PCS", "XYZ 或 Lab\n规定白点与参照", "#fff7e8", "#e8c77d"),
        (900, "目标变换", "PCS → 设备值\n含色域映射", "#f7efff", "#c9a9e8"),
        (1185, "输出设备", "显示 RGB / 打印 CMYK\n在规定状态下", "#fff0f3", "#eab0be"),
    ]
    for x0, title_value, subtitle, fill, stroke in blocks:
        rounded_box(svg, x0, 170, 240, 175, fill, stroke, title_value, None, title_size=20)
        a, b = subtitle.split("\n")
        text(svg, x0 + 120, 275, a, size=15, fill="#486581")
        text(svg, x0 + 120, 305, b, size=15, fill="#486581")
    for x1, x2 in ((285, 320), (570, 605), (855, 890), (1140, 1175)):
        line(svg, x1, 258, x2, 258, stroke="#527da3", width=4, marker="arrow-blue")
    rounded_box(svg, 160, 465, 500, 145, "#eef5fb", "#a8c8e0", "校准 calibration",
                "把设备调到可重复目标状态：白点、亮度、灰阶响应", "#285b7a", 20)
    rounded_box(svg, 840, 465, 500, 145, "#edf8f2", "#9fd6b7", "表征 profiling",
                "测量该状态下数值与颜色的映射，生成配置文件", "#397456", 20)
    line(svg, 660, 538, 825, 538, stroke="#7b4b74", width=4, marker="arrow-purple")
    rounded_box(svg, 250, 690, 1000, 55, "#fff7e8", "#e8c77d",
                "配置文件描述设备，不自动修好设备；缺失或误分配源配置会让同一数字产生错误颜色",
                None, "#8a5f19", 17)
    ElementTree(svg).write(SVG_DIR / "color_management_chain.svg", encoding="utf-8",
                           xml_declaration=True)


def display_environment_calibration():
    width, height = 1500, 790
    svg = base_svg(width, height, "显示器校准环境光与观看条件")
    text(svg, 750, 43, "显示器只是输出系统的一部分：环境反射与视觉适应共同决定可见黑位和白点",
         size=30, weight="700", fill="#102a43")
    rounded_box(svg, 60, 125, 600, 500, "#ffffff", "#b9c7d3", "显示设备状态",
                "先稳定，再测量，再验证", "#285b7a", 22)
    # monitor
    SubElement(svg, "rect", {"x": "170", "y": "260", "width": "380", "height": "220",
                              "rx": "12", "fill": "#243b53", "stroke": "#829ab1", "stroke-width": "5"})
    for k, c in enumerate(("#dce7ef", "#a9becd", "#6f8799", "#334e68")):
        SubElement(svg, "rect", {"x": str(200 + k * 82), "y": "300", "width": "72",
                                  "height": "135", "fill": c})
    line(svg, 360, 480, 360, 535, stroke="#627d98", width=8)
    line(svg, 285, 535, 435, 535, stroke="#627d98", width=8)
    text(svg, 360, 585, "白点 · 亮度 · 黑位 · 灰阶 · 原色", size=17, weight="700", fill="#486581")

    rounded_box(svg, 790, 120, 610, 145, "#fff7e8", "#e8c77d", "环境光",
                "反射抬高屏幕黑位；彩色墙面改变适应与视觉白", "#8a5f19", 20)
    rounded_box(svg, 790, 320, 610, 145, "#eaf4ff", "#9bc7ee", "界面与周边",
                "明亮网页、深灰编辑器和暗展厅产生不同局部对比", "#285b7a", 20)
    rounded_box(svg, 790, 520, 610, 145, "#edf8f2", "#9fd6b7", "验证",
                "灰阶、色差、均匀性和目标亮度需定期复测", "#397456", 20)
    rounded_box(svg, 265, 710, 970, 48, "#fff0f3", "#eab0be",
                "不要用显示器亮度滑块修照片：先把设备和环境固定，再判断图像",
                None, "#a24862", 17)
    ElementTree(svg).write(SVG_DIR / "display_environment_calibration.svg", encoding="utf-8",
                           xml_declaration=True)


def screen_print_mapping():
    width, height = 1500, 810
    svg = base_svg(width, height, "屏幕到打印的介质差异与软打样")
    text(svg, 750, 43, "屏幕发光，纸张反光：色域、黑位、白点和局部对比不可能逐像素复制",
         size=30, weight="700", fill="#102a43")
    rounded_box(svg, 45, 125, 420, 450, "#eaf4ff", "#9bc7ee", "屏幕",
                "加色 RGB · 自发光", "#285b7a", 22)
    # RGB overlap
    for cx, cy, color in ((170, 345, "#ff4b5c"), (265, 345, "#43c56b"), (218, 425, "#4a73ff")):
        SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": "82", "fill": color,
                                    "fill-opacity": ".48"})
    text(svg, 255, 530, "峰值与黑位由显示器和环境决定", size=15, fill="#486581")

    rounded_box(svg, 540, 125, 420, 450, "#fff7e8", "#e8c77d", "打印",
                "减色墨层 · 反射介质", "#8a5f19", 22)
    SubElement(svg, "rect", {"x": "645", "y": "285", "width": "210", "height": "210",
                              "fill": "#f4efe1", "stroke": "#d5c8aa", "stroke-width": "3"})
    for y, color, op in ((325, "#00a7c4", .52), (370, "#d23c8a", .48), (415, "#e7c441", .55)):
        SubElement(svg, "rect", {"x": "680", "y": str(y), "width": "140", "height": "38",
                                  "fill": color, "fill-opacity": str(op)})
    text(svg, 750, 530, "纸白、墨黑、表面与观察光共同决定", size=15, fill="#486581")

    rounded_box(svg, 1035, 125, 420, 450, "#edf8f2", "#9fd6b7", "软打样",
                "源图 → 打印配置 → 模拟显示", "#397456", 22)
    steps = [(1090, 285, "源色"), (1215, 285, "映射"), (1340, 285, "预览")]
    colors = ["#3b82b5", "#c58a2d", "#4d8c6a"]
    for (x, y, label), color in zip(steps, colors):
        SubElement(svg, "circle", {"cx": str(x), "cy": str(y), "r": "38", "fill": color,
                                    "fill-opacity": ".78"})
        text(svg, x, y + 75, label, size=15, weight="700", fill=color)
    line(svg, 1130, 285, 1170, 285, stroke="#527da3", width=3, marker="arrow-blue")
    line(svg, 1255, 285, 1295, 285, stroke="#527da3", width=3, marker="arrow-blue")
    text(svg, 1245, 405, "纸张配置 + 渲染意图\n黑点补偿 + 观看光", size=16, fill="#486581")
    rounded_box(svg, 230, 685, 1040, 68, "#fff0f3", "#eab0be",
                "软打样只能在已校准屏幕上近似打印外观；最终纸张、墨水和照明仍需实样验证",
                None, "#a24862", 18)
    ElementTree(svg).write(SVG_DIR / "screen_print_mapping.svg", encoding="utf-8",
                           xml_declaration=True)


def jpeg_delivery_pipeline():
    width, height = 1500, 800
    svg = base_svg(width, height, "JPEG压缩交付与平台二次处理链")
    text(svg, 750, 43, "交付文件会经历颜色变换、降采样、量化与平台重编码；每一步伪影不同",
         size=30, weight="700", fill="#102a43")
    stages = [
        (35, "RGB", "目标尺寸\n已完成锐化", "#eaf4ff", "#9bc7ee"),
        (265, "YCbCr", "亮度/色度\n坐标变换", "#edf8f2", "#9fd6b7"),
        (495, "色度子采样", "4:4:4 / 4:2:2\n4:2:0", "#fff7e8", "#e8c77d"),
        (725, "8×8 DCT", "空间块 →\n频率系数", "#f7efff", "#c9a9e8"),
        (955, "量化", "高频精度下降\n主要有损步骤", "#fff0f3", "#eab0be"),
        (1185, "熵编码", "无损打包\n生成 JPEG", "#eef5fb", "#a8c8e0"),
    ]
    for x0, title_value, subtitle, fill, stroke in stages:
        rounded_box(svg, x0, 135, 190, 165, fill, stroke, title_value, None, title_size=18)
        a, b = subtitle.split("\n")
        text(svg, x0 + 95, 238, a, size=14, fill="#486581")
        text(svg, x0 + 95, 265, b, size=14, fill="#486581")
    for x1, x2 in ((225, 255), (455, 485), (685, 715), (915, 945), (1145, 1175)):
        line(svg, x1, 218, x2, 218, stroke="#527da3", width=3, marker="arrow-blue")
    artifacts = [
        (145, "颜色边缘变软", "子采样"),
        (440, "块效应", "粗量化 + 低码率"),
        (735, "振铃 / 蚊噪", "高频系数丢失"),
        (1030, "渐变断层", "量化 + 再处理"),
    ]
    for x0, title_value, subtitle in artifacts:
        rounded_box(svg, x0, 405, 260, 120, "#ffffff", "#b9c7d3", title_value, subtitle,
                    title_size=18)
    rounded_box(svg, 365, 610, 770, 95, "#fff7e8", "#e8c77d", "平台二次处理",
                "重缩放 · 去除配置文件 · 再压缩 · HDR/SDR 映射 · 缩略图缓存", "#8a5f19", 19)
    line(svg, 1280, 300, 1040, 595, stroke="#c58a2d", width=4, marker="arrow-gold")
    rounded_box(svg, 270, 735, 960, 45, "#fff0f3", "#eab0be",
                "母版保留余量；交付版本只为一个已知接口优化，避免反复 JPEG 重存",
                None, "#a24862", 17)
    ElementTree(svg).write(SVG_DIR / "jpeg_delivery_pipeline.svg", encoding="utf-8",
                           xml_declaration=True)


def archive_layers_integrity():
    width, height = 1500, 810
    svg = base_svg(width, height, "影像归档的内容层校验副本与迁移")
    text(svg, 750, 43, "归档目标不是“硬盘里还有文件”，而是未来仍能验证、解释与重建",
         size=30, weight="700", fill="#102a43")
    layers = [
        (115, "原始观测", "RAW / 原视频 / 音频\n相机元数据与原始校验", "#eaf4ff", "#9bc7ee"),
        (245, "决策记录", "目录、评分、编辑参数\n颜色配置、软件与版本", "#edf8f2", "#9fd6b7"),
        (375, "固定母版", "高质量渲染\n开放或广泛支持格式", "#fff7e8", "#e8c77d"),
        (505, "交付版本", "网页、打印、客户文件\n尺寸与用途说明", "#f7efff", "#c9a9e8"),
    ]
    for y, title_value, subtitle, fill, stroke in layers:
        rounded_box(svg, 85, y, 660, 100, fill, stroke, title_value, None, title_size=19)
        a, b = subtitle.split("\n")
        text(svg, 415, y + 63, a, size=14, fill="#486581")
        text(svg, 415, y + 86, b, size=14, fill="#486581")
    rounded_box(svg, 860, 115, 500, 120, "#fff0f3", "#eab0be", "完整性",
                "密码学校验值：发现静默损坏与传输错误", "#a24862", 20)
    rounded_box(svg, 860, 285, 500, 120, "#eaf4ff", "#9bc7ee", "冗余",
                "不同介质、不同地点、独立故障域的多副本", "#285b7a", 20)
    rounded_box(svg, 860, 455, 500, 120, "#edf8f2", "#9fd6b7", "可解释性",
                "格式、配置、元数据、说明与必要的软件环境", "#397456", 20)
    rounded_box(svg, 860, 625, 500, 120, "#fff7e8", "#e8c77d", "迁移与演练",
                "定期复核、换介质、抽样恢复并记录结果", "#8a5f19", 20)
    for y in (235, 405, 575):
        line(svg, 1110, y, 1110, y + 35, stroke="#527da3", width=3, marker="arrow-blue")
    rounded_box(svg, 210, 735, 520, 46, "#ffffff", "#b9c7d3",
                "目录便于查找；校验、副本和迁移才防止丢失",
                None, "#334e68", 16)
    ElementTree(svg).write(SVG_DIR / "archive_layers_integrity.svg", encoding="utf-8",
                           xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    color_management_chain()
    display_environment_calibration()
    screen_print_mapping()
    jpeg_delivery_pipeline()
    archive_layers_integrity()


if __name__ == "__main__":
    main()
