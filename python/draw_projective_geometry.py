from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
import math


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"
FONT = "Source Han Sans SC, Microsoft YaHei, sans-serif"


def text(parent, x, y, value, size=24, weight="400", fill="#243b53", anchor="middle"):
    node = SubElement(
        parent,
        "text",
        {
            "x": str(x),
            "y": str(y),
            "text-anchor": anchor,
            "font-family": FONT,
            "font-size": str(size),
            "font-weight": weight,
            "fill": fill,
        },
    )
    node.text = value
    return node


def line(parent, x1, y1, x2, y2, stroke="#527da3", width=3, dash=None, marker=None):
    attrs = {
        "x1": str(x1),
        "y1": str(y1),
        "x2": str(x2),
        "y2": str(y2),
        "stroke": stroke,
        "stroke-width": str(width),
        "stroke-linecap": "round",
    }
    if dash:
        attrs["stroke-dasharray"] = dash
    if marker:
        attrs["marker-end"] = f"url(#{marker})"
    return SubElement(parent, "line", attrs)


def polyline(parent, points, stroke="#527da3", width=2, fill="none", dash=None):
    attrs = {
        "points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points),
        "stroke": stroke,
        "stroke-width": str(width),
        "fill": fill,
        "stroke-linejoin": "round",
        "stroke-linecap": "round",
    }
    if dash:
        attrs["stroke-dasharray"] = dash
    return SubElement(parent, "polyline", attrs)


def add_defs(svg):
    defs = SubElement(svg, "defs")
    for marker_id, color in (("arrow-blue", "#3b82b5"), ("arrow-red", "#c85b73"), ("arrow-dark", "#334e68"), ("arrow-green", "#4d8c6a")):
        marker = SubElement(
            defs,
            "marker",
            {
                "id": marker_id,
                "markerWidth": "10",
                "markerHeight": "8",
                "refX": "9",
                "refY": "4",
                "orient": "auto",
                "markerUnits": "strokeWidth",
            },
        )
        SubElement(marker, "path", {"d": "M 0 0 L 10 4 L 0 8 z", "fill": color})


def base_svg(width, height, label):
    svg = Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
            "role": "img",
            "aria-label": label,
        },
    )
    add_defs(svg)
    return svg


