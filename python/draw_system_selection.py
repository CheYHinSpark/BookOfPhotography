from pathlib import Path
from xml.etree.ElementTree import SubElement, ElementTree

from draw_raw_pipeline import base_svg, text, line, rounded_box, axes, polyline


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"


def task_requirements():
    width, height = 1500, 790
    svg = base_svg(width, height, "从摄影任务到相机系统约束")
    text(svg, 750, 43, "先定义任务，再把场景与交付条件翻译为可测系统需求",
         size=30, weight="700", fill="#102a43")
    rounded_box(svg, 45, 275, 230, 190, "#eaf4ff", "#9bc7ee", "摄影任务",
                "人物 · 城市 · 旅行\n夜景 · 视频 · 打印", "#285b7a", 23)
    conditions = [
        (380, 105, "输出", "尺寸 · 观看距离\n色彩一致性"),
        (380, 260, "光线", "照度 · 动态范围\n允许补光"),
        (380, 415, "运动", "主体速度 · 相机运动\n事件持续时间"),
        (380, 570, "现场", "工作距离 · 重量\n天气 · 交付速度"),
    ]
    for x0, y0, title_value, subtitle in conditions:
        rounded_box(svg, x0, y0, 310, 115, "#ffffff", "#b9c7d3", title_value, None,
                    title_size=19)
        a, b = subtitle.split("\n")
        text(svg, x0 + 155, y0 + 75, a, size=14, fill="#486581")
        text(svg, x0 + 155, y0 + 99, b, size=14, fill="#486581")
        line(svg, 275, 370, x0 - 15, y0 + 58, stroke="#527da3", width=3,
             marker="arrow-blue")
    rounded_box(svg, 810, 145, 295, 470, "#edf8f2", "#9fd6b7", "系统需求",
                "视角范围\n入瞳与快门\n对焦与读出\n分辨率与噪声\n操作与可靠性",
                "#397456", 23)
    line(svg, 690, 370, 795, 370, stroke="#4d8c6a", width=5, marker="arrow-green")
    rounded_box(svg, 1215, 235, 240, 275, "#fff7e8", "#e8c77d", "可接受方案集",
                "满足硬约束\n比较软偏好\n保留余量",
                "#8a5f19", 22)
    line(svg, 1105, 370, 1200, 370, stroke="#c58a2d", width=5, marker="arrow-gold")
    rounded_box(svg, 275, 710, 950, 50, "#fff0f3", "#eab0be",
                "品牌与型号只在最后一步进入；任务定义改变，最优解也会改变",
                None, "#a24862", 17)
    ElementTree(svg).write(SVG_DIR / "task_requirements.svg", encoding="utf-8",
                           xml_declaration=True)


