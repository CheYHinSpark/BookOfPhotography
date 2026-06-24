#import "drawing.typ": diagram-canvas

#let pinhole-projection(width: 100%) = diagram-canvas(1200, 440, draw => {
  let dark = rgb("#334e68")
  let muted = rgb("#627d98")
  let blue = rgb("#3b82b5")
  let blue-dark = rgb("#285b7a")
  let green = rgb("#4d8c6a")
  let green-dark = rgb("#397456")
  let rose-dark = rgb("#a24862")

  let segment = draw.segment
  let draw-arrow = draw.arrow
  let circle-at = draw.circle-at
  let label = draw.label

  let axis-y = 220
  let center-x = 480
  let virtual-x = 720
  let sensor-x = 240
  let point-x = 1080
  let point-y = 40
  let slope = (point-y - axis-y) / (point-x - center-x)
  let virtual-y = axis-y + slope * (virtual-x - center-x)
  let sensor-y = axis-y + slope * (sensor-x - center-x)

  [
    #draw-arrow(80, axis-y, 1120, axis-y, paint: rgb("#8aa2b5"), thickness: 3, head: 15, wing: 6)
    #label(1120, axis-y + 20, [光轴 $Z$], width: 120, size: 22, fill: muted)

    #segment(center-x, 20, center-x, 390, paint: dark, thickness: 2, dashed: true, dash: (8, 7))
    #circle-at(center-x, axis-y, 9, fill: rgb("#102a43"), stroke: rgb("#102a43"), thickness: 1)
    #label(500, 270, [$C$], width: 60, size: 24, fill: dark, weight: 600)

    #segment(virtual-x, 60, virtual-x, 390, paint: green, thickness: 4)
    #label(720, 40, [虚像平面 $Z=f$], width: 240, size: 22, fill: green-dark, weight: 600)
    #segment(sensor-x, 60, sensor-x, 390, paint: rose-dark, thickness: 4)
    #label(sensor-x, 40, [真实传感器], width: 180, size: 22, fill: rose-dark, weight: 600)

    #draw-arrow(sensor-x - 20, sensor-y - slope * 20, point-x, point-y, paint: blue, thickness: 3, head: 24, wing: 8)
    #circle-at(point-x, point-y, 9, fill: blue-dark, stroke: blue-dark, thickness: 1)
    #label(1010, 30, [$P(X,Z)$], width: 160, size: 24, fill: dark, weight: 600)

    #circle-at(virtual-x, virtual-y, 7, fill: rgb("#3c8d65"), stroke: rgb("#3c8d65"), thickness: 1)
    #label(760, virtual-y - 40, [$p(x,f)$], width: 150, size: 22, fill: green-dark, weight: 600)
    #circle-at(sensor-x, sensor-y, 7, fill: rgb("#b84e68"), stroke: rgb("#b84e68"), thickness: 1)
    #label(210, sensor-y + 30, [倒像], width: 100, size: 22, fill: rose-dark, weight: 600)

    #segment(center-x, 410, virtual-x, 410, paint: dark, thickness: 2)
    #segment(center-x, 400, center-x, 420, paint: dark, thickness: 2)
    #segment(virtual-x, 400, virtual-x, 420, paint: dark, thickness: 2)
    #label((center-x + virtual-x) / 2, 390, [$f$], width: 100, size: 22, fill: dark, weight: 600)

    #segment(virtual-x + 10, axis-y, virtual-x + 10, virtual-y, paint: green-dark, thickness: 2, dashed: true, dash: (5, 5))
    #label(virtual-x + 30, (axis-y + virtual-y) / 2, [$x$], width: 60, size: 22, fill: green-dark, weight: 600)
    #segment(point-x, axis-y, point-x, point-y, paint: blue-dark, thickness: 2, dashed: true, dash: (5, 5))
    #label(point-x + 20, (axis-y + point-y) / 2, [$X$], width: 60, size: 22, fill: blue-dark, weight: 600)

    #label(960, 360, [相似三角形：$x/f = X/Z$], width: 360, size: 24, fill: rgb("#7b3651"), weight: 600)
  ]
}, width: width, fill: rgb("#fbfdff"))
