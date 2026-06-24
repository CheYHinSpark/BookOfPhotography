from pathlib import Path
from xml.etree.ElementTree import SubElement, ElementTree
import math

from draw_raw_pipeline import base_svg, text, line, polyline, rounded_box, axes


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"


def mini_grid(svg, x, y, shift_x=0, shift_y=0, accent="#3b82b5"):
    for k in range(5):
        line(svg, x + shift_x + k * 16, y + shift_y, x + shift_x + k * 16,
             y + shift_y + 64, stroke="#c7d4df", width=1.5)
        line(svg, x + shift_x, y + shift_y + k * 16, x + shift_x + 64,
             y + shift_y + k * 16, stroke="#c7d4df", width=1.5)
    SubElement(svg, "circle", {
        "cx": str(x + shift_x + 31), "cy": str(y + shift_y + 29), "r": "9",
        "fill": accent, "fill-opacity": ".86",
    })


def multiframe_forward_model():
    width, height = 1500, 790
    svg = base_svg(width, height, "多帧成像的统一前向模型与融合流程")
    text(svg, 750, 43, "多帧不是把文件叠起来：每一帧都经历不同几何、模糊、采样与噪声",
         size=30, weight="700", fill="#102a43")
    rounded_box(svg, 45, 260, 220, 180, "#eaf4ff", "#9bc7ee", "潜在场景 x",
                "共同但未知的辐射与结构", "#285b7a", 22)
    mini_grid(svg, 123, 352, accent="#3b82b5")

    frame_y = [105, 245, 385, 525]
    shifts = [(-4, 2), (2, -3), (5, 4), (-1, -5)]
    colors = ["#3b82b5", "#4d8c6a", "#c58a2d", "#7b4b74"]
    for idx, (yy, shift, color) in enumerate(zip(frame_y, shifts, colors), start=1):
        rounded_box(svg, 365, yy, 250, 105, "#ffffff", "#b9c7d3", f"第 {idx} 帧 y{idx}",
                    "W：位移　H：模糊　D：采样", title_size=18)
        mini_grid(svg, 526, yy + 27, shift[0], shift[1], accent=color)
        line(svg, 265, 350, 350, yy + 52, stroke=color, width=3, marker="arrow-blue")

    rounded_box(svg, 745, 145, 285, 430, "#edf8f2", "#9fd6b7", "配准到共同坐标",
                "估计 W⁻¹；统一曝光尺度", "#397456", 22)
    for idx, yy in enumerate((235, 315, 395, 475)):
        mini_grid(svg, 855, yy, accent=colors[idx])
    for yy in frame_y:
        line(svg, 615, yy + 52, 730, 350, stroke="#527da3", width=3, marker="arrow-blue")

    rounded_box(svg, 1130, 250, 325, 200, "#fff7e8", "#e8c77d", "融合估计结果",
                "平均 · 鲁棒权重 · 选择\n联合重建", "#8a5f19", 22)
    mini_grid(svg, 1260, 360, accent="#c58a2d")
    line(svg, 1030, 350, 1115, 350, stroke="#c58a2d", width=4, marker="arrow-gold")

    rounded_box(svg, 165, 650, 1170, 78, "#eef5fb", "#a8c8e0",
                "yᵣ = Dᵣ Hᵣ Wᵣ x + nᵣ：先说明各帧如何形成，才知道该怎样对齐和融合",
                "若主体、焦点、曝光或滚动快门改变，帧间差异不能全部塞进同一个平移量",
                "#285b7a", 19)
    ElementTree(svg).write(SVG_DIR / "multiframe_forward_model.svg", encoding="utf-8",
                           xml_declaration=True)