def pinhole_projection():
    width, height = 1350, 650
    svg = base_svg(width, height, "针孔相机中心投影")
    axis_y = 330
    center_x = 520
    virtual_x = 750
    sensor_x = 270
    point_x, point_y = 1120, 115
    slope = (point_y - axis_y) / (point_x - center_x)
    virtual_y = axis_y + slope * (virtual_x - center_x)
    sensor_y = axis_y + slope * (sensor_x - center_x)

    line(svg, 90, axis_y, 1260, axis_y, stroke="#8aa2b5", width=2, marker="arrow-dark")
    text(svg, 1230, axis_y - 18, "光轴", size=22, fill="#627d98")
    line(svg, center_x, 95, center_x, 570, stroke="#334e68", width=2, dash="8 7")
    SubElement(svg, "circle", {"cx": str(center_x), "cy": str(axis_y), "r": "9", "fill": "#102a43"})
    text(svg, center_x - 35, axis_y + 34, "投影中心", size=22, weight="700")

    line(svg, virtual_x, 100, virtual_x, 560, stroke="#4d8c6a", width=4)
    text(svg, virtual_x, 88, "虚像平面", size=22, weight="700", fill="#397456")
    line(svg, sensor_x, 100, sensor_x, 560, stroke="#a24862", width=6)
    text(svg, sensor_x, 88, "真实传感器", size=22, weight="700", fill="#a24862")

    line(svg, sensor_x - 20, sensor_y, point_x, point_y, stroke="#3b82b5", width=3, marker="arrow-blue")
    SubElement(svg, "circle", {"cx": str(point_x), "cy": str(point_y), "r": "9", "fill": "#285b7a"})
    text(svg, point_x + 24, point_y + 5, "空间点", size=23, weight="700", anchor="start")
    SubElement(svg, "circle", {"cx": str(virtual_x), "cy": f"{virtual_y:.2f}", "r": "7", "fill": "#3c8d65"})
    text(svg, virtual_x + 15, virtual_y - 14, "虚像点", size=21, weight="600", fill="#397456", anchor="start")
    SubElement(svg, "circle", {"cx": str(sensor_x), "cy": f"{sensor_y:.2f}", "r": "7", "fill": "#b84e68"})
    text(svg, sensor_x - 15, sensor_y + 32, "倒像", size=22, weight="600", fill="#a24862", anchor="end")

    line(svg, center_x, 585, virtual_x, 585, stroke="#334e68", width=2)
    line(svg, center_x, 574, center_x, 596, stroke="#334e68", width=2)
    line(svg, virtual_x, 574, virtual_x, 596, stroke="#334e68", width=2)
    text(svg, (center_x + virtual_x) / 2, 618, "焦距", size=22, weight="700")
    line(svg, virtual_x + 18, axis_y, virtual_x + 18, virtual_y, stroke="#397456", width=2, dash="5 5")
    text(svg, virtual_x + 38, (axis_y + virtual_y) / 2, "像高", size=22, weight="700", fill="#397456", anchor="start")
    line(svg, point_x + 18, axis_y, point_x + 18, point_y, stroke="#285b7a", width=2, dash="5 5")
    text(svg, point_x + 38, (axis_y + point_y) / 2, "物高", size=22, weight="700", fill="#285b7a", anchor="start")
    text(svg, 930, 605, "相似三角形决定投影比例", size=22, weight="600", fill="#7b3651")

    ElementTree(svg).write(SVG_DIR / "pinhole_projection.svg", encoding="utf-8", xml_declaration=True)


