from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
import math


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "svg"
FONT = "Source Han Sans SC, Microsoft YaHei, sans-serif"


def text(parent, x, y, value, size=24, weight="400", fill="#243b53", anchor="middle"):
    node = SubElement(parent, "text", {
        "x": str(x), "y": str(y), "text-anchor": anchor,
        "font-family": FONT, "font-size": str(size),
        "font-weight": weight, "fill": fill,
    })
    node.text = value
    return node


def line(parent, x1, y1, x2, y2, stroke="#527da3", width=3, dash=None, marker=None):
    attrs = {"x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2),
             "stroke": stroke, "stroke-width": str(width), "stroke-linecap": "round"}
    if dash:
        attrs["stroke-dasharray"] = dash
    if marker:
        attrs["marker-end"] = f"url(#{marker})"
    return SubElement(parent, "line", attrs)


def polyline(parent, points, stroke="#527da3", width=2, fill="none", dash=None):
    attrs = {"points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points),
             "stroke": stroke, "stroke-width": str(width), "fill": fill,
             "stroke-linejoin": "round", "stroke-linecap": "round"}
    if dash:
        attrs["stroke-dasharray"] = dash
    return SubElement(parent, "polyline", attrs)


def add_defs(svg):
    defs = SubElement(svg, "defs")
    for marker_id, color in (("arrow-blue", "#3b82b5"), ("arrow-red", "#c85b73"),
                             ("arrow-dark", "#334e68"), ("arrow-green", "#4d8c6a")):
        marker = SubElement(defs, "marker", {"id": marker_id, "markerWidth": "10", "markerHeight": "8",
            "refX": "9", "refY": "4", "orient": "auto", "markerUnits": "strokeWidth"})
        SubElement(marker, "path", {"d": "M 0 0 L 10 4 L 0 8 z", "fill": color})


def base_svg(width, height, label):
    svg = Element("svg", {"xmlns": "http://www.w3.org/2000/svg", "width": str(width),
        "height": str(height), "viewBox": f"0 0 {width} {height}", "role": "img", "aria-label": label})
    add_defs(svg)
    SubElement(svg, "rect", {"width": str(width), "height": str(height), "fill": "#fbfdff"})
    return svg


def wavefront_aberration():
    width, height = 1400, 620
    svg = base_svg(width, height, "理想与像差波前")
    text(svg, width/2, 42, "波前误差改变局部法线与焦点相位", size=30, weight="700", fill="#102a43")
    line(svg, 700, 80, 700, 560, stroke="#c6d2dc", width=2)
    panels = [(350, "理想参考球面", False, "#3b82b5"), (1050, "含像差的真实波前", True, "#c85b73")]
    for cx, title_value, aberrated, color in panels:
        text(svg, cx, 92, title_value, size=24, weight="700", fill=color)
        lens_x, focus_x, axis_y = cx-220, cx+210, 330
        SubElement(svg, "ellipse", {"cx": str(lens_x), "cy": str(axis_y), "rx": "26", "ry": "160",
            "fill": "#eaf4ff", "stroke": "#5595c5", "stroke-width": "3"})
        for y0 in (205,260,330,400,455):
            target_y = axis_y
            if aberrated:
                target_y += 0.0018*(y0-axis_y)**2 * (1 if y0<axis_y else -1)
                target_x = focus_x + 0.45*abs(y0-axis_y)
            else:
                target_x = focus_x
            line(svg, lens_x, y0, target_x, target_y, stroke=color, width=2.2)
        if not aberrated:
            SubElement(svg, "circle", {"cx": str(focus_x), "cy": str(axis_y), "r": "8", "fill": color})
            text(svg, focus_x, axis_y-22, "理想像点", size=19, weight="700", fill=color)
        else:
            SubElement(svg, "ellipse", {"cx": str(focus_x+35), "cy": str(axis_y), "rx": "55", "ry": "24",
                "fill": "#efb6c5", "fill-opacity": "0.65", "stroke": color, "stroke-width": "2"})
            text(svg, focus_x+35, axis_y-42, "有限能量分布", size=19, weight="700", fill=color)
        # Wavefront arc or perturbed polyline.
        pts=[]
        for j in range(100):
            y=170+320*j/99
            base_x=cx-30+0.0013*(y-axis_y)**2
            if aberrated:
                base_x += 15*math.sin((y-axis_y)/44)+8*((y-axis_y)/160)**3
            pts.append((base_x,y))
        polyline(svg,pts,stroke="#7b4b74" if aberrated else "#4d8c6a",width=4)
        text(svg,cx,535,"W = 0" if not aberrated else "W(ρ,φ) ≠ 0",size=21,weight="700",fill="#397456" if not aberrated else "#7b4b74")
    ElementTree(svg).write(SVG_DIR / "wavefront_aberration.svg", encoding="utf-8", xml_declaration=True)


