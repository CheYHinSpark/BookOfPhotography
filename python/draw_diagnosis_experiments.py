from pathlib import Path
from xml.etree.ElementTree import ElementTree, SubElement

from draw_raw_pipeline import base_svg, line, rounded_box, text


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"


def diagnosis_cycle():
    width, height = 1500, 820
    svg = base_svg(width, height, "照片质量诊断的症状假设实验与决策闭环")
    text(svg, 750, 43, "先找伪影首次出现的位置，再改变一个变量验证；修图不是诊断的第一步",
         size=30, weight="700", fill="#102a43")
    stages = [
        (55, "定义症状", "在最终尺寸描述\n位置、方向、尺度", "#eaf4ff", "#9bc7ee"),
        (345, "定位阶段", "原始数据 → 中间结果\n→ 交付与观看", "#edf8f2", "#9fd6b7"),
        (635, "提出假设", "只保留能解释证据的\n两三个候选原因", "#fff7e8", "#e8c77d"),
        (925, "最小实验", "固定其余条件\n重复采样并留记录", "#f7efff", "#c9a9e8"),
        (1215, "处理或重拍", "按信息是否仍存在\n选择可逆动作", "#fff0f3", "#eab0be"),
    ]
    for x0, title_value, subtitle, fill, stroke in stages:
        rounded_box(svg, x0, 180, 230, 180, fill, stroke, title_value, None, title_size=20)
        a, b = subtitle.split("\n")
        text(svg, x0 + 115, 282, a, size=14, fill="#486581")
        text(svg, x0 + 115, 310, b, size=14, fill="#486581")
    for x1, x2 in ((285, 335), (575, 625), (865, 915), (1155, 1205)):
        line(svg, x1, 270, x2, 270, stroke="#527da3", width=4, marker="arrow-blue")

    rounded_box(svg, 145, 485, 340, 145, "#ffffff", "#b9c7d3", "证据",
                "RAW / 参数 / 中间导出\n目标平台下载文件 / 实际打印", "#334e68", 19)
    rounded_box(svg, 580, 485, 340, 145, "#ffffff", "#b9c7d3", "控制",
                "同一场景与输出\n一次只改一个自变量", "#334e68", 19)
    rounded_box(svg, 1015, 485, 340, 145, "#ffffff", "#b9c7d3", "判据",
                "先写预期，再看片\n用多张样本与效应大小", "#334e68", 19)
    line(svg, 1315, 360, 1315, 435, stroke="#a24862", width=4)
    line(svg, 1315, 435, 185, 435, stroke="#a24862", width=4)
    line(svg, 185, 435, 185, 167, stroke="#a24862", width=4, marker="arrow-purple")
    rounded_box(svg, 245, 715, 1010, 55, "#fff7e8", "#e8c77d",
                "若实验结果与预测不符，更新模型；不要靠挑一张样片保护原假设",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "diagnosis_cycle.svg", encoding="utf-8",
                           xml_declaration=True)


def symptom_cause_matrix():
    width, height = 1500, 900
    svg = base_svg(width, height, "照片症状与成像阶段原因矩阵")
    text(svg, 750, 43, "同一种症状可由不同阶段产生；交叉格是候选假设，不是自动结论",
         size=30, weight="700", fill="#102a43")
    x0, y0 = 310, 155
    col_w, row_h = 205, 92
    cols = ["几何与运动", "光学与对焦", "曝光与传感器", "计算处理", "输出与观看"]
    rows = ["虚：边缘不清", "糊或变形", "噪或脏", "高光无层次", "色彩异常", "细节不自然"]
    for j, label in enumerate(cols):
        rounded_box(svg, x0 + j * col_w, 95, col_w - 10, 55, "#eef5fb", "#a8c8e0",
                    label, None, title_size=15)
    row_colors = ["#eaf4ff", "#edf8f2", "#fff7e8", "#fff0f3", "#f7efff", "#eef5fb"]
    for i, (label, fill) in enumerate(zip(rows, row_colors)):
        rounded_box(svg, 45, y0 + i * row_h, 240, row_h - 12, fill, "#b9c7d3",
                    label, None, title_size=16)
        for j in range(5):
            SubElement(svg, "rect", {
                "x": str(x0 + j * col_w), "y": str(y0 + i * row_h),
                "width": str(col_w - 10), "height": str(row_h - 12), "rx": "9",
                "fill": "#ffffff", "stroke": "#d5dee6", "stroke-width": "2",
            })

    labels = {
        (0, 0): "视点变化", (0, 1): "失焦·像差\n景深·衍射", (0, 2): "低信噪比", (0, 3): "降噪·缩放", (0, 4): "观看倍率",
        (1, 0): "相机/主体运动\n滚动快门", (1, 1): "防抖耦合", (1, 3): "配准错误", (1, 4): "播放插值",
        (2, 2): "光子·读出\n暗电流", (2, 3): "提亮·去马赛克\n压缩", (2, 4): "显示黑位",
        (3, 1): "眩光", (3, 2): "满阱/通道剪切", (3, 3): "色调映射", (3, 4): "峰值受限",
        (4, 1): "光谱与镀膜", (4, 2): "白平衡基准", (4, 3): "配置/变换错误", (4, 4): "设备与环境",
        (5, 0): "混叠", (5, 1): "像差结构", (5, 2): "采样相位", (5, 3): "锐化·AI\nJPEG", (5, 4): "缩放算法",
    }
    palette = ["#3b82b5", "#4d8c6a", "#c58a2d", "#7b4b74", "#a24862"]
    for (i, j), label in labels.items():
        cx = x0 + j * col_w + (col_w - 10) / 2
        cy = y0 + i * row_h + (row_h - 12) / 2
        SubElement(svg, "circle", {"cx": str(cx - 66), "cy": str(cy), "r": "6",
                                     "fill": palette[j]})
        parts = label.split("\n")
        if len(parts) == 1:
            text(svg, cx + 6, cy + 6, parts[0], size=13, fill="#334e68")
        else:
            text(svg, cx + 6, cy - 5, parts[0], size=12, fill="#334e68")
            text(svg, cx + 6, cy + 16, parts[1], size=12, fill="#334e68")
    rounded_box(svg, 270, 775, 960, 72, "#fff7e8", "#e8c77d",
                "从 RAW 到最终介质逐级比较：首次出现差异的阶段，通常比症状名称更有诊断力",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "symptom_cause_matrix.svg", encoding="utf-8",
                           xml_declaration=True)