def perspective_focal_distance():
    width, height = 1200, 720
    svg = base_svg(width, height, "固定机位与固定主体构图的透视比较")

    # Panel 1: fixed camera, wide frame and central crop.
    SubElement(svg, "rect", {"x": "20", "y": "20", "width": "1160", "height": "320", "rx": "20", "fill": "#f2f8fc", "stroke": "#b4cadd", "stroke-width": "2"})
    text(svg, 40, 60, "A  固定机位", size=24, weight="600", fill="#285b7a", anchor="start")
    cx, cy = 160, 240
    SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": "9", "fill": "#102a43"})
    text(svg, cx, cy + 40, "同一投影中心", size=22, weight="600")
    # Same projected image and crop.
    SubElement(svg, "rect", {"x": "640", "y": "50", "width": "500", "height": "250", "fill": "#ffffff", "stroke": "#6aa6d8", "stroke-width": "3"})
    SubElement(svg, "rect", {"x": "750", "y": "120", "width": "300", "height": "150", "fill": "none", "stroke": "#c85b73", "stroke-width": "4", "stroke-dasharray": "12 8"})
    SubElement(svg, "circle", {"cx": "900", "cy": "180", "r": "36", "fill": "#f3a9b9", "fill-opacity": "0.8"})
    SubElement(svg, "rect", {"x": "850", "y": "220", "width": "100", "height": "40", "fill": "#8ec5e8"})
    text(svg, 900, 325, "长焦图像相当于广角中央裁切后统一放大", size=22, weight="600", fill="#486581")
    line(svg, cx, cy, 640, 50, stroke="#6aa6d8", width=3)
    line(svg, cx, cy, 640, 300, stroke="#6aa6d8", width=3)
    line(svg, cx, cy, 750, 120, stroke="#c85b73", width=3)
    line(svg, cx, cy, 750, 270, stroke="#c85b73", width=3)
    text(svg, 520, 135, "广角视场", size=22, weight="600", fill="#3b82b5")
    text(svg, 540, 210, "长焦视场", size=22, weight="600", fill="#a24862")

    # Panel 2: same subject size, different distance.
    SubElement(svg, "rect", {"x": "20", "y": "360", "width": "1160", "height": "340", "rx": "20", "fill": "#fff8f2", "stroke": "#e5c3a5", "stroke-width": "2"})
    text(svg, 40, 400, "B  主体大小固定", size=24, weight="600", fill="#8b5e20", anchor="start")
    # Scene line.
    scene_y = 640
    line(svg, 100, scene_y, 1100, scene_y, stroke="#9fb3c2", width=2)
    near_cam, far_cam, subject_x, bg_x = 160, 400, 750, 1000
    subject_size, bg_size = 120, 140
    for x, label, color in ((far_cam, "近机位 + 广角", "#3b82b5"), (near_cam, "远机位 + 长焦", "#a24862")):
        SubElement(svg, "circle", {"cx": str(x), "cy": f"{scene_y}", "r": "9", "fill": color})
        text(svg, x, scene_y + 40, label, size=22, weight="600", fill=color)
    line(svg, subject_x, scene_y, subject_x, scene_y - subject_size, stroke="#285b7a", width=7, marker="arrow-blue")
    text(svg, subject_x, scene_y - subject_size - 20, "主体", size=22, weight="600", fill="#285b7a")
    line(svg, bg_x, scene_y, bg_x, scene_y - bg_size, stroke="#a24862", width=7, marker="arrow-red")
    text(svg, bg_x, scene_y - bg_size - 20, "背景", size=22, weight="600", fill="#a24862")
    # Rays to subject top and background top.
    for cam, color in ((far_cam, "#6aa6d8"), (near_cam, "#d98298")):
        line(svg, cam, scene_y, subject_x, scene_y - subject_size, stroke=color, width=2)
        line(svg, cam, scene_y, bg_x, scene_y - bg_size, stroke=color, width=2, dash="8 6")

    # Two small rendered frames.
    for x, title_value, bg_radius in ((280, "近拍 / 广角", 25), (60, "远拍 / 长焦", 45)):
        SubElement(svg, "rect", {"x": str(x), "y": "420", "width": "200", "height": "150", "fill": "#ffffff", "stroke": "#b8c7d1", "stroke-width": "2"})
        line(svg, x + 60, 560, x + 60, 480, stroke="#285b7a", width=6, marker="arrow-blue")
        SubElement(svg, "circle", {"cx": str(x + 135), "cy": "500", "r": str(bg_radius), "fill": "#f3a9b9", "fill-opacity": "0.8"})
        text(svg, x + 100, 445, title_value, size=22, weight="600", fill="#486581")
    text(svg, 840, scene_y + 40, "后退并增加焦距后，主体像高不变；背景相对主体变大", size=22, weight="600", fill="#7b4b74")

    ElementTree(svg).write(SVG_DIR / "perspective_focal_distance.svg", encoding="utf-8", xml_declaration=True)


