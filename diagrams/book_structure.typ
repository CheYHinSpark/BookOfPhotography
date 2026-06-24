#import "drawing.typ": diagram-canvas

#let book-structure(width: 100%) = diagram-canvas(1200, 1020, draw => {
  let ink = rgb("#102a43")
  let muted = rgb("#486581")
  let arrow-color = rgb("#527da3")
  let feedback-color = rgb("#b35c74")

  let panel = draw.panel
  let label = draw.label
  let segment = draw.segment
  let draw-arrow = draw.arrow

  let stage-card(
    x,
    y,
    title,
    items,
    card-fill,
    card-stroke,
  ) = {
    panel(
      x,
      y,
      500,
      200,
      card-fill,
      card-stroke,
      radius: 20,
      thickness: 2.5,
    )
    label(
      x + 250,
      y + 25,
      title,
      width: 400,
      height: 30,
      size: 24,
      fill: ink,
      weight: 600,
    )
    segment(
      x + 20,
      y + 45,
      x + 480,
      y + 45,
      paint: card-stroke,
      thickness: 1.5,
    )
    for (index, item) in items.enumerate() {
      label(
        x + 260,
        y + 70 + index * 35,
        item,
        width: 470,
        height: 30,
        size: 22,
        fill: muted,
        weight: 500,
        alignment: left + horizon,
      )
    }
  }

  [
    #stage-card(
      80,
      20,
      [一　建立问题与光的语言],
      (
        [第1章　导论：摄影作为成像与推断],
        [第2章　光的描述层次],
      ),
      rgb("#eef6ff"),
      rgb("#78a9d1"),
    )

    #stage-card(
      640,
      20,
      [二　建立空间成像],
      (
        [第3章　中心投影与摄影透视],
        [第4章　理想透镜与高斯成像],
        [第5章　对焦、离焦与景深],
      ),
      rgb("#edf9f6"),
      rgb("#74b7a5"),
    )

    #stage-card(
      640,
      280,
      [三　计量、曝光与探测],
      (
        [第6章　辐射度学与光度学],
        [第7章　曝光方程与摄影计量],
        [第8章　图像传感器的物理模型],
        [第9章　噪声、信噪比与动态范围],
      ),
      rgb("#fff7e8"),
      rgb("#d7aa55"),
    )

    #stage-card(
      80,
      280,
      [四　解释清晰度与离散化],
      (
        [第10章　衍射与有限孔径],
        [第11章　像差、MTF 与镜头评价],
        [第12章　时间采样、运动与防抖],
        [第13章　采样、像素与分辨率],
      ),
      rgb("#f5f0ff"),
      rgb("#aa91d1"),
    )

    #stage-card(
      80,
      540,
      [五　把测量变成可解释图像],
      (
        [第14章　色度学],
        [第15章　亮度编码、位深与动态范围],
        [第16章　RAW 数据与相机图像管线],
      ),
      rgb("#fff0f3"),
      rgb("#d98ba0"),
    )

    #stage-card(
      640,
      540,
      [六　控制现场并定义观看目标],
      (
        [第17章　光源、材质与布光],
        [第18章　人类视觉、构图与风格],
      ),
      rgb("#eef8ed"),
      rgb("#82b978"),
    )

    #stage-card(
      640,
      800,
      [七　用模型、先验与更多观测恢复],
      (
        [第19章　卷积、傅里叶分析与图像复原],
        [第20章　降噪、细节与 AI 恢复],
        [第21章　多帧成像与计算摄影],
      ),
      rgb("#f2f3ff"),
      rgb("#8995cf"),
    )

    #stage-card(
      80,
      800,
      [八　系统决策、交付与反馈],
      (
        [第22章　相机系统与任务化选型],
        [第23章　色彩管理、显示、打印与归档],
        [第24章　照片质量诊断与最小实验],
      ),
      rgb("#f6f8fa"),
      rgb("#91a4b5"),
    )

    #draw-arrow(580, 120, 640, 120, paint: arrow-color, thickness: 3, head: 12, wing: 6)
    #draw-arrow(890, 220, 890, 280, paint: arrow-color, thickness: 3, head: 12, wing: 6)
    #draw-arrow(640, 380, 580, 380, paint: arrow-color, thickness: 3, head: 12, wing: 6)
    #draw-arrow(330, 480, 330, 540, paint: arrow-color, thickness: 3, head: 12, wing: 6)
    #draw-arrow(580, 640, 640, 640, paint: arrow-color, thickness: 3, head: 12, wing: 6)
    #draw-arrow(890, 740, 890, 800, paint: arrow-color, thickness: 3, head: 12, wing: 6)
    #draw-arrow(640, 900, 580, 900, paint: arrow-color, thickness: 3, head: 12, wing: 6)

    #segment(80, 900, 20, 900, paint: feedback-color, thickness: 2, dashed: true)
    #segment(20, 900, 20, 120, paint: feedback-color, thickness: 2, dashed: true)
    #draw-arrow(20, 120, 80, 120, paint: feedback-color, thickness: 2, head: 12, wing: 6, dashed: true)
  ]
}, width: width)