def seidel_aberrations():
    width, height = 1500, 620
    svg = base_svg(width, height, "五种 Seidel 初级单色像差")
    text(svg, width/2, 42, "初级单色像差的典型签名", size=30, weight="700", fill="#102a43")
    centers=[150,450,750,1050,1350]
    titles=["球差","彗差","像散","场曲","畸变"]
    colors=["#3b82b5","#c85b73","#8a69b4","#4d8c6a","#c58a2d"]
    for j,(cx,title_value,color) in enumerate(zip(centers,titles,colors)):
        if j>0:
            line(svg,cx-150,75,cx-150,570,stroke="#d7e0e7",width=2)
        text(svg,cx,90,title_value,size=23,weight="700",fill=color)
        cy=290
        if j==0:
            for r,op in ((95,.13),(70,.18),(45,.28),(20,.55)):
                SubElement(svg,"circle",{"cx":str(cx),"cy":str(cy),"r":str(r),"fill":color,"fill-opacity":str(op)})
            text(svg,cx,455,"轴上同心扩散",size=18,fill="#486581")
        elif j==1:
            for k in range(11):
                x=cx-55+12*k
                y=cy+35*math.sin(k/2.2)*(1-k/13)
                r=max(5,18-1.0*k)
                SubElement(svg,"circle",{"cx":f"{x:.1f}","cy":f"{y:.1f}","r":f"{r:.1f}","fill":color,"fill-opacity":f"{0.22+0.06*k:.2f}"})
            text(svg,cx,455,"离轴彗星尾",size=18,fill="#486581")
        elif j==2:
            line(svg,cx-80,cy,cx+80,cy,stroke=color,width=13)
            line(svg,cx,cy+55,cx,cy+145,stroke=color,width=13)
            text(svg,cx,455,"正交焦线分离",size=18,fill="#486581")
        elif j==3:
            line(svg,cx-95,175,cx-95,420,stroke="#334e68",width=5)
            pts=[(cx-65+160*t/99,185+235*(t/99)**2) for t in range(100)]
            polyline(svg,pts,stroke=color,width=5)
            text(svg,cx,455,"最佳焦面弯曲",size=18,fill="#486581")
        else:
            for v in [-1,-.5,0,.5,1]:
                pts=[]
                for k in range(50):
                    u=-1+2*k/49
                    r2=u*u+v*v
                    fac=1+0.18*r2
                    pts.append((cx+85*u*fac,cy+85*v*fac))
                polyline(svg,pts,stroke=color,width=2)
                pts=[]
                for k in range(50):
                    v2=-1+2*k/49
                    r2=v2*v2+v*v
                    fac=1+0.18*r2
                    pts.append((cx+85*v*fac,cy+85*v2*fac))
                polyline(svg,pts,stroke=color,width=2)
            text(svg,cx,455,"位置映射弯曲",size=18,fill="#486581")
        orders=["ρ⁴","hρ³","h²ρ²","h²ρ²","h³ρ"]
        text(svg,cx,530,orders[j],size=21,weight="700",fill=color)
    ElementTree(svg).write(SVG_DIR / "seidel_aberrations.svg", encoding="utf-8", xml_declaration=True)


