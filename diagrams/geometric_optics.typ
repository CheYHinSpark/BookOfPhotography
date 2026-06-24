#import "drawing.typ": diagram-canvas

#let lens-shape(
  draw,
  x,
  top,
  bottom,
  bulge,
  fill,
  stroke,
  thickness: 3,
) = {
  let cubic-path = draw.cubic-path
  cubic-path(
    (x, top),
    (
      ((x - bulge, top + 70), (x - bulge, bottom - 70), (x, bottom)),
      ((x + bulge, bottom - 70), (x + bulge, top + 70), (x, top)),
    ),
    fill: fill,
    stroke: stroke,
    thickness: thickness,
    closed: true,
  )
}

#let horizontal-dimension(
  draw,
  x1,
  x2,
  y,
  body,
  label-y,
  paint: rgb("#334e68"),
  size: 21,
) = {
  let segment = draw.segment
  let label = draw.label
  segment(x1, y, x2, y, paint: paint, thickness: 2)
  segment(x1, y - 15, x1, y + 15, paint: paint, thickness: 2)
  segment(x2, y - 15, x2, y + 15, paint: paint, thickness: 2)
  label(
    (x1 + x2) / 2,
    label-y,
    body,
    width: x2 - x1,
    height: 32,
    size: size,
    fill: paint,
    weight: 600,
  )
}

#let fermat-snell(width: 100%) = diagram-canvas(1300, 700, draw => {
  let ink = rgb("#243b53")
  let blue = rgb("#3b82b5")
  let blue-dark = rgb("#2f6f9f")
  let rose = rgb("#c85b73")
  let rose-dark = rgb("#a24862")
  let dark = rgb("#334e68")
  let muted = rgb("#627d98")

  let segment = draw.segment
  let draw-arrow = draw.arrow
  let circle-at = draw.circle-at
  let arc = draw.arc
  let label = draw.label

  let interface-y = 350
  let point-a = (190, 105)
  let point-p = (600, interface-y)
  let point-b = (1090, 585)

  [
    #segment(90, interface-y, 1210, interface-y, paint: rgb("#829ab1"), thickness: 3)
    #label(1160, 322, [介质界面], width: 150, height: 30, size: 19, fill: muted)
    #label(1140, 130, [$n_1$], width: 90, size: 26, fill: blue-dark, weight: 700)
    #label(1140, 560, [$n_2$], width: 90, size: 26, fill: rose-dark, weight: 700)

    #draw-arrow(
      point-a.at(0), point-a.at(1),
      point-p.at(0), point-p.at(1),
      paint: blue,
      thickness: 4,
      head: 17,
      wing: 8,
    )
    #draw-arrow(
      point-p.at(0), point-p.at(1),
      point-b.at(0), point-b.at(1),
      paint: rose,
      thickness: 4,
      head: 17,
      wing: 8,
    )

    #circle-at(point-a.at(0), point-a.at(1), 8, fill: rgb("#285b7a"), stroke: rgb("#285b7a"), thickness: 1)
    #circle-at(point-p.at(0), point-p.at(1), 8, fill: dark, stroke: dark, thickness: 1)
    #circle-at(point-b.at(0), point-b.at(1), 8, fill: rgb("#9a4059"), stroke: rgb("#9a4059"), thickness: 1)
    #label(170, 78, [$A$], width: 60, size: 24, fill: ink, weight: 700)
    #label(600, 320, [$P(x)$], width: 100, size: 23, fill: ink, weight: 700)
    #label(1120, 590, [$B$], width: 60, size: 24, fill: ink, weight: 700)

    #segment(600, 120, 600, 585, paint: rgb("#73899b"), thickness: 2, dashed: true, dash: (10, 8))
    #label(650, 135, [法线], width: 100, size: 18, fill: muted)

    #arc(600, interface-y, 58, -90, -146, paint: blue, thickness: 3)
    #arc(600, interface-y, 58, 90, 29, paint: rose, thickness: 3)
    #label(548, 278, [$theta_1$], width: 90, size: 22, fill: blue-dark, weight: 600)
    #label(657, 414, [$theta_2$], width: 90, size: 22, fill: rose-dark, weight: 600)

    #segment(190, 80, 190, interface-y, paint: rgb("#aac0d1"), thickness: 2, dashed: true, dash: (6, 7))
    #segment(1090, interface-y, 1090, 615, paint: rgb("#d7a9b5"), thickness: 2, dashed: true, dash: (6, 7))
    #label(160, 235, [$a$], width: 60, size: 22, fill: rgb("#486581"), weight: 600)
    #label(1120, 485, [$b$], width: 60, size: 22, fill: rgb("#7b4b74"), weight: 600)

    #horizontal-dimension(draw, 190, 1090, 655, [水平间隔 $D$], 683, paint: dark)
    #label(370, 378, [$x$], width: 60, size: 21, fill: dark, weight: 600)
    #label(845, 378, [$D - x$], width: 120, size: 21, fill: dark, weight: 600)

    #label(330, 160, [光程 $n_1 dot A P$], width: 260, size: 20, fill: blue-dark, weight: 600)
    #label(865, 520, [光程 $n_2 dot P B$], width: 260, size: 20, fill: rose-dark, weight: 600)
  ]
}, width: width, fill: rgb("#fbfdff"))