def six_minimal_experiments():
    width, height = 1500, 910
    svg = base_svg(width, height, "六个摄影最小实验的控制变量与证据")
    text(svg, 750, 43, "每个实验只回答一个问题：固定什么、改变什么、用什么证据判定",
         size=30, weight="700", fill="#102a43")
    cards = [
        (65, 120, "1 透视", "固定机位换焦距并裁切\n再移动机位保持主体大小", "比例与遮挡关系", "#eaf4ff", "#9bc7ee"),
        (530, 120, "2 光圈", "固定场景、对焦、输出\n只改变 f 数", "焦点/前后景/边角", "#edf8f2", "#9fd6b7"),
        (995, 120, "3 运动", "固定速度或快门\n防抖各拍一组", "拖影方向与命中率", "#fff7e8", "#e8c77d"),
        (65, 465, "4 曝光与 ISO", "先固定光子量改 ISO\n再固定 ISO 改光子量", "RAW 余量与归一化噪声", "#fff0f3", "#eab0be"),
        (530, 465, "5 RAW / JPEG", "同一次曝光双格式\n统一白平衡与最终尺寸", "恢复余量与已固化处理", "#f7efff", "#c9a9e8"),
        (995, 465, "6 后期顺序", "同一 RAW 建处理分支\n统一交付尺寸与介质", "伪影首次出现的位置", "#eef5fb", "#a8c8e0"),
    ]
    for x, y, title_value, control, evidence, fill, stroke in cards:
        rounded_box(svg, x, y, 405, 285, fill, stroke, title_value, None, title_size=21)
        c1, c2 = control.split("\n")
        text(svg, x + 202, y + 115, "控制 / 变量", size=14, weight="700", fill="#627d98")
        text(svg, x + 202, y + 150, c1, size=15, fill="#334e68")
        text(svg, x + 202, y + 179, c2, size=15, fill="#334e68")
        line(svg, x + 58, y + 205, x + 347, y + 205, stroke="#b9c7d3", width=2)
        text(svg, x + 202, y + 238, "判据：" + evidence, size=14, weight="700", fill="#486581")
    rounded_box(svg, 245, 820, 1010, 52, "#fff7e8", "#e8c77d",
                "先记录预测与失败条件；重复样本、相同输出、保留原始文件和拍摄参数",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "six_minimal_experiments.svg", encoding="utf-8",
                           xml_declaration=True)