def averaging_limits():
    width, height = 1500, 780
    svg = base_svg(width, height, "多帧平均的信噪比收益和失效方式")
    text(svg, 750, 43, "独立噪声按 1/√N 下降；相关误差、错位和运动不会自动平均掉",
         size=30, weight="700", fill="#102a43")
    l, r, t, b = 100, 770, 135, 570
    axes(svg, l, r, t, b, "帧数 N", "输出噪声标准差")
    independent, plateau = [], []
    for j in range(1, 65):
        u = (j - 1) / 63
        x = l + u * (r - l)
        indep = 1 / math.sqrt(j)
        corr = math.sqrt((1 - .10) / j + .10)
        independent.append((x, b - indep * (b - t - 20)))
        plateau.append((x, b - corr * (b - t - 20)))
    polyline(svg, independent, stroke="#3b82b5", width=6)
    polyline(svg, plateau, stroke="#c85b73", width=6)
    line(svg, 500, 185, 570, 185, stroke="#3b82b5", width=6)
    text(svg, 590, 192, "独立噪声", size=17, weight="700", fill="#3b82b5", anchor="start")
    line(svg, 500, 230, 570, 230, stroke="#c85b73", width=6)
    text(svg, 590, 237, "含相关/固定项", size=17, weight="700", fill="#c85b73", anchor="start")
    text(svg, 140, 615, "4 帧约降 1 档标准差；16 帧约降 2 档，但帧数翻倍收益递减",
         size=16, fill="#486581", anchor="start")

    panels = [
        (875, 125, "静态且配准", "随机颗粒变细", "good"),
        (875, 330, "主体运动", "出现重影或被抹除", "motion"),
        (1180, 330, "视差 / 错配", "不同深度双边缘", "parallax"),
    ]
    for x0, y0, title_value, subtitle, mode in panels:
        w = 270 if mode == "good" else 250
        rounded_box(svg, x0, y0, w, 165, "#ffffff", "#b9c7d3", title_value, subtitle,
                    title_size=19)
        cx, cy = x0 + w / 2, y0 + 112
        if mode == "good":
            for rr, op in ((42, .08), (27, .16), (13, .68)):
                SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": str(rr),
                                            "fill": "#4d8c6a", "fill-opacity": str(op)})
        elif mode == "motion":
            for dx, op in ((-25, .35), (0, .75), (28, .35)):
                SubElement(svg, "circle", {"cx": str(cx + dx), "cy": str(cy), "r": "23",
                                            "fill": "#c85b73", "fill-opacity": str(op)})
        else:
            for dx, color in ((-18, "#3b82b5"), (18, "#7b4b74")):
                SubElement(svg, "rect", {"x": str(cx + dx - 38), "y": str(cy - 25),
                                          "width": "76", "height": "50", "rx": "7",
                                          "fill": color, "fill-opacity": ".38"})
    line(svg, 1145, 207, 1280, 310, stroke="#9ab3c6", width=3, marker="arrow-blue")
    rounded_box(svg, 915, 600, 460, 90, "#fff7e8", "#e8c77d", "平均只消除帧间变化的零均值部分",
                "固定图样、模型偏差和稳定重影会留下来", "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "averaging_limits.svg", encoding="utf-8",
                           xml_declaration=True)


