from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "svg" / "forward_model.svg"

WIDTH, HEIGHT = 1200, 400


def add_text(parent, x, y, text, size=25, weight="400", fill="#16324f", anchor="middle"):
    node = SubElement(
        parent,
        "text",
        {
            "x": str(x),
            "y": str(y),
            "text-anchor": anchor,
            "font-family": "Source Han Sans SC, Microsoft YaHei, sans-serif",
            "font-size": str(size),
            "font-weight": weight,
            "fill": fill,
        },
    )
    node.text = text
    return node


def rounded_box(parent, x, y, w, h, fill, stroke, title, lines):
    SubElement(
        parent,
        "rect",
        {
            "x": str(x),
            "y": str(y),
            "width": str(w),
            "height": str(h),
            "rx": "18",
            "fill": fill,
            "stroke": stroke,
            "stroke-width": "2.5",
        },
    )
    add_text(parent, x + w / 2, y + 45, title, size=24, weight="600", fill="#102a43")
    for idx, line in enumerate(lines):
        add_text(parent, x + w / 2, y + 85 + idx * 30, line, size=22, fill="#486581")


def arrow(parent, x1, y1, x2, y2, dashed=False, color="#527da3"):
    attrs = {
        "x1": str(x1),
        "y1": str(y1),
        "x2": str(x2),
        "y2": str(y2),
        "stroke": color,
        "stroke-width": "3",
        "marker-end": "url(#arrowhead)",
    }
    if dashed:
        attrs["stroke-dasharray"] = "10 8"
    SubElement(parent, "line", attrs)


def main():
    svg = Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(WIDTH),
            "height": str(HEIGHT),
            "viewBox": f"0 0 {WIDTH} {HEIGHT}",
            "role": "img",
            "aria-label": "摄影系统从场景到视觉解释的前向模型",
        },
    )
    defs = SubElement(svg, "defs")
    marker = SubElement(
        defs,
        "marker",
        {
            "id": "arrowhead",
            "markerWidth": "10",
            "markerHeight": "8",
            "refX": "9",
            "refY": "4",
            "orient": "auto",
            "markerUnits": "strokeWidth",
        },
    )
    SubElement(marker, "path", {"d": "M 0 0 L 10 4 L 0 8 z", "fill": "#527da3"})

    add_text(svg, 600, 30, "摄影系统：从世界到有限观测", size=28, weight="600", fill="#102a43")

    xs = [80, 300, 520, 740, 960]
    w, y, h = 160, 60, 140
    boxes = [
        ("场景", ["几何 · 材料", "照明 · 运动"], "#eaf4ff", "#9bc7ee"),
        ("光场", ["位置 · 方向", "波长 · 时间"], "#edf8f2", "#9fd6b7"),
        ("光学系统", ["投影 · 孔径", "像差 · 衍射"], "#fff7e8", "#e9c784"),
        ("传感与计算", ["积分 · 噪声", "采样 · 映射"], "#f7efff", "#c9a9e8"),
        ("图像与观看", ["显示 · 适应", "识别 · 解释"], "#fff0f3", "#eab0be"),
    ]
    for x, (title, lines, fill, stroke) in zip(xs, boxes):
        rounded_box(svg, x, y, w, h, fill, stroke, title, lines)

    for left, right in zip(xs[:-1], xs[1:]):
        arrow(svg, left + w + 4, y + h / 2, right - 5, y + h / 2)

    add_text(svg, 600, 250, "前向问题：给定场景与系统，预测观测", size=22, weight="600", fill="#3d6f99")
    arrow(svg, 1080, 280, 120, 280, dashed=True, color="#527da3")
    add_text(svg, 600, 320, "逆问题：由有限图像推断场景；通常不唯一，需要先验", size=22, weight="600", fill="#7b4b74")
    add_text(svg, 600, 360, "每一次曝光都同时进行选择、积分、采样与损失", size=20, fill="#627d98")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ElementTree(svg).write(OUTPUT, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
