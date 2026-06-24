from pathlib import Path
from xml.etree.ElementTree import SubElement, ElementTree
import math

from draw_raw_pipeline import base_svg, text, line, polyline, rounded_box, axes


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"


def surface_interaction():
    width, height = 1500, 780
    svg = base_svg(width, height, "光在表面的反射透射吸收与方向分布")
    text(svg, 750, 43, "材质外观不是表面的固定颜色：入射方向、观察方向与能量分配共同决定",
         size=30, weight="700", fill="#102a43")
    # source, surface, camera
    rounded_box(svg, 60, 230, 220, 130, "#fff7e8", "#e8c77d", "光源",
                "光谱 · 方向 · 角尺寸", "#8a5f19", 22)
    SubElement(svg, "rect", {"x": "610", "y": "150", "width": "34", "height": "470",
                              "rx": "10", "fill": "#94aabd"})
    text(svg, 627, 655, "表面与法线", size=18, weight="700", fill="#486581")
    line(svg, 627, 385, 627, 205, stroke="#334e68", width=3, marker="arrow-dark")
    text(svg, 650, 225, "n", size=20, weight="700", fill="#334e68", anchor="start")
    line(svg, 280, 295, 595, 365, stroke="#c58a2d", width=7, marker="arrow-gold")
    text(svg, 430, 300, "入射", size=18, weight="700", fill="#8a5f19")

    rounded_box(svg, 1190, 235, 245, 130, "#eaf4ff", "#9bc7ee", "相机 / 观察者",
                "只接收某些出射方向", "#285b7a", 21)
    line(svg, 655, 360, 1175, 295, stroke="#3b82b5", width=6, marker="arrow-blue")
    text(svg, 905, 295, "镜面分量", size=18, weight="700", fill="#285b7a")
    # diffuse rays
    for angle in (-62, -38, -15, 18, 42, 66):
        rad = math.radians(angle)
        x2 = 642 + 250 * math.cos(rad)
        y2 = 390 - 250 * math.sin(rad)
        line(svg, 642, 390, x2, y2, stroke="#4d8c6a", width=3, marker="arrow-green")
    text(svg, 845, 505, "漫反射：分散到许多方向", size=17, fill="#397456")
    line(svg, 627, 395, 627, 610, stroke="#7b4b74", width=5, marker="arrow-purple")
    text(svg, 700, 585, "透射 / 内部散射", size=17, fill="#7b4b74", anchor="start")

    rounded_box(svg, 160, 690, 1180, 55, "#eef5fb", "#a8c8e0",
                "每个波长上近似满足 R(λ)+T(λ)+A(λ)=1；相机颜色还要积分光源与传感器响应",
                None, "#285b7a", 18)
    ElementTree(svg).write(SVG_DIR / "surface_interaction.svg", encoding="utf-8",
                           xml_declaration=True)


def roughness_highlight():
    width, height = 1500, 790
    svg = base_svg(width, height, "表面粗糙度材质与高光形状")
    text(svg, 750, 43, "同一光源照在不同材料上：高光记录了光源形状经过表面方向分布后的结果",
         size=30, weight="700", fill="#102a43")
    cards = [
        (45, "光滑介质", "窄而清楚的高光", "#eaf4ff", "#9bc7ee", 28, "#ffffff"),
        (405, "粗糙介质", "宽而柔的高光", "#edf8f2", "#9fd6b7", 75, "#ffffff"),
        (765, "金属", "镜面分量带材质颜色", "#fff7e8", "#e8c77d", 45, "#d4a34f"),
        (1125, "皮肤 / 蜡", "表面高光 + 内部散射", "#fff0f3", "#eab0be", 58, "#ffd9cf"),
    ]
    for x0, title_value, subtitle, fill, stroke, radius, hcolor in cards:
        rounded_box(svg, x0, 110, 330, 540, fill, stroke, title_value, subtitle, title_size=21)
        # curved material
        SubElement(svg, "ellipse", {"cx": str(x0 + 165), "cy": "430", "rx": "118", "ry": "92",
                                     "fill": "#7e8f9f", "fill-opacity": ".82"})
        # highlight layers
        for scale, op in ((1.55, .12), (1.0, .35), (.48, .75)):
            SubElement(svg, "ellipse", {"cx": str(x0 + 125), "cy": "392",
                                         "rx": str(radius * scale), "ry": str(radius * .55 * scale),
                                         "fill": hcolor, "fill-opacity": str(op),
                                         "transform": f"rotate(-25 {x0+125} 392)"})
        line(svg, x0 + 70, 250, x0 + 115, 340, stroke="#c58a2d", width=5,
             marker="arrow-gold")
        line(svg, x0 + 205, 340, x0 + 270, 255, stroke="#3b82b5", width=5,
             marker="arrow-blue")
        text(svg, x0 + 165, 575,
             "粗糙度改变法线分布" if title_value != "皮肤 / 蜡" else "光可进入组织再逸出",
             size=15, fill="#486581")
    rounded_box(svg, 260, 700, 980, 56, "#ffffff", "#b9c7d3",
                "移动光源或机位，高光位置与形状会变；漫反射底色通常变化较慢",
                None, "#334e68", 18)
    ElementTree(svg).write(SVG_DIR / "roughness_highlight.svg", encoding="utf-8",
                           xml_declaration=True)


