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
    SubElement(svg, "rect", {"width": str(width), "height": str(height), "fill": "#fbfdff"})
    return svg


def bessel_j1(x):
    if x == 0:
        return 0.0
    term = x / 2.0
    total = term
    for m in range(60):
        term *= -(x*x/4.0) / ((m+1)*(m+2))
        total += term
        if abs(term) < 1e-15 * max(1.0, abs(total)):
            break
    return total


def airy_intensity(rho):
    x = math.pi * rho
    if abs(x) < 1e-12:
        return 1.0
    value = 2 * bessel_j1(x) / x
    return value * value


def diffraction_regimes():
    width, height = 1400, 650
    svg = base_svg(width, height, "菲涅耳与夫琅禾费衍射区域")
    text(svg, width / 2, 43, "有限孔径后的近场与远场", size=30, weight="700", fill="#102a43")
    axis_y = 330
    aperture_x = 260
    line(svg, 70, axis_y, 1320, axis_y, stroke="#9fb3c2", width=2, marker="arrow-dark")
    line(svg, aperture_x, 100, aperture_x, 245, stroke="#334e68", width=8)
    line(svg, aperture_x, 415, aperture_x, 560, stroke="#334e68", width=8)
    text(svg, aperture_x, 80, "有限孔径 2a", size=22, weight="700")
    # Plane waves before aperture.
    for x in (95, 140, 185, 225):
        line(svg, x, 145, x, 515, stroke="#6aa6d8", width=2)
    # Huygens wavelets and envelopes.
    for radius, opacity in ((95,0.75),(180,0.55),(270,0.38),(360,0.25)):
        for y0 in (255, 330, 405):
            SubElement(svg, "path", {"d": f"M {aperture_x} {y0-radius} A {radius} {radius} 0 0 1 {aperture_x} {y0+radius}", "fill": "none", "stroke": "#7ba9ca", "stroke-width": "1.7", "stroke-opacity": str(opacity)})
    # Near plane and far/focal plane.
    near_x, far_x = 690, 1210
    line(svg, near_x, 105, near_x, 555, stroke="#c58a2d", width=4)
    line(svg, far_x, 105, far_x, 555, stroke="#a24862", width=5)
    text(svg, near_x, 85, "菲涅耳近场", size=23, weight="700", fill="#8b5e20")
    text(svg, far_x, 85, "夫琅禾费角谱 / 焦平面", size=23, weight="700", fill="#a24862")
    # Stylized intensity marks.
    for y, w in ((220,30),(275,55),(330,90),(385,55),(440,30)):
        line(svg, near_x-w/2, y, near_x+w/2, y, stroke="#d29a45", width=7)
    for y, w, opacity in ((250,20,0.35),(292,38,0.55),(330,95,1),(368,38,0.55),(410,20,0.35)):
        line(svg, far_x-w/2, y, far_x+w/2, y, stroke="#c85b73", width=8)
    text(svg, 475, 602, "F = a²/(λz) 较大", size=20, weight="600", fill="#8b5e20")
    text(svg, 1020, 602, "F ≪ 1：角分布近似瞳函数的傅里叶变换", size=20, weight="600", fill="#7b4b74")

    ElementTree(svg).write(SVG_DIR / "diffraction_regimes.svg", encoding="utf-8", xml_declaration=True)


def airy_pattern():
    width, height = 1400, 650
    svg = base_svg(width, height, "艾里图样及径向强度")
    text(svg, width / 2, 43, "圆孔衍射：二维艾里环与一维径向强度", size=30, weight="700", fill="#102a43")
    line(svg, 620, 80, 620, 585, stroke="#c6d2dc", width=2)
    # Left: stylized 2D pattern on dark square.
    SubElement(svg, "rect", {"x": "80", "y": "100", "width": "470", "height": "470", "rx": "18", "fill": "#101923", "stroke": "#50677a", "stroke-width": "2"})
    cx, cy = 315, 335
    rings = [(190,"#5d7690",0.14),(160,"#0f1720",1),(140,"#718ca6",0.18),(112,"#0f1720",1),(92,"#93adc4",0.24),(63,"#0f1720",1),(52,"#fff8dd",0.95)]
    for radius, color, opacity in rings:
        SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": str(radius), "fill": color, "fill-opacity": str(opacity), "stroke": "none"})
    text(svg, cx, 600, "中央主瓣约含 83.8% 能量", size=20, weight="600", fill="#486581")

    # Right: accurate radial profile.
    left, right, top, bottom = 700, 1320, 115, 535
    line(svg, left, bottom, right, bottom, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, left, bottom, left, top, stroke="#334e68", width=2, marker="arrow-dark")
    text(svg, right-10, bottom+34, "ρ = r/(λN)", size=20, fill="#627d98")
    text(svg, left-18, top+10, "I/I₀", size=20, fill="#627d98")
    pts = []
    for j in range(500):
        rho = 4.2*j/499
        intensity = airy_intensity(rho)
        x = left + (right-left)*rho/4.2
        y = bottom - (bottom-top-20)*intensity
        pts.append((x,y))
    polyline(svg, pts, stroke="#3b82b5", width=4)
    first_zero = 1.22
    x0 = left + (right-left)*first_zero/4.2
    line(svg, x0, bottom, x0, top+85, stroke="#c85b73", width=2, dash="9 7")
    text(svg, x0+8, top+72, "第一暗环 1.22λN", size=18, weight="700", fill="#a24862", anchor="start")
    for rho in (0,1,2,3,4):
        x = left + (right-left)*rho/4.2
        line(svg, x, bottom-6, x, bottom+6, stroke="#334e68", width=2)
        text(svg, x, bottom+24, str(rho), size=16, fill="#486581")

    ElementTree(svg).write(SVG_DIR / "airy_pattern.svg", encoding="utf-8", xml_declaration=True)