def hdr_exposure_coverage():
    width, height = 1500, 790
    svg = base_svg(width, height, "包围曝光的有效测量区间与HDR融合")
    text(svg, 750, 43, "每张曝光只在一段场景亮度上既未沉入噪声、也未达到饱和",
         size=30, weight="700", fill="#102a43")
    l, r = 145, 1350
    line(svg, l, 650, r, 650, stroke="#334e68", width=3, marker="arrow-dark")
    text(svg, l, 690, "暗部", size=18, fill="#627d98", anchor="start")
    text(svg, r, 690, "亮部 / log 场景曝光", size=18, fill="#627d98", anchor="end")
    exposures = [
        (150, "长曝光", 160, 820, "#4d8c6a", "阴影 SNR 高；高光早饱和"),
        (315, "中曝光", 390, 1060, "#3b82b5", "覆盖中间调"),
        (480, "短曝光", 660, 1320, "#c58a2d", "保住高光；阴影噪声大"),
    ]
    for y, name, x1, x2, color, note in exposures:
        text(svg, 75, y + 12, name, size=20, weight="700", fill=color, anchor="start")
        # unreliable dark end, usable interval, clipped end
        SubElement(svg, "rect", {"x": str(l), "y": str(y - 20), "width": str(x1 - l),
                                  "height": "42", "rx": "8", "fill": "#dfe7ee"})
        SubElement(svg, "rect", {"x": str(x1), "y": str(y - 20), "width": str(x2 - x1),
                                  "height": "42", "rx": "8", "fill": color,
                                  "fill-opacity": ".74"})
        SubElement(svg, "rect", {"x": str(x2), "y": str(y - 20), "width": str(r - x2),
                                  "height": "42", "rx": "8", "fill": "#f3c8d2"})
        text(svg, (x1 + x2) / 2, y + 8, "可用权重高", size=16, weight="700", fill="#ffffff")
        text(svg, 750, y + 64, note, size=15, fill="#486581")
    text(svg, 255, 595, "噪声主导", size=17, weight="700", fill="#627d98")
    text(svg, 1180, 595, "饱和 / 只剩下界", size=17, weight="700", fill="#a24862")

    rounded_box(svg, 335, 720, 830, 52, "#eef5fb", "#a8c8e0",
                "融合先把各帧除以曝光尺度回到共同辐射坐标，再按可靠性选择或加权",
                None, "#285b7a", 17)
    ElementTree(svg).write(SVG_DIR / "hdr_exposure_coverage.svg", encoding="utf-8",
                           xml_declaration=True)