def astigmatism_field_curvature():
    width,height=1400,630
    svg=base_svg(width,height,"离轴像散与场曲")
    text(svg,width/2,42,"弧矢、切向焦面与平面传感器",size=30,weight="700",fill="#102a43")
    axis_y=325
    # Left astigmatic cone.
    text(svg,340,92,"像散：两个正交焦线",size=23,weight="700",fill="#7b4b74")
    lens_x=130
    SubElement(svg,"ellipse",{"cx":str(lens_x),"cy":str(axis_y),"rx":"24","ry":"145","fill":"#eef2fa","stroke":"#8a69b4","stroke-width":"3"})
    for y in (200,250,400,450):
        line(svg,lens_x,y,590,axis_y+(y-axis_y)*0.08,stroke="#8a69b4",width=2)
    line(svg,420,260,420,390,stroke="#3b82b5",width=9)
    line(svg,505,axis_y,610,axis_y,stroke="#c85b73",width=9)
    text(svg,420,235,"切向焦线",size=18,weight="700",fill="#285b7a")
    text(svg,555,355,"弧矢焦线",size=18,weight="700",fill="#a24862")
    SubElement(svg,"circle",{"cx":"465","cy":str(axis_y),"r":"22","fill":"#cbb8df","fill-opacity":".7","stroke":"#8a69b4","stroke-width":"2"})
    text(svg,465,375,"最小弥散圆",size=17,fill="#7b4b74")
    line(svg,700,80,700,560,stroke="#d7e0e7",width=2)
    # Right field curvature.
    text(svg,1050,92,"场曲：最佳焦面不平",size=23,weight="700",fill="#397456")
    line(svg,1225,150,1225,515,stroke="#334e68",width=6)
    text(svg,1225,540,"平面传感器",size=19,weight="700")
    ys=[170+300*j/99 for j in range(100)]
    sag=[(1030+95*((y-325)/160)**2,y) for y in ys]
    tan=[(970+125*((y-325)/160)**2,y) for y in ys]
    mean=[(1000+110*((y-325)/160)**2,y) for y in ys]
    polyline(svg,sag,stroke="#3b82b5",width=4)
    polyline(svg,tan,stroke="#c85b73",width=4)
    polyline(svg,mean,stroke="#4d8c6a",width=4,dash="10 7")
    text(svg,1100,185,"弧矢面",size=18,weight="700",fill="#285b7a")
    text(svg,1010,215,"切向面",size=18,weight="700",fill="#a24862")
    text(svg,1055,490,"平均 / Petzval 趋势",size=18,weight="700",fill="#397456")
    ElementTree(svg).write(SVG_DIR / "astigmatism_field_curvature.svg", encoding="utf-8", xml_declaration=True)