def circular_mtf(freq, f_number, wavelength_mm=0.00055):
    cutoff = 1.0 / (wavelength_mm * f_number)
    x = freq / cutoff
    if x >= 1:
        return 0.0
    if x <= 0:
        return 1.0
    return 2/math.pi * (math.acos(x) - x*math.sqrt(1-x*x))


def mtf_sampling():
    width, height = 1400, 680
    svg = base_svg(width, height, "衍射 MTF 与像素 Nyquist 频率")
    text(svg, width / 2, 43, "衍射 MTF 与传感器采样带宽", size=30, weight="700", fill="#102a43")
    left, right, top, bottom = 105, 1300, 105, 560
    line(svg, left, bottom, right, bottom, stroke="#334e68", width=2, marker="arrow-dark")
    line(svg, left, bottom, left, top, stroke="#334e68", width=2, marker="arrow-dark")
    text(svg, right-5, bottom+38, "空间频率 ν (lp/mm)", size=20, fill="#627d98")
    text(svg, left-25, top+5, "MTF", size=20, fill="#627d98")
    max_freq = 500
    curves = [
        (4,"#397456",330),
        (8,"#3b82b5",130),
        (16,"#c85b73",70),
        (22,"#8b5e20",25),
    ]
    for n_value, color, label_freq in curves:
        pts = []
        for j in range(500):
            freq = max_freq*j/499
            mtf = circular_mtf(freq, n_value)
            x = left + (right-left)*freq/max_freq
            y = bottom - (bottom-top)*mtf
            pts.append((x,y))
        polyline(svg, pts, stroke=color, width=4)
        label_mtf = circular_mtf(label_freq,n_value)
        lx = left + (right-left)*label_freq/max_freq
        ly = bottom - (bottom-top)*label_mtf
        text(svg, lx+10, ly-10, f"f/{n_value}", size=18, weight="700", fill=color, anchor="start")
    # Nyquist lines.
    for freq, label, color in ((83.33,"6 μm Nyquist","#7b4b74"),(125,"4 μm Nyquist","#7251a2")):
        x = left + (right-left)*freq/max_freq
        line(svg, x, bottom, x, top, stroke=color, width=2, dash="10 7")
        text(svg, x+8, top+28 if freq<100 else top+55, label, size=17, weight="600", fill=color, anchor="start")
    for freq in (0,100,200,300,400,500):
        x = left + (right-left)*freq/max_freq
        line(svg, x, bottom-6, x, bottom+6, stroke="#334e68", width=2)
        text(svg, x, bottom+24, str(freq), size=16, fill="#486581")
    for value in (0,0.25,0.5,0.75,1):
        y = bottom - (bottom-top)*value
        line(svg, left-6, y, left+6, y, stroke="#334e68", width=2)
        text(svg, left-14, y+5, f"{value:g}", size=16, fill="#486581", anchor="end")
    text(svg, width/2, 640, "曲线连续下降；不同采样频率只是在同一响应上选择不同评价位置", size=20, fill="#627d98")

    ElementTree(svg).write(SVG_DIR / "mtf_sampling.svg", encoding="utf-8", xml_declaration=True)


def polygon_points(cx, cy, radius, n, rotation=-math.pi/2):
    return [(cx+radius*math.cos(rotation+2*math.pi*j/n), cy+radius*math.sin(rotation+2*math.pi*j/n)) for j in range(n)]


