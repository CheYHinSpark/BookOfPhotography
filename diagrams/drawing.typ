#let diagram-canvas(
  logical-width,
  logical-height,
  body,
  width: 100%,
  fill: none,
  clip: true,
) = box(width: width)[
  #layout(size => {
    let canvas-width = size.width
    let scale = canvas-width / logical-width
    let canvas-height = logical-height * scale
    let unit(value) = value * scale

    let put(body) = place(top + left, body)

    let stroke-style(
      paint,
      thickness,
      dashed: false,
      dash: (9, 7),
      cap: "round",
      join: "miter",
    ) = {
      let style = (
        paint: paint,
        thickness: unit(thickness),
        cap: cap,
        join: join,
      )
      if dashed {
        style.insert(
          "dash",
          (array: dash.map(value => unit(value))),
        )
      }
      style
    }

    let segment(
      x1,
      y1,
      x2,
      y2,
      paint: rgb("#334e68"),
      thickness: 2,
      dashed: false,
      dash: (9, 7),
    ) = {
      put(line(
        start: (unit(x1), unit(y1)),
        end: (unit(x2), unit(y2)),
        stroke: stroke-style(
          paint,
          thickness,
          dashed: dashed,
          dash: dash,
        ),
      ))
    }

    let polyline(
      points,
      paint: rgb("#334e68"),
      thickness: 2,
      closed: false,
    ) = {
      if points.len() < 2 { return }

      for index in range(points.len() - 1) {
        let start = points.at(index)
        let end = points.at(index + 1)
        segment(
          start.at(0),
          start.at(1),
          end.at(0),
          end.at(1),
          paint: paint,
          thickness: thickness,
        )
      }

      if closed {
        let start = points.last()
        let end = points.first()
        segment(
          start.at(0),
          start.at(1),
          end.at(0),
          end.at(1),
          paint: paint,
          thickness: thickness,
        )
      }
    }

    let arrow(
      x1,
      y1,
      x2,
      y2,
      paint: rgb("#334e68"),
      thickness: 3,
      head: 16,
      wing: 7,
      dashed: false,
    ) = {
      let dx = x2 - x1
      let dy = y2 - y1
      let length = calc.sqrt(dx * dx + dy * dy)
      let ux = dx / length
      let uy = dy / length
      let base-x = x2 - ux * head
      let base-y = y2 - uy * head
      let perpendicular-x = -uy
      let perpendicular-y = ux

      segment(x1, y1, x2 - head * perpendicular-y, y2 + head * perpendicular-x, paint: paint, thickness: thickness, dashed: dashed)
      put(polygon(
        fill: paint,
        (unit(x2), unit(y2)),
        (
          unit(base-x + perpendicular-x * wing),
          unit(base-y + perpendicular-y * wing),
        ),
        (
          unit(base-x - perpendicular-x * wing),
          unit(base-y - perpendicular-y * wing),
        ),
      ))
    }

    let panel(
      x,
      y,
      panel-width,
      panel-height,
      panel-fill,
      panel-stroke,
      radius: 0,
      thickness: 2,
    ) = place(
      top + left,
      dx: unit(x),
      dy: unit(y),
      rect(
        width: unit(panel-width),
        height: unit(panel-height),
        radius: unit(radius),
        fill: panel-fill,
        stroke: (paint: panel-stroke, thickness: unit(thickness)),
      ),
    )

    let shape(points, shape-fill, shape-stroke, thickness: 3) = put(polygon(
      fill: shape-fill,
      stroke: (
        paint: shape-stroke,
        thickness: unit(thickness),
        join: "round",
      ),
      ..points.map(point => (unit(point.at(0)), unit(point.at(1)))),
    ))

    let ellipse-at(
      x,
      y,
      radius-x,
      radius-y,
      fill: none,
      stroke: rgb("#334e68"),
      thickness: 2,
      dashed: false,
      dash: (9, 7),
    ) = place(
      top + left,
      dx: unit(x - radius-x),
      dy: unit(y - radius-y),
      ellipse(
        width: unit(2 * radius-x),
        height: unit(2 * radius-y),
        fill: fill,
        stroke: stroke-style(
          stroke,
          thickness,
          dashed: dashed,
          dash: dash,
        ),
      ),
    )

    let circle-at(
      x,
      y,
      radius,
      fill: none,
      stroke: rgb("#334e68"),
      thickness: 2,
      dashed: false,
      dash: (9, 7),
    ) = ellipse-at(
      x,
      y,
      radius,
      radius,
      fill: fill,
      stroke: stroke,
      thickness: thickness,
      dashed: dashed,
      dash: dash,
    )

    let arc(
      x,
      y,
      radius,
      start-angle,
      end-angle,
      paint: rgb("#334e68"),
      thickness: 2,
      steps: 14,
    ) = {
      let points = range(steps + 1).map(index => {
        let angle = start-angle + (end-angle - start-angle) * index / steps
        (
          x + radius * calc.cos(angle * 1deg),
          y + radius * calc.sin(angle * 1deg),
        )
      })
      polyline(points, paint: paint, thickness: thickness)
    }

    let cubic-path(
      start,
      segments,
      fill: none,
      stroke: rgb("#334e68"),
      thickness: 2,
      closed: false,
      dashed: false,
      dash: (9, 7),
    ) = {
      let commands = (
        curve.move((unit(start.at(0)), unit(start.at(1)))),
      )
      for segment in segments {
        commands.push(curve.cubic(
          (unit(segment.at(0).at(0)), unit(segment.at(0).at(1))),
          (unit(segment.at(1).at(0)), unit(segment.at(1).at(1))),
          (unit(segment.at(2).at(0)), unit(segment.at(2).at(1))),
        ))
      }
      if closed {
        commands.push(curve.close(mode: "straight"))
      }
      put(curve(
        fill: fill,
        stroke: stroke-style(
          stroke,
          thickness,
          dashed: dashed,
          dash: dash,
          join: "round",
        ),
        ..commands,
      ))
    }

    let label(
      x,
      y,
      body,
      width: 360,
      height: 42,
      size: 20,
      fill: rgb("#334e68"),
      weight: 400,
      alignment: center + horizon,
    ) = place(
      top + left,
      dx: unit(x - width / 2),
      dy: unit(y - height / 2),
      block(width: unit(width), height: unit(height))[
        #align(alignment)[
          #text(size: unit(size), fill: fill, weight: weight)[#body]
        ]
      ],
    )

    let drawing = (
      unit: unit,
      put: put,
      segment: segment,
      polyline: polyline,
      arrow: arrow,
      panel: panel,
      shape: shape,
      ellipse-at: ellipse-at,
      circle-at: circle-at,
      arc: arc,
      cubic-path: cubic-path,
      label: label,
    )

    block(
      width: canvas-width,
      height: canvas-height,
      clip: clip,
    )[
      #body(drawing)
    ]
  })
]