def chromatic_aberration():
    width,height=1400,620
    svg=base_svg(width,height,"纵向与横向色差")
    text(svg,width/2,42,"色差：焦点位置与放大率随波长变化",size=30,weight="700",fill="#102a43")
    line(svg,700,80,700,560,stroke="#d7e0e7",width=2)
    # Longitudinal CA.
    text(svg,350,92,"纵向色差 LoCA",size=24,weight="700",fill="#486581")
    lens_x,axis_y=180,320
    SubElement(svg,"ellipse",{"cx":str(lens_x),"cy":str(axis_y),"rx":"26","ry":"150","fill":"#eef6fb","stroke":"#5595c5","stroke-width":"3"})
    colors=[("#3f6dcc",520,"蓝"),("#46a36a",565,"绿"),("#c85b73",615,"红")]
    for color,fx,label in colors:
        line(svg,lens_x,200,fx,axis_y,stroke=color,width=3)
        line(svg,lens_x,440,fx,axis_y,stroke=color,width=3)
        SubElement(svg,"circle",{"cx":str(fx),"cy":str(axis_y),"r":"7","fill":color})
        text(svg,fx,axis_y+36,label,size=18,weight="700",fill=color)
    text(svg,400,520,"蓝光焦点通常更近",size=19,fill="#486581")
    # Lateral CA.
    text(svg,1050,92,"横向色差 LaCA",size=24,weight="700",fill="#486581")
    sensor_x=1190
    line(svg,sensor_x,135,sensor_x,505,stroke="#334e68",width=5)
    center_y=320
    for color,scale,label in (("#3f6dcc",0.92,"B"),("#46a36a",1.0,"G"),("#c85b73",1.09,"R")):
        y=center_y-145*scale
        line(svg,810,center_y,sensor_x,y,stroke=color,width=3)
        line(svg,sensor_x-18,y,sensor_x+18,y,stroke=color,width=5)
        text(svg,sensor_x+28,y+5,label,size=17,weight="700",fill=color,anchor="start")
    text(svg,1030,520,"轴上重合，边缘通道位置分离",size=19,fill="#486581")
    ElementTree(svg).write(SVG_DIR / "chromatic_aberration.svg", encoding="utf-8", xml_declaration=True)


def mtf_chart_anatomy():
    width,height=1450,680
    svg=base_svg(width,height,"MTF 频率曲线和像高曲线")
    text(svg,width/2,42,"MTF 图是高维传递函数的切片",size=30,weight="700",fill="#102a43")
    line(svg,725,80,725,610,stroke="#d7e0e7",width=2)
    # Left frequency slice.
    text(svg,360,88,"固定像高：MTF 随空间频率",size=23,weight="700",fill="#285b7a")
    l,r,t,b=90,670,135,540
    line(svg,l,b,r,b,stroke="#334e68",width=2,marker="arrow-dark")
    line(svg,l,b,l,t,stroke="#334e68",width=2,marker="arrow-dark")
    for label,color,scale,power in (("中心","#397456",95,1.45),("边缘","#c85b73",58,1.25)):
        pts=[]
        for j in range(240):
            freq=120*j/239
            val=math.exp(-(freq/scale)**power)
            x=l+(r-l)*freq/120
            y=b-(b-t)*val
            pts.append((x,y))
        polyline(svg,pts,stroke=color,width=4)
        text(svg,540 if label=="中心" else 430,245 if label=="中心" else 350,label,size=19,weight="700",fill=color)
    text(svg,r,b+34,"ν (lp/mm)",size=19,fill="#627d98")
    text(svg,l-18,t+5,"MTF",size=19,fill="#627d98")
    # Right field-height slice.
    text(svg,1085,88,"固定频率：S/T 随归一化像高",size=23,weight="700",fill="#7b4b74")
    l2,r2,t2,b2=780,1390,135,540
    line(svg,l2,b2,r2,b2,stroke="#334e68",width=2,marker="arrow-dark")
    line(svg,l2,b2,l2,t2,stroke="#334e68",width=2,marker="arrow-dark")
    curves=[("10 S","#397456",lambda x:.96-.15*x*x),
            ("10 T","#69a87f",lambda x:.94-.26*x*x+.025*math.sin(3*math.pi*x)),
            ("30 S","#3b82b5",lambda x:.82-.37*x*x),
            ("30 T","#c85b73",lambda x:.80-.58*x*x+.035*math.sin(2.5*math.pi*x))]
    for idx,(label,color,func) in enumerate(curves):
        pts=[]
        for j in range(200):
            xval=j/199
            val=max(0,min(1,func(xval)))
            x=l2+(r2-l2)*xval
            y=b2-(b2-t2)*val
            pts.append((x,y))
        polyline(svg,pts,stroke=color,width=3.5,dash="9 6" if "T" in label else None)
        text(svg,810+115*idx,590,label,size=18,weight="700",fill=color)
    text(svg,r2,b2+34,"像高 0 → 1",size=19,fill="#627d98")
    text(svg,l2-18,t2+5,"MTF",size=19,fill="#627d98")
    text(svg,width/2,645,"频率、像高、方向、光圈、波长、物距与焦距都属于测试条件",size=20,fill="#627d98")
    ElementTree(svg).write(SVG_DIR / "mtf_chart_anatomy.svg", encoding="utf-8", xml_declaration=True)