def multiframe_tasks():
    width, height = 1500, 800
    svg = base_svg(width, height, "多帧数据通过不同融合算子解决不同摄影问题")
    text(svg, 750, 43, "同样是一组帧，保留什么取决于融合算子：平均、选择、重建或时间统计",
         size=30, weight="700", fill="#102a43")
    cards = [
        (45, "平均 / 鲁棒平均", "目标：降低独立噪声", "静态结构相加\n异常帧降权", "#eaf4ff", "#9bc7ee", "avg"),
        (405, "HDR 融合", "目标：扩展可测亮度", "不同曝光归一\n选未饱和高 SNR", "#edf8f2", "#9fd6b7", "hdr"),
        (765, "超分辨率 / 像素位移", "目标：补充采样相位", "亚像素错位联合求解\n不突破光学零点", "#fff7e8", "#e8c77d", "sr"),
        (1125, "焦点与时间堆栈", "目标：按位置或时间选择", "清晰区域 · 中位数\n最大值 · 累积", "#f7efff", "#c9a9e8", "stack"),
    ]
    for x0, title_value, subtitle, detail, fill, stroke, mode in cards:
        rounded_box(svg, x0, 110, 330, 535, fill, stroke, title_value, subtitle, title_size=20)
        a, b = detail.split("\n")
        text(svg, x0 + 165, 238, a, size=16, weight="700", fill="#486581")
        text(svg, x0 + 165, 270, b, size=16, fill="#486581")
        if mode == "avg":
            for k, dx in enumerate((-42, -21, 0, 21, 42)):
                SubElement(svg, "circle", {"cx": str(x0 + 165 + dx), "cy": "415",
                                            "r": str(15 + (k == 2) * 4), "fill": "#3b82b5",
                                            "fill-opacity": str(.22 + .12 * (k == 2))})
            line(svg, x0 + 95, 500, x0 + 235, 500, stroke="#3b82b5", width=5,
                 marker="arrow-blue")
        elif mode == "hdr":
            for k, w in enumerate((90, 145, 210)):
                SubElement(svg, "rect", {"x": str(x0 + 60), "y": str(355 + k * 48),
                                          "width": str(w), "height": "28", "rx": "6",
                                          "fill": "#4d8c6a", "fill-opacity": str(.45 + .15*k)})
        elif mode == "sr":
            offsets = [(0, 0), (10, 0), (0, 10), (10, 10)]
            for k, (dx, dy) in enumerate(offsets):
                mini_grid(svg, x0 + 75 + (k % 2) * 100, 355 + (k // 2) * 100, dx / 3, dy / 3,
                          accent="#c58a2d")
        else:
            for k, rr in enumerate((44, 31, 18)):
                SubElement(svg, "circle", {"cx": str(x0 + 165), "cy": "420", "r": str(rr),
                                            "fill": "none", "stroke": "#7b4b74",
                                            "stroke-width": str(2 + k)})
            text(svg, x0 + 165, 535, "每个位置选择最清晰帧", size=15, fill="#7b4b74")
    rounded_box(svg, 260, 700, 980, 58, "#ffffff", "#b9c7d3",
                "若帧间场景不一致，算法必须在“保留运动”与“当作异常删除”之间作出任务选择",
                None, "#334e68", 18)
    ElementTree(svg).write(SVG_DIR / "multiframe_tasks.svg", encoding="utf-8",
                           xml_declaration=True)


def mobile_computational_pipeline():
    width, height = 1500, 790
    svg = base_svg(width, height, "手机计算摄影的多帧处理链及常见失效点")
    text(svg, 750, 43, "手机夜景与多摄融合：算法在按下快门前后组织一段时间内的观测",
         size=30, weight="700", fill="#102a43")
    blocks = [
        (35, "连续缓存", "多帧 RAW\n陀螺仪/曝光", "#eaf4ff", "#9bc7ee"),
        (285, "选参考帧", "清晰度\n表情与运动", "#edf8f2", "#9fd6b7"),
        (535, "局部配准", "全局运动\n局部光流/深度", "#fff7e8", "#e8c77d"),
        (785, "运动感知融合", "降噪/HDR\n去鬼影", "#f7efff", "#c9a9e8"),
        (1035, "颜色与色调", "白平衡\n局部映射", "#fff0f3", "#eab0be"),
        (1285, "输出", "锐化/压缩\n屏幕预览", "#eef5fb", "#a8c8e0"),
    ]
    for x0, title_value, subtitle, fill, stroke in blocks:
        rounded_box(svg, x0, 130, 180, 155, fill, stroke, title_value, None, title_size=18)
        a, b = subtitle.split("\n")
        text(svg, x0 + 90, 222, a, size=14, fill="#486581")
        text(svg, x0 + 90, 248, b, size=14, fill="#486581")
    for x1, x2 in ((215, 275), (465, 525), (715, 775), (965, 1025), (1215, 1275)):
        line(svg, x1, 207, x2, 207, stroke="#527da3", width=4, marker="arrow-blue")

    risks = [
        (120, "帧内模糊", "单帧曝光已经积分掉的细节", "#fff0f3", "#eab0be"),
        (430, "错配与鬼影", "人物、树叶、水面、滚动快门", "#fff7e8", "#e8c77d"),
        (740, "多摄视差", "近物、遮挡与镜头切换", "#f7efff", "#c9a9e8"),
        (1050, "先验边界", "头发、透明物与数字虚化", "#eaf4ff", "#9bc7ee"),
    ]
    for x0, title_value, subtitle, fill, stroke in risks:
        rounded_box(svg, x0, 420, 270, 125, fill, stroke, title_value, subtitle, title_size=18)
    line(svg, 625, 285, 565, 405, stroke="#c58a2d", width=3, marker="arrow-gold")
    line(svg, 875, 285, 875, 405, stroke="#c58a2d", width=3, marker="arrow-gold")
    line(svg, 1190, 285, 1185, 405, stroke="#c58a2d", width=3, marker="arrow-gold")
    rounded_box(svg, 250, 640, 1000, 82, "#edf8f2", "#9fd6b7",
                "成功时：时间提供更多光子、曝光区间与采样相位",
                "失败时：同一时间窗口内的变化被误判为噪声、深度或可融合结构",
                "#397456", 20)
    ElementTree(svg).write(SVG_DIR / "mobile_computational_pipeline.svg", encoding="utf-8",
                           xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    multiframe_forward_model()
    averaging_limits()
    hdr_exposure_coverage()
    multiframe_tasks()
    mobile_computational_pipeline()


if __name__ == "__main__":
    main()