def system_bottleneck_budget():
    width, height = 1500, 790
    svg = base_svg(width, height, "摄影系统质量预算与瓶颈")
    text(svg, 750, 43, "最终质量由整条链共同决定：强项不能自动补偿已经丢失的信息",
         size=30, weight="700", fill="#102a43")
    stages = [
        (35, "场景", "光子 · 运动", "#eaf4ff", "#9bc7ee"),
        (285, "镜头", "视角 · 入瞳 · MTF", "#edf8f2", "#9fd6b7"),
        (535, "传感器", "采样 · 满阱 · 读出", "#fff7e8", "#e8c77d"),
        (785, "计算", "对齐 · 降噪 · 色调", "#f7efff", "#c9a9e8"),
        (1035, "输出", "尺寸 · 介质 · 压缩", "#fff0f3", "#eab0be"),
        (1285, "观看", "距离 · 环境 · 任务", "#eef5fb", "#a8c8e0"),
    ]
    for x0, title_value, subtitle, fill, stroke in stages:
        rounded_box(svg, x0, 155, 180, 145, fill, stroke, title_value, subtitle, title_size=19)
    for x1, x2 in ((215, 275), (465, 525), (715, 775), (965, 1025), (1215, 1275)):
        line(svg, x1, 228, x2, 228, stroke="#527da3", width=4, marker="arrow-blue")

    # quality bars
    labels = [("空间细节", [0.95, .72, .62, .66, .55, .55]),
              ("信噪比", [.42, .55, .68, .78, .70, .70]),
              ("时间一致性", [.62, .62, .58, .38, .38, .38])]
    colors = ["#3b82b5", "#4d8c6a", "#c85b73"]
    for row, ((label, vals), color) in enumerate(zip(labels, colors)):
        y = 410 + row * 92
        text(svg, 65, y + 24, label, size=18, weight="700", fill=color, anchor="start")
        for k, val in enumerate(vals):
            x = 210 + k * 200
            SubElement(svg, "rect", {"x": str(x), "y": str(y), "width": "150", "height": "34",
                                      "rx": "7", "fill": "#e5edf3"})
            SubElement(svg, "rect", {"x": str(x), "y": str(y), "width": str(150 * val),
                                      "height": "34", "rx": "7", "fill": color,
                                      "fill-opacity": ".78"})
    rounded_box(svg, 250, 705, 1000, 52, "#ffffff", "#b9c7d3",
                "不同质量维度有不同瓶颈；不存在一个“总画质分”能替代任务权重",
                None, "#334e68", 18)
    ElementTree(svg).write(SVG_DIR / "system_bottleneck_budget.svg", encoding="utf-8",
                           xml_declaration=True)


def body_metric_meaning():
    width, height = 1500, 810
    svg = base_svg(width, height, "相机机身指标的任务意义与代价")
    text(svg, 750, 43, "机身规格只有放进场景、镜头与输出条件后才变成摄影能力",
         size=30, weight="700", fill="#102a43")
    rows = [
        ("传感器面积", "同视角与 f 数下更多总光；景深选择", "镜头体积、成本、读出面积"),
        ("像素数", "采样、裁切与大输出余量", "数据量；需镜头与稳定性兑现"),
        ("动态范围", "单次曝光保高光与阴影", "依 ISO、阈值与输出定义"),
        ("读出速度", "连拍、视频、滚动快门与黑屏", "噪声、位深、发热和数据率交换"),
        ("自动对焦", "事件捕获与主体跟踪", "依镜头、光线、题材与设置"),
        ("防抖", "降低相机运动导致的模糊", "不冻结主体；成功率而非保证值"),
        ("操作与可靠性", "响应、续航、耐候与重复工作", "重量、学习成本与维护"),
    ]
    text(svg, 165, 115, "指标", size=20, weight="700", fill="#285b7a")
    text(svg, 665, 115, "可能带来的能力", size=20, weight="700", fill="#397456")
    text(svg, 1190, 115, "条件与代价", size=20, weight="700", fill="#8a5f19")
    for i, (metric, benefit, cost) in enumerate(rows):
        y = 145 + i * 82
        fill = "#f7fafc" if i % 2 == 0 else "#eef4f8"
        SubElement(svg, "rect", {"x": "55", "y": str(y), "width": "1390", "height": "68",
                                  "rx": "8", "fill": fill})
        text(svg, 165, y + 42, metric, size=18, weight="700", fill="#285b7a")
        text(svg, 665, y + 42, benefit, size=16, fill="#397456")
        text(svg, 1190, y + 42, cost, size=16, fill="#8a5f19")
    rounded_box(svg, 270, 745, 960, 46, "#fff0f3", "#eab0be",
                "规格描述潜力；命中率、携带率与工作流决定潜力能否变成照片",
                None, "#a24862", 17)
    ElementTree(svg).write(SVG_DIR / "body_metric_meaning.svg", encoding="utf-8",
                           xml_declaration=True)