def evidence_chain():
    width, height = 1500, 810
    svg = base_svg(width, height, "照片质量诊断的证据链与首次分歧原则")
    text(svg, 750, 43, "保存中间状态，把“看起来不好”变成可定位的首次分歧",
         size=30, weight="700", fill="#102a43")
    stages = [
        (40, "现场与设置", "光源·机位·主体\n拍摄参数与重复样本", "#eaf4ff", "#9bc7ee"),
        (330, "原始观测", "RAW 数据·通道直方图\n传感器元数据", "#edf8f2", "#9fd6b7"),
        (620, "中间状态", "去马赛克·降噪·色调\n遮罩与锐化分支", "#fff7e8", "#e8c77d"),
        (910, "交付文件", "尺寸·配置·编码\n平台下载回看", "#f7efff", "#c9a9e8"),
        (1200, "实际观看", "显示器/纸张·环境光\n观看距离与适应", "#fff0f3", "#eab0be"),
    ]
    for x, title_value, subtitle, fill, stroke in stages:
        rounded_box(svg, x, 190, 250, 180, fill, stroke, title_value, None, title_size=19)
        a, b = subtitle.split("\n")
        text(svg, x + 125, 293, a, size=14, fill="#486581")
        text(svg, x + 125, 321, b, size=14, fill="#486581")
    for x1, x2 in ((290, 320), (580, 610), (870, 900), (1160, 1190)):
        line(svg, x1, 280, x2, 280, stroke="#527da3", width=4, marker="arrow-blue")
    rounded_box(svg, 190, 505, 430, 120, "#ffffff", "#b9c7d3", "向前追溯",
                "最终异常 → 交付 → 中间状态 → RAW → 现场", "#334e68", 18)
    rounded_box(svg, 880, 505, 430, 120, "#ffffff", "#b9c7d3", "向后验证",
                "替换单一阶段，再按相同目标重新输出", "#334e68", 18)
    line(svg, 620, 565, 865, 565, stroke="#7b4b74", width=4, marker="arrow-purple")
    rounded_box(svg, 260, 700, 980, 55, "#fff7e8", "#e8c77d",
                "若 RAW 已剪切或运动细节从未记录，后期只能重建外观，不能恢复唯一真实值",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "evidence_chain.svg", encoding="utf-8",
                           xml_declaration=True)


def complete_imaging_chain():
    width, height = 1500, 850
    svg = base_svg(width, height, "从场景到观看的完整摄影质量链与不可逆损失")
    text(svg, 750, 43, "照片质量是整条链对光、空间、时间、容量与观看目标的共同分配",
         size=30, weight="700", fill="#102a43")
    stages = [
        (35, "场景与光", "光子·光谱\n方向·时刻", "#eaf4ff", "#9bc7ee"),
        (240, "几何与时间", "机位·视角\n运动·快门", "#edf8f2", "#9fd6b7"),
        (445, "光学", "聚焦·像差\n衍射·眩光", "#fff7e8", "#e8c77d"),
        (650, "传感器", "采样·满阱\n噪声·读出", "#fff0f3", "#eab0be"),
        (855, "计算", "重建·色调\n降噪·锐化", "#f7efff", "#c9a9e8"),
        (1060, "输出", "尺寸·色彩\n压缩·介质", "#eef5fb", "#a8c8e0"),
        (1265, "观看", "环境·距离\n注意与目的", "#edf8f2", "#9fd6b7"),
    ]
    for x, title_value, subtitle, fill, stroke in stages:
        rounded_box(svg, x, 155, 170, 180, fill, stroke, title_value, None, title_size=18)
        a, b = subtitle.split("\n")
        text(svg, x + 85, 257, a, size=13, fill="#486581")
        text(svg, x + 85, 284, b, size=13, fill="#486581")
    for x1, x2 in ((205, 230), (410, 435), (615, 640), (820, 845), (1025, 1050), (1230, 1255)):
        line(svg, x1, 245, x2, 245, stroke="#527da3", width=4, marker="arrow-blue")

    losses = [
        (260, "视点错过\n瞬间未捕获"), (465, "严重失焦\n频率被抑制"),
        (670, "饱和剪切\n混叠与坏点"), (875, "过强先验\n伪细节固化"),
        (1080, "色域裁切\n重压缩"),
    ]
    for x, label in losses:
        rounded_box(svg, x, 435, 170, 95, "#fff0f3", "#eab0be", "不可逆风险", label,
                    "#a24862", 14)
        line(svg, x + 85, 335, x + 85, 425, stroke="#a24862", width=3, marker="arrow-purple")

    rounded_box(svg, 75, 645, 410, 115, "#eaf4ff", "#9bc7ee", "拍摄端",
                "改变光、机位、时刻和曝光，让信息真正进入系统", "#285b7a", 18)
    rounded_box(svg, 545, 645, 410, 115, "#f7efff", "#c9a9e8", "处理端",
                "利用冗余与模型分配余量，同时标记不确定性", "#7b4b74", 18)
    rounded_box(svg, 1015, 645, 410, 115, "#edf8f2", "#9fd6b7", "输出端",
                "面向介质和观看者优化，并保留可重建母版", "#397456", 18)
    rounded_box(svg, 270, 790, 960, 42, "#fff7e8", "#e8c77d",
                "最优动作总在当前瓶颈处；一个环节的富余不能补偿另一环节已经丢失的信息",
                None, "#8a5f19", 17)
    ElementTree(svg).write(SVG_DIR / "complete_imaging_chain.svg", encoding="utf-8",
                           xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    diagnosis_cycle()
    symptom_cause_matrix()
    six_minimal_experiments()
    evidence_chain()
    complete_imaging_chain()


if __name__ == "__main__":
    main()