def source_angular_penumbra():
    width, height = 1500, 790
    svg = base_svg(width, height, "光源角尺寸与阴影半影宽度")
    text(svg, 750, 43, "光的软硬由主体看到的光源角尺寸决定，不由柔光附件名称决定",
         size=30, weight="700", fill="#102a43")
    scenes = [
        (60, "小 / 远光源", 70, "阴影边缘窄", "#c85b73"),
        (770, "大 / 近光源", 190, "半影宽，明暗过渡软", "#4d8c6a"),
    ]
    for x0, title_value, source_h, subtitle, color in scenes:
        rounded_box(svg, x0, 105, 665, 520, "#ffffff", "#b9c7d3", title_value, subtitle,
                    title_size=21)
        sx = x0 + 80
        sy = 320
        SubElement(svg, "rect", {"x": str(sx), "y": str(sy - source_h/2), "width": "26",
                                  "height": str(source_h), "rx": "9", "fill": "#f1c75b"})
        # occluder and screen
        ox, oy = x0 + 350, 330
        SubElement(svg, "circle", {"cx": str(ox), "cy": str(oy), "r": "38", "fill": "#334e68"})
        screen_x = x0 + 590
        SubElement(svg, "rect", {"x": str(screen_x), "y": "190", "width": "20", "height": "310",
                                  "rx": "8", "fill": "#d9e3ea"})
        # extreme rays
        for source_y, target_y in ((sy - source_h/2, oy - 38), (sy + source_h/2, oy + 38),
                                   (sy - source_h/2, oy + 38), (sy + source_h/2, oy - 38)):
            slope = (target_y - source_y) / (ox - sx)
            end_y = target_y + slope * (screen_x - ox)
            line(svg, sx + 26, source_y, screen_x, end_y, stroke=color, width=2.5)
        penumbra = 42 if source_h < 100 else 138
        SubElement(svg, "rect", {"x": str(screen_x - 3), "y": str(330 - penumbra), "width": "26",
                                  "height": str(2 * penumbra), "fill": color, "fill-opacity": ".25"})
        text(svg, x0 + 335, 555, "α ≈ D/R　　半影宽 w ≈ zα", size=20,
             weight="700", fill=color)
    rounded_box(svg, 235, 680, 1030, 66, "#fff7e8", "#e8c77d",
                "同一柔光箱移近主体，角尺寸增大而光更软；移远后即使物理尺寸不变也会变硬",
                None, "#8a5f19", 18)
    ElementTree(svg).write(SVG_DIR / "source_angular_penumbra.svg", encoding="utf-8",
                           xml_declaration=True)


def inverse_square_falloff():
    width, height = 1500, 790
    svg = base_svg(width, height, "点光源平方反比和主体内相对衰减")
    text(svg, 750, 43, "近光源的绝对照度高，主体前后相对距离差也更显著",
         size=30, weight="700", fill="#102a43")
    l, r, t, b = 105, 710, 130, 570
    axes(svg, l, r, t, b, "距离 r", "相对照度 E/I")
    pts = []
    for j in range(1, 181):
        u = j / 180
        dist = .5 + 4.5 * u
        val = 1 / (dist * dist)
        x = l + u * (r - l)
        y = b - min(1, val / 4) * (b - t - 10)
        pts.append((x, y))
    polyline(svg, pts, stroke="#3b82b5", width=6)
    text(svg, 410, 210, "E = I cosθ / r²", size=24, weight="700", fill="#285b7a")
    text(svg, 155, 620, "只适用于足够小、足够远的光源近似", size=15, fill="#627d98", anchor="start")

    # relative falloff examples
    examples = [
        (820, 135, "近光源", 95, 190, "前后距离 1 m → 2 m", "照度比 4:1（2 档）", "#c58a2d"),
        (820, 400, "远光源", 230, 290, "前后距离 4 m → 5 m", "照度比约 1.56:1（0.64 档）", "#4d8c6a"),
    ]
    for x0, y0, title_value, d1, d2, detail, ratio, color in examples:
        rounded_box(svg, x0, y0, 610, 205, "#ffffff", "#b9c7d3", title_value, detail,
                    title_size=20)
        source_x = x0 + 55
        SubElement(svg, "circle", {"cx": str(source_x), "cy": str(y0 + 125), "r": "18",
                                    "fill": "#f1c75b"})
        for xx, op in ((x0 + d1, .90), (x0 + d2, .42 if title_value == "近光源" else .65)):
            SubElement(svg, "ellipse", {"cx": str(xx + 120), "cy": str(y0 + 128),
                                         "rx": "28", "ry": "48", "fill": color,
                                         "fill-opacity": str(op)})
        line(svg, source_x + 25, y0 + 125, x0 + 560, y0 + 125, stroke=color, width=3)
        text(svg, x0 + 305, y0 + 185, ratio, size=17, weight="700", fill=color)
    rounded_box(svg, 850, 690, 530, 58, "#eef5fb", "#a8c8e0",
                "大型近距离扩展源需按立体角积分，不能机械套 1/r²",
                None, "#285b7a", 17)
    ElementTree(svg).write(SVG_DIR / "inverse_square_falloff.svg", encoding="utf-8",
                           xml_declaration=True)