def aperture_starbursts():
    width, height = 1400, 650
    svg = base_svg(width, height, "光圈形状与衍射星芒")
    text(svg, width / 2, 43, "孔径边缘决定远场方向结构", size=30, weight="700", fill="#102a43")
    panels = [(240,0,"圆孔","艾里环"),(700,6,"六边形","6 条主星芒"),(1160,7,"七边形","14 条主星芒")]
    for cx,n,title_value,subtitle in panels:
        cy=245
        if n==0:
            SubElement(svg, "circle", {"cx": str(cx), "cy": str(cy), "r": "105", "fill": "#d9edf9", "stroke": "#4b8bbd", "stroke-width": "4"})
        else:
            pts=polygon_points(cx,cy,108,n)
            SubElement(svg, "polygon", {"points": " ".join(f"{x:.1f},{y:.1f}" for x,y in pts), "fill": "#e8f5ec" if n==6 else "#fbe9ee", "stroke": "#4d8c6a" if n==6 else "#c2677e", "stroke-width": "4"})
        text(svg,cx,90,title_value,size=24,weight="700",fill="#243b53")
        # Pattern below/right within panel.
        py=470
        SubElement(svg,"circle",{"cx":str(cx),"cy":str(py),"r":"16","fill":"#fff3b0","stroke":"#d5962d","stroke-width":"3"})
        if n==0:
            for r,op in ((38,0.4),(62,0.25),(88,0.14)):
                SubElement(svg,"circle",{"cx":str(cx),"cy":str(py),"r":str(r),"fill":"none","stroke":"#d5962d","stroke-width":"3","stroke-opacity":str(op)})
        else:
            spike_count=n if n%2==0 else 2*n
            for j in range(spike_count):
                angle=2*math.pi*j/spike_count
                length=105 if j%2==0 else 82
                x2=cx+length*math.cos(angle)
                y2=py+length*math.sin(angle)
                line(svg,cx,py,x2,y2,stroke="#d5962d",width=3)
        text(svg,cx,610,subtitle,size=20,weight="700",fill="#7b4b74")
    line(svg,470,75,470,620,stroke="#d7e0e7",width=2)
    line(svg,930,75,930,620,stroke="#d7e0e7",width=2)

    ElementTree(svg).write(SVG_DIR / "aperture_starbursts.svg", encoding="utf-8", xml_declaration=True)


def blur_tradeoff():
    width, height = 1400, 670
    svg = base_svg(width, height, "几何离焦与衍射的光圈折中")
    text(svg, width / 2, 43, "缩小光圈：几何离焦下降，衍射上升", size=30, weight="700", fill="#102a43")
    left,right,top,bottom=110,1300,105,550
    line(svg,left,bottom,right,bottom,stroke="#334e68",width=2,marker="arrow-dark")
    line(svg,left,bottom,left,top,stroke="#334e68",width=2,marker="arrow-dark")
    text(svg,right-5,bottom+38,"f 数 N",size=20,fill="#627d98")
    text(svg,left-25,top+5,"模糊尺度",size=20,fill="#627d98")
    n_min,n_max=1.4,22
    a=80.0
    b=2.44*0.55
    n_opt=math.sqrt(a/b)
    curves=[("几何离焦 A/N",lambda n:a/n,"#3b82b5"),("衍射 BN",lambda n:b*n,"#c85b73"),("合成",lambda n:math.sqrt((a/n)**2+(b*n)**2),"#4d8c6a")]
    max_blur=65
    for label,func,color in curves:
        pts=[]
        for j in range(400):
            n=n_min+(n_max-n_min)*j/399
            val=min(func(n),max_blur)
            x=left+(right-left)*(n-n_min)/(n_max-n_min)
            y=bottom-(bottom-top)*val/max_blur
            pts.append((x,y))
        polyline(svg,pts,stroke=color,width=4)
    # Direct labels.
    text(svg,260,175,"几何离焦 A/N",size=19,weight="700",fill="#285b7a")
    text(svg,1120,250,"衍射 BN",size=19,weight="700",fill="#a24862")
    text(svg,1030,390,"合成尺度",size=19,weight="700",fill="#397456")
    xopt=left+(right-left)*(n_opt-n_min)/(n_max-n_min)
    yopt=bottom-(bottom-top)*math.sqrt((a/n_opt)**2+(b*n_opt)**2)/max_blur
    line(svg,xopt,bottom,xopt,yopt,stroke="#8b5e20",width=2,dash="9 7")
    SubElement(svg,"circle",{"cx":f"{xopt:.2f}","cy":f"{yopt:.2f}","r":"8","fill":"#c58a2d"})
    text(svg,xopt,yopt-20,f"示例最小值 f/{n_opt:.1f}",size=19,weight="700",fill="#8b5e20")
    for n in (2,4,8,11,16,22):
        x=left+(right-left)*(n-n_min)/(n_max-n_min)
        line(svg,x,bottom-6,x,bottom+6,stroke="#334e68",width=2)
        text(svg,x,bottom+25,str(n),size=16,fill="#486581")
    text(svg,width/2,630,"最小值随离焦量、波长、评价频率和像差状态改变，并非镜头常数",size=20,fill="#627d98")

    ElementTree(svg).write(SVG_DIR / "blur_tradeoff.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    diffraction_regimes()
    airy_pattern()
    mtf_sampling()
    aperture_starbursts()
    blur_tradeoff()


if __name__ == "__main__":
    main()