def lens_parameter_space():
    width, height = 1500, 800
    svg = base_svg(width, height, "镜头选择的参数空间与任务约束")
    text(svg, 750, 43, "镜头不是一个锐度数字：视角、入瞳、距离、成像与操作共同构成解",
         size=30, weight="700", fill="#102a43")
    rounded_box(svg, 45, 255, 250, 210, "#eaf4ff", "#9bc7ee", "题材与机位",
                "要站在哪里？\n要包含多少环境？", "#285b7a", 22)
    params = [
        (410, 105, "视角 / 焦距", "决定取景范围；机位决定透视"),
        (410, 270, "最大入瞳 D=f/N", "光子、景深、对焦与体积"),
        (410, 435, "工作距离 / 最近对焦", "遮挡、放大率与沟通空间"),
        (410, 600, "MTF / 像差 / 眩光", "随光圈、焦距、距离和像高变化"),
    ]
    for x0, y0, title_value, subtitle in params:
        rounded_box(svg, x0, y0, 400, 120, "#ffffff", "#b9c7d3", title_value, subtitle,
                    title_size=19)
        line(svg, 295, 360, x0 - 15, y0 + 60, stroke="#527da3", width=3,
             marker="arrow-blue")
    rounded_box(svg, 930, 155, 480, 185, "#edf8f2", "#9fd6b7", "定焦",
                "更少焦段自由度；可换取体积、入瞳、校正或操作一致性", "#397456", 20)
    rounded_box(svg, 930, 420, 480, 185, "#fff7e8", "#e8c77d", "变焦",
                "快速改变视角；光圈、成像与体积在范围内共同折中", "#8a5f19", 20)
    rounded_box(svg, 315, 745, 870, 45, "#fff0f3", "#eab0be",
                "定焦与变焦是不同约束解，不是天然的画质等级",
                None, "#a24862", 17)
    ElementTree(svg).write(SVG_DIR / "lens_parameter_space.svg", encoding="utf-8",
                           xml_declaration=True)


def system_crossovers():
    width, height = 1500, 810
    svg = base_svg(width, height, "手机可换镜头系统与中画幅的交叉优势")
    text(svg, 750, 43, "系统优势会随照度、运动、输出和携带约束交叉，不形成永恒等级",
         size=30, weight="700", fill="#102a43")
    systems = [
        ("手机", "#3b82b5", [0.95, .82, .58, .50, .72]),
        ("可换镜头系统", "#4d8c6a", [.65, .78, .88, .84, .82]),
        ("中画幅", "#c58a2d", [.38, .48, .72, .95, .70]),
    ]
    criteria = ["随身与响应", "计算融合", "弱光/运动", "大输出余量", "镜头与控制"]
    text(svg, 170, 115, "任务维度", size=20, weight="700", fill="#334e68")
    for idx, (name, color, _) in enumerate(systems):
        text(svg, 570 + idx * 300, 115, name, size=20, weight="700", fill=color)
    for row, criterion in enumerate(criteria):
        y = 155 + row * 105
        fill = "#f7fafc" if row % 2 == 0 else "#eef4f8"
        SubElement(svg, "rect", {"x": "55", "y": str(y), "width": "1390", "height": "82",
                                  "rx": "9", "fill": fill})
        text(svg, 170, y + 50, criterion, size=18, weight="700", fill="#334e68")
        for idx, (_, color, vals) in enumerate(systems):
            x = 455 + idx * 300
            SubElement(svg, "rect", {"x": str(x), "y": str(y + 25), "width": "220", "height": "32",
                                      "rx": "7", "fill": "#dfe7ee"})
            SubElement(svg, "rect", {"x": str(x), "y": str(y + 25),
                                      "width": str(220 * vals[row]), "height": "32",
                                      "rx": "7", "fill": color, "fill-opacity": ".78"})
    rounded_box(svg, 240, 720, 1020, 58, "#ffffff", "#b9c7d3",
                "条长只是关系示意，不是跨型号实测分数；具体技术代际可改变交叉点",
                None, "#334e68", 18)
    ElementTree(svg).write(SVG_DIR / "system_crossovers.svg", encoding="utf-8",
                           xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    task_requirements()
    system_bottleneck_budget()
    body_metric_meaning()
    lens_parameter_space()
    system_crossovers()


if __name__ == "__main__":
    main()