def vanishing_homography():
    width, height = 1200, 500
    svg = base_svg(width, height, "消失点与平面单应校正")
    line(svg, 600, 60, 600, 480, stroke="#c6d2dc", width=2)

    # Left: road plane and vanishing point.
    text(svg, 300, 20, "平行方向在图像中共享消失点", size=24, weight="600", fill="#285b7a")
    horizon_y, bottom_y = 100, 450
    vp_x = 300
    line(svg, 20, horizon_y, 580, horizon_y, stroke="#8aa2b5", width=2, dash="10 8")
    SubElement(svg, "circle", {"cx": str(vp_x), "cy": str(horizon_y), "r": "8", "fill": "#a24862"})
    text(svg, vp_x, horizon_y - 20, "消失点", size=22, weight="600", fill="#a24862")
    text(svg, 100, horizon_y - 15, "地平线", size=22, fill="#627d98", anchor="start")
    # Road boundaries and longitudinal lines.
    for bottom_x in (60, 200, 400, 540):
        line(svg, bottom_x, bottom_y, vp_x, horizon_y, stroke="#4b88b4", width=3)
    # Cross lines interpolate toward VP.
    for t in (0.18, 0.36, 0.54, 0.72, 0.9):
        y = horizon_y + t * (bottom_y - horizon_y)
        left = vp_x + t * (60 - vp_x)
        right = vp_x + t * (540 - vp_x)
        line(svg, left, y, right, y, stroke="#9fbdd3", width=2)
    text(svg, 300, 480, "地面网格中的三维平行线仍由方向决定", size=22, fill="#486581")

    # Right: quadrilateral to rectified rectangle.
    text(svg, 900, 20, "单应变换校正一个平面", size=24, weight="600", fill="#8b5e20")
    quad = [(620, 120), (890, 80), (840, 400), (640, 455), (620, 120)]
    polyline(svg, quad, stroke="#c58a2d", width=4, fill="#fff1d9")
    # Grid inside approximate quadrilateral using bilinear interpolation (illustrative).
    q00, q10, q11, q01 = quad[0], quad[1], quad[2], quad[3]
    def interp(u, v):
        x = (1-u)*(1-v)*q00[0] + u*(1-v)*q10[0] + u*v*q11[0] + (1-u)*v*q01[0]
        y = (1-u)*(1-v)*q00[1] + u*(1-v)*q10[1] + u*v*q11[1] + (1-u)*v*q01[1]
        return x, y
    for u in (0.25, 0.5, 0.75):
        polyline(svg, [interp(u, v/30) for v in range(31)], stroke="#deb46f", width=2)
    for v in (0.25, 0.5, 0.75):
        polyline(svg, [interp(u/30, v) for u in range(31)], stroke="#deb46f", width=2)

    line(svg, 860, 360, 930, 360, stroke="#4d8c6a", width=3, marker="arrow-green")
    text(svg, 890, 400, "平面校正", size=22, weight="600", fill="#397456")
    SubElement(svg, "rect", {"x": "940", "y": "100", "width": "240", "height": "320", "fill": "#eef8f2", "stroke": "#5ca47a", "stroke-width": "4"})
    for x in (1000, 1060, 1120):
        line(svg, x, 100, x, 420, stroke="#9bc9ab", width=2)
    for y in (180, 260, 340):
        line(svg, 940, y, 1180, y, stroke="#9bc9ab", width=2)
    text(svg, 900, 480, "矩形化需要拉伸与重采样", size=22, fill="#397456")

    ElementTree(svg).write(SVG_DIR / "vanishing_homography.svg", encoding="utf-8", xml_declaration=True)


def distortion_grids():
    width, height = 1200, 400
    svg = base_svg(width, height, "桶形理想和枕形畸变网格")

    panels = [
        (200, -0.16, "桶形（负系数）", "#3b82b5"),
        (600, 0.0, "理想（零系数）", "#4d8c6a"),
        (1000, 0.16, "枕形（正系数）", "#c85b73"),
    ]
    size = 300
    half = size / 2
    grid_values = [i / 5 for i in range(-5, 6)]

    for cx, k1, label, color in panels:
        cy = 180
        SubElement(svg, "rect", {"x": str(cx-half-10), "y": str(cy-half-10), "width": str(size+20), "height": str(size+20), "fill": "#ffffff", "stroke": "#b8c7d1", "stroke-width": "2"})

        def warp(x, y):
            r2 = x * x + y * y
            factor = 1 + k1 * (r2 - 1)
            return cx + half * x * factor, cy + half * y * factor

        for value in grid_values:
            points_h = [warp(-1 + 2*j/80, value) for j in range(81)]
            points_v = [warp(value, -1 + 2*j/80) for j in range(81)]
            polyline(svg, points_h, stroke=color, width=1.7)
            polyline(svg, points_v, stroke=color, width=1.7)
        SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": "5", "fill": "#102a43"})
        text(svg, cx, 370, label, size=24, weight="700", fill=color)
    ElementTree(svg).write(SVG_DIR / "distortion_grids.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    pinhole_projection()
    perspective_focal_distance()
    vanishing_homography()
    distortion_grids()


if __name__ == "__main__":
    main()