def face_lighting_geometry():
    width, height = 1500, 800
    svg = base_svg(width, height, "人像布光中的光位面部法线阴影和眼神光")
    text(svg, 750, 43, "经典布光名称只是几何结果：光位改变面部法线的受光与投影阴影",
         size=30, weight="700", fill="#102a43")
    cards = [
        (45, "顺光 / 正面", "阴影少，起伏变弱", "front"),
        (405, "侧前上方", "面颊塑形，鼻影落向侧下", "rembrandt"),
        (765, "正前上方", "鼻影向下，下颌分离", "butterfly"),
        (1125, "侧光", "明暗分割，纹理与轮廓强", "split"),
    ]
    for idx, (x0, title_value, subtitle, mode) in enumerate(cards):
        rounded_box(svg, x0, 105, 330, 545, "#ffffff", "#b9c7d3", title_value, subtitle,
                    title_size=20)
        defs = SubElement(svg, "defs")
        clip_id = f"face-clip-{idx}"
        clip = SubElement(defs, "clipPath", {"id": clip_id})
        SubElement(clip, "ellipse", {"cx": str(x0 + 165), "cy": "420", "rx": "92", "ry": "125"})
        SubElement(svg, "ellipse", {"cx": str(x0 + 165), "cy": "420", "rx": "92", "ry": "125",
                                     "fill": "#d9a68f", "stroke": "#8b6758", "stroke-width": "3"})
        if mode == "front":
            SubElement(svg, "ellipse", {"cx": str(x0 + 165), "cy": "400", "rx": "70", "ry": "100",
                                         "fill": "#ffe4c7", "fill-opacity": ".48",
                                         "clip-path": f"url(#{clip_id})"})
            light_x, light_y = x0 + 165, 210
        elif mode == "rembrandt":
            SubElement(svg, "rect", {"x": str(x0 + 165), "y": "285", "width": "110", "height": "280",
                                      "fill": "#334e68", "fill-opacity": ".38",
                                      "clip-path": f"url(#{clip_id})"})
            SubElement(svg, "path", {"d": f"M {x0+158} 410 L {x0+195} 438 L {x0+165} 455 Z",
                                      "fill": "#ffe7c2", "fill-opacity": ".80"})
            light_x, light_y = x0 + 65, 215
        elif mode == "butterfly":
            SubElement(svg, "ellipse", {"cx": str(x0 + 165), "cy": "460", "rx": "45", "ry": "80",
                                         "fill": "#334e68", "fill-opacity": ".27",
                                         "clip-path": f"url(#{clip_id})"})
            light_x, light_y = x0 + 165, 195
        else:
            SubElement(svg, "rect", {"x": str(x0 + 165), "y": "280", "width": "110", "height": "290",
                                      "fill": "#243b53", "fill-opacity": ".58",
                                      "clip-path": f"url(#{clip_id})"})
            light_x, light_y = x0 + 55, 360
        # simple face features
        for ex in (x0 + 132, x0 + 198):
            SubElement(svg, "ellipse", {"cx": str(ex), "cy": "395", "rx": "9", "ry": "5",
                                         "fill": "#334e68"})
        line(svg, x0 + 165, 405, x0 + 155, 445, stroke="#8b6758", width=3)
        SubElement(svg, "path", {"d": f"M {x0+140} 478 Q {x0+165} 494 {x0+190} 478",
                                  "fill": "none", "stroke": "#8b6758", "stroke-width": "3"})
        SubElement(svg, "circle", {"cx": str(light_x), "cy": str(light_y), "r": "21",
                                    "fill": "#f1c75b"})
        line(svg, light_x, light_y + 24, x0 + 165, 315, stroke="#c58a2d", width=4,
             marker="arrow-gold")
        text(svg, x0 + 165, 590, "眼神光位置随光源方向移动", size=14, fill="#486581")
    rounded_box(svg, 250, 700, 1000, 60, "#edf8f2", "#9fd6b7",
                "先观察高光、鼻影、面颊梯度与背景分离，再决定是否需要柔化、补光或移动机位",
                None, "#397456", 18)
    ElementTree(svg).write(SVG_DIR / "face_lighting_geometry.svg", encoding="utf-8",
                           xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    surface_interaction()
    roughness_highlight()
    source_angular_penumbra()
    inverse_square_falloff()
    face_lighting_geometry()


if __name__ == "__main__":
    main()