#let thin-lens-imaging(width: 100%) = diagram-canvas(1300, 660, draw => {
  let dark = rgb("#334e68")
  let muted = rgb("#627d98")
  let blue = rgb("#3b82b5")
  let blue-dark = rgb("#285b7a")
  let rose = rgb("#c85b73")
  let rose-dark = rgb("#9a4059")

  let segment = draw.segment
  let draw-arrow = draw.arrow
  let label = draw.label

  let axis-y = 330
  let lens-x = 650
  let object-x = 300
  let image-x = 945
  let object-top = 140
  let image-tip = 490
  let focal-length = 160

  [
    #draw-arrow(80, axis-y, 1215, axis-y, paint: rgb("#829ab1"), thickness: 2, head: 15, wing: 6)
    #label(1180, 304, [光轴 $z$], width: 130, size: 20, fill: muted)

    #lens-shape(
      draw,
      lens-x,
      70,
      590,
      62,
      rgb("#eaf4ff"),
      rgb("#5595c5"),
    )
    #segment(lens-x, 75, lens-x, 585, paint: blue, thickness: 2, dashed: true, dash: (8, 7))
    #label(lens-x, 628, [薄透镜平面], width: 200, size: 20, fill: rgb("#2f6f9f"), weight: 600)

    #segment(lens-x - focal-length, axis-y - 10, lens-x - focal-length, axis-y + 10, paint: dark, thickness: 3)
    #segment(lens-x + focal-length, axis-y - 10, lens-x + focal-length, axis-y + 10, paint: dark, thickness: 3)
    #label(lens-x - focal-length, axis-y + 35, [$F$], width: 60, size: 22, fill: dark, weight: 700)
    #label(lens-x + focal-length, axis-y + 35, [$F'$], width: 60, size: 22, fill: dark, weight: 700)

    #draw-arrow(object-x, axis-y, object-x, object-top, paint: blue-dark, thickness: 5, head: 17, wing: 8)
    #label(275, 112, [物体 $y_o$], width: 150, size: 22, fill: blue-dark, weight: 700)
    #draw-arrow(image-x, axis-y, image-x, image-tip, paint: rose-dark, thickness: 5, head: 17, wing: 8)
    #label(1010, 520, [倒立实像 $y_i$], width: 210, size: 22, fill: rose-dark, weight: 700)

    #segment(object-x, object-top, lens-x, object-top, paint: blue, thickness: 3)
    #segment(lens-x, object-top, image-x, image-tip, paint: blue, thickness: 3)
    #segment(object-x, object-top, image-x, image-tip, paint: rgb("#5f8f72"), thickness: 3)
    #segment(object-x, object-top, lens-x, image-tip, paint: rgb("#c58a2d"), thickness: 3)
    #segment(lens-x, image-tip, image-x, image-tip, paint: rgb("#c58a2d"), thickness: 3)

    #horizontal-dimension(draw, object-x, lens-x, 590, [$s = -z_o$], 625, paint: dark)
    #horizontal-dimension(draw, lens-x, image-x, 590, [$s' = z_i$], 625, paint: dark)

    #label(650, 30, [$1/z_i - 1/z_o = 1/f$], width: 420, height: 42, size: 23, fill: rgb("#7b3651"), weight: 600)
  ]
}, width: width, fill: rgb("#fbfdff"))

#let aperture-pupils(width: 100%) = diagram-canvas(1350, 600, draw => {
  let dark = rgb("#334e68")
  let muted = rgb("#627d98")
  let blue = rgb("#3b82b5")
  let blue-dark = rgb("#2f7ba8")
  let rose = rgb("#c85b73")
  let rose-dark = rgb("#a24862")

  let segment = draw.segment
  let draw-arrow = draw.arrow
  let ellipse-at = draw.ellipse-at
  let label = draw.label

  let axis-y = 290

  [
    #draw-arrow(70, axis-y, 1280, axis-y, paint: rgb("#9fb3c2"), thickness: 2, head: 15, wing: 6)

    #lens-shape(
      draw,
      360,
      85,
      495,
      45,
      rgb("#eef6fb"),
      rgb("#5a9bcc"),
    )
    #label(360, 535, [前透镜组], width: 170, size: 21, fill: rgb("#5a9bcc"), weight: 700)

    #lens-shape(
      draw,
      860,
      85,
      495,
      45,
      rgb("#f5effb"),
      rgb("#8d6bb4"),
    )
    #label(860, 535, [后透镜组], width: 170, size: 21, fill: rgb("#8d6bb4"), weight: 700)

    #segment(650, 65, 650, 210, paint: dark, thickness: 8)
    #segment(650, 370, 650, 515, paint: dark, thickness: 8)
    #label(650, 48, [孔径光阑], width: 180, size: 22, fill: dark, weight: 700)
    #label(650, 325, [机械开口], width: 150, size: 18, fill: muted)

    #ellipse-at(505, axis-y, 18, 110, stroke: blue-dark, thickness: 4, dashed: true, dash: (12, 8))
    #label(505, 145, [入瞳], width: 100, size: 23, fill: blue-dark, weight: 700)
    #ellipse-at(1030, axis-y, 18, 110, stroke: rose-dark, thickness: 4, dashed: true, dash: (12, 8))
    #label(1030, 145, [出瞳], width: 100, size: 23, fill: rose-dark, weight: 700)

    #label(120, 205, [物方观察], width: 160, size: 21, fill: blue-dark, weight: 600)
    #draw-arrow(135, 225, 475, 195, paint: blue, thickness: 3, head: 15, wing: 6)
    #segment(135, 355, 475, 385, paint: blue, thickness: 3)

    #label(1200, 205, [像方观察], width: 160, size: 21, fill: rose-dark, weight: 600)
    #draw-arrow(1200, 225, 1060, 195, paint: rose, thickness: 3, head: 15, wing: 6)
    #segment(1200, 355, 1060, 385, paint: rose, thickness: 3)

    #label(
      675,
      570,
      [虚线椭圆表示瞳的位置与表观尺寸，并非额外的物理光圈],
      width: 900,
      size: 19,
      fill: muted,
    )
  ]
}, width: width, fill: rgb("#fbfdff"))