def slanted_edge_pipeline():
    width,height=1500,620
    svg=base_svg(width,height,"斜边法 MTF 处理流程")
    text(svg,width/2,42,"斜边法：从亚像素边缘到频率响应",size=30,weight="700",fill="#102a43")
    centers=[170,520,880,1240]
    titles=["倾斜边缘 ROI","ESF","LSF = d(ESF)/dx","MTF = |F(LSF)|"]
    colors=["#486581","#3b82b5","#c85b73","#4d8c6a"]
    for cx,title_value,color in zip(centers,titles,colors):
        text(svg,cx,95,title_value,size=21,weight="700",fill=color)
    # ROI with pixel grid and slanted edge.
    x0,y0,w,h=70,145,200,330
    SubElement(svg,"rect",{"x":str(x0),"y":str(y0),"width":str(w),"height":str(h),"fill":"#f3f6f8","stroke":"#8aa2b5","stroke-width":"2"})
    for j in range(1,10):
        line(svg,x0+w*j/10,y0,x0+w*j/10,y0+h,stroke="#c9d4dd",width=1)
    for j in range(1,14):
        line(svg,x0,y0+h*j/14,x0+w,y0+h*j/14,stroke="#c9d4dd",width=1)
    SubElement(svg,"polygon",{"points":f"{x0},{y0+h} {x0+w},{y0+h} {x0+w},{y0+70} {x0},{y0+140}","fill":"#263746"})
    # Common axes plotting helper.
    def axes(cx):
        l,r,t,b=cx-125,cx+125,160,470
        line(svg,l,b,r,b,stroke="#334e68",width=2,marker="arrow-dark")
        line(svg,l,b,l,t,stroke="#334e68",width=2,marker="arrow-dark")
        return l,r,t,b
    # ESF sigmoid.
    l,r,t,b=axes(centers[1])
    pts=[]
    for j in range(180):
        x=-4+8*j/179
        val=1/(1+math.exp(-2.2*x))
        pts.append((l+(r-l)*j/179,b-(b-t)*val))
    polyline(svg,pts,stroke=colors[1],width=4)
    # LSF Gaussian.
    l,r,t,b=axes(centers[2])
    pts=[]
    for j in range(180):
        x=-4+8*j/179
        val=math.exp(-1.4*x*x)
        pts.append((l+(r-l)*j/179,b-(b-t)*val))
    polyline(svg,pts,stroke=colors[2],width=4)
    # MTF monotonic curve.
    l,r,t,b=axes(centers[3])
    pts=[]
    for j in range(180):
        x=3*j/179
        val=math.exp(-0.85*x*x)
        pts.append((l+(r-l)*j/179,b-(b-t)*val))
    polyline(svg,pts,stroke=colors[3],width=4)
    # Arrows between stages.
    for x1,x2,label in ((285,390,"合箱/线性化"),(645,750,"求导"),(1005,1110,"傅里叶变换")):
        line(svg,x1,310,x2,310,stroke="#627d98",width=3,marker="arrow-dark")
        text(svg,(x1+x2)/2,285,label,size=17,fill="#627d98")
    text(svg,width/2,565,"锐化、gamma、去马赛克和噪声都会进入实测曲线",size=20,fill="#7b4b74")
    ElementTree(svg).write(SVG_DIR / "slanted_edge_pipeline.svg", encoding="utf-8", xml_declaration=True)


def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    wavefront_aberration()
    seidel_aberrations()
    astigmatism_field_curvature()
    chromatic_aberration()
    mtf_chart_anatomy()
    slanted_edge_pipeline()


if __name__ == "__main__":
    main()
