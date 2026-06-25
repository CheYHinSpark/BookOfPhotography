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
  size: 22,
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

#let thin-lens-imaging(width: 100%) = diagram-canvas(1200, 570, draw => {
  let dark = rgb("#334e68")
  let muted = rgb("#627d98")
  let blue = rgb("#3b82b5")
  let blue-dark = rgb("#285b7a")
  let rose = rgb("#c85b73")
  let rose-dark = rgb("#9a4059")

  let segment = draw.segment
  let draw-arrow = draw.arrow
  let label = draw.label

  let axis-y = 280
  let lens-x = 600
  let object-x = 300
  let image-x = 900
  let object-top = 140
  let image-tip = 420
  let focal-length = 150

  [
    #draw-arrow(100, axis-y, 1100, axis-y, paint: rgb("#829ab1"), thickness: 2, head: 15, wing: 6)
    #label(1080, 260, [光轴 $z$], width: 100, size: 22, fill: muted)

    #lens-shape(
      draw,
      lens-x,
      80,
      480,
      50,
      rgb("#eaf4ff"),
      rgb("#5595c5"),
    )
    #segment(lens-x, 60, lens-x, 500, paint: blue, thickness: 2, dashed: true, dash: (8, 7))
    #label(lens-x, 540, [薄透镜平面], width: 200, size: 22, fill: rgb("#2f6f9f"), weight: 600)

    #segment(lens-x - focal-length, axis-y - 10, lens-x - focal-length, axis-y + 10, paint: dark, thickness: 3)
    #segment(lens-x + focal-length, axis-y - 10, lens-x + focal-length, axis-y + 10, paint: dark, thickness: 3)
    #label(lens-x - focal-length, axis-y + 35, [$F$], width: 60, size: 22, fill: dark, weight: 600)
    #label(lens-x + focal-length, axis-y + 35, [$F'$], width: 60, size: 22, fill: dark, weight: 600)

    #draw-arrow(object-x, axis-y, object-x, object-top, paint: blue-dark, thickness: 5, head: 17, wing: 8)
    #label(280, 110, [物体 $y_o$], width: 150, size: 22, fill: blue-dark, weight: 700)
    #draw-arrow(image-x, axis-y, image-x, image-tip, paint: rose-dark, thickness: 5, head: 17, wing: 8)
    #label(920, 450, [倒立实像 $y_i$], width: 210, size: 22, fill: rose-dark, weight: 700)

    #segment(object-x, object-top, lens-x, object-top, paint: blue, thickness: 3)
    #segment(lens-x, object-top, image-x, image-tip, paint: blue, thickness: 3)
    #segment(object-x, object-top, image-x, image-tip, paint: rgb("#5f8f72"), thickness: 3)
    #segment(object-x, object-top, lens-x, image-tip, paint: rgb("#c58a2d"), thickness: 3)
    #segment(lens-x, image-tip, image-x, image-tip, paint: rgb("#c58a2d"), thickness: 3)

    #horizontal-dimension(draw, object-x, lens-x, 510, [$s = -z_o$], 530, paint: dark)
    #horizontal-dimension(draw, lens-x, image-x, 510, [$s' = z_i$], 530, paint: dark)

    #label(600, 30, [$1/z_i - 1/z_o = 1/f$], width: 400, height: 40, size: 28, fill: rgb("#7b3651"), weight: 600)
  ]
}, width: width, fill: rgb("#fbfdff"))

#let aperture-pupils(width: 100%) = diagram-canvas(1350, 680, draw => {
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
    #label(105, axis-y - 30, [物方], width: 90, size: 19, fill: muted, weight: 600)
    #label(1245, axis-y - 30, [像方], width: 90, size: 19, fill: muted, weight: 600)

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

    #segment(650, 70, 650, 190, paint: dark, thickness: 8)
    #segment(650, 390, 650, 510, paint: dark, thickness: 8)
    #label(650, 48, [孔径光阑], width: 180, size: 22, fill: dark, weight: 700)
    #label(650, 325, [真实机械开口], width: 180, size: 18, fill: muted)

    #ellipse-at(480, axis-y, 22, 118, stroke: blue-dark, thickness: 4, dashed: true, dash: (12, 8))
    #label(480, 122, [入瞳], width: 120, size: 24, fill: blue-dark, weight: 700)
    #label(480, 154, [物方看到的光阑像], width: 280, size: 18, fill: blue-dark, weight: 600)

    #ellipse-at(1025, axis-y, 24, 138, stroke: rose-dark, thickness: 4, dashed: true, dash: (12, 8))
    #label(1025, 112, [出瞳], width: 120, size: 24, fill: rose-dark, weight: 700)
    #label(1025, 144, [像方看到的光阑像], width: 280, size: 18, fill: rose-dark, weight: 600)

    #segment(430, axis-y - 118, 430, axis-y + 118, paint: blue-dark, thickness: 2)
    #segment(420, axis-y - 118, 440, axis-y - 118, paint: blue-dark, thickness: 2)
    #segment(420, axis-y + 118, 440, axis-y + 118, paint: blue-dark, thickness: 2)
    #label(405, axis-y, [$D_("en")$], width: 85, size: 20, fill: blue-dark, weight: 600)

    #segment(1070, axis-y - 138, 1070, axis-y + 138, paint: rose-dark, thickness: 2)
    #segment(1060, axis-y - 138, 1080, axis-y - 138, paint: rose-dark, thickness: 2)
    #segment(1060, axis-y + 138, 1080, axis-y + 138, paint: rose-dark, thickness: 2)
    #label(1100, axis-y, [$D_("ex")$], width: 85, size: 20, fill: rose-dark, weight: 600)

    #label(120, 200, [从物方看进去], width: 190, size: 20, fill: blue-dark, weight: 600)
    #draw-arrow(130, 225, 454, axis-y - 118, paint: blue, thickness: 3, head: 14, wing: 6)
    #segment(130, 355, 454, axis-y + 118, paint: blue, thickness: 3)
    #segment(506, axis-y - 118, 650, 190, paint: blue, thickness: 2, dashed: true, dash: (8, 6))
    #segment(506, axis-y + 118, 650, 390, paint: blue, thickness: 2, dashed: true, dash: (8, 6))

    #label(1220, 200, [从像方看回来], width: 210, size: 20, fill: rose-dark, weight: 600)
    #draw-arrow(1210, 225, 1052, axis-y - 138, paint: rose, thickness: 3, head: 14, wing: 6)
    #segment(1210, 355, 1052, axis-y + 138, paint: rose, thickness: 3)
    #segment(998, axis-y - 138, 650, 190, paint: rose, thickness: 2, dashed: true, dash: (8, 6))
    #segment(998, axis-y + 138, 650, 390, paint: rose, thickness: 2, dashed: true, dash: (8, 6))

    #label(
      675,
      600,
      [虚线椭圆是同一个孔径光阑经前后镜组形成的像，位置和直径可与机械开口不同],
      width: 900,
      size: 19,
      fill: muted,
    )
  ]
}, width: width, fill: rgb("#fbfdff"))
