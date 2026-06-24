#import "drawing.typ": diagram-canvas

#let radiance-geometry(width: 100%) = diagram-canvas(1200, 460, draw => {
    let dark-line = rgb("#334e68")
    let blue = rgb("#4b8bbd")
    let blue-dark = rgb("#285b7a")
    let rose = rgb("#c2677e")
    let rose-dark = rgb("#9a4059")

    let segment = draw.segment
    let polyline = draw.polyline
    let draw-arrow = draw.arrow
    let panel = draw.panel
    let shape = draw.shape
    let label = draw.label

    [
      #shape(
        ((150, 240), (245, 200), (330, 280), (235, 320)),
        rgb("#eaf4ff"),
        rgb("#6aa6d8"),
      )
      #shape(
        ((990, 20), (1070, 90), (1010, 180), (930, 110)),
        rgb("#fff0f3"),
        rgb("#d98298"),
      )

      #draw-arrow(240, 260, 1000, 100, paint: dark-line, thickness: 3)
      #label(620, 200, [距离 $r$], width: 100, size: 22, fill: dark-line, weight: 600)

      #draw-arrow(240, 260, 280, 110, paint: blue, thickness: 3)
      #draw-arrow(1000, 100, 840, 80, paint: rose, thickness: 3)
      #label(260, 85, [法线 $bold(n)_s$], width: 200, size: 22, fill: rgb("#356f9d"), weight: 600)
      #label(820, 45, [法线 $bold(n)_r$], width: 200, size: 22, fill: rgb("#a94e66"), weight: 600)

      #segment(240, 260, 990, 20, paint: rgb("#8aa4b8"), thickness: 2, dashed: true)
      #segment(240, 260, 1010, 180, paint: rgb("#8aa4b8"), thickness: 2, dashed: true)
      #label(620, 140, [源点所见接收面元：$dif Omega_(s arrow.r r)$], width: 390, size: 22, fill: dark-line, weight: 600)

      #polyline(
        (
          (251, 222),
          (262, 226),
          (270, 233),
          (275, 241),
          (278, 251),
        ),
        paint: blue,
        thickness: 3,
      )

      #polyline(
        (
          (910, 90),
          (908, 99),
          (908, 109),
          (910, 118),
        ),
        paint: rose,
        thickness: 3,
      )
      #label(285, 215, [$theta_s$], width: 90, size: 22, fill: rgb("#356f9d"), weight: 600)
      #label(890, 100, [$theta_r$], width: 90, size: 22, fill: rgb("#a94e66"), weight: 600)

      #label(360, 320, [源面元 $dif A_s$], width: 300, size: 22, fill: blue-dark, weight: 700)
      #label(1000, 220, [接收面元 $dif A_r$], width: 300, size: 22, fill: rose-dark, weight: 700)

      #panel(
        400, 345, 400, 100,
        rgb("#f5faff"),
        rgb("#b8ccda"),
        radius: 16,
      )
      #label(
        600, 370,
        [$dif Omega_(s arrow.r r) = (cos theta_r dif A_r) / r^2$],
        width: 800,
        height: 40,
        size: 24,
        fill: rgb("#234e70"),
        weight: 600,
      )
      #label(
        600, 420,
        [$dif^2 Phi_(s arrow.r r) = (L_s cos theta_s cos theta_r dif A_s dif A_r) / r^2$],
        width: 900,
        height: 40,
        size: 24,
        fill: rgb("#7b3651"),
        weight: 600,
      )
    ]
}, width: width)

#let radiometric-quantities(width: 100%) = diagram-canvas(1200, 460, draw => {
  let ink = rgb("#102a43")
  let blue-text = rgb("#285b7a")
  let muted = rgb("#486581")
  let arrow-color = rgb("#527da3")

  let segment = draw.segment
  let draw-arrow = draw.arrow
  let panel = draw.panel
  let label = draw.label

  let quantity-card(
    x,
    y,
    card-width,
    title,
    symbol,
    unit-content,
    card-fill,
    card-stroke,
    symbol-size: 24,
  ) = {
    panel(
      x,
      y,
      card-width,
      110,
      card-fill,
      card-stroke,
      radius: 20,
      thickness: 2.5,
    )
    label(
      x + card-width / 2,
      y + 20,
      title,
      width: card-width - 20,
      height: 30,
      size: 22,
      fill: ink,
      weight: 600,
    )
    label(
      x + card-width / 2,
      y + 55,
      symbol,
      width: card-width -20,
      height: 40,
      size: symbol-size,
      fill: blue-text,
      weight: 600,
    )
    label(
      x + card-width / 2,
      y + 90,
      unit-content,
      width: card-width - 20,
      height: 20,
      size: 22,
      fill: rgb("#627d98"),
    )
  }

  [
    #quantity-card(
      20,
      140,
      160,
      [辐射能],
      [$Q_e$],
      [$"J"$],
      rgb("#eaf4ff"),
      rgb("#8dbce6"),
    )
    #quantity-card(
      280,
      140,
      160,
      [辐射通量],
      [$Phi_e = (dif Q_e) / (dif t)$],
      [$"W"$],
      rgb("#edf8f2"),
      rgb("#8fceb0"),
    )

    #draw-arrow(190, 195, 270, 195, paint: arrow-color, thickness: 3, head: 13, wing: 6)
    #label(230, 170, [时间密度], width: 120, size: 18, fill: muted)

    #quantity-card(
      580,
      20,
      220,
      [辐照度 / 出射度],
      [$E_e slash M_e = (dif Phi_e) / (dif A)$],
      [$"W" dot "m"^(-2)$],
      rgb("#fff7e8"),
      rgb("#e4bd70"),
      symbol-size: 22,
    )
    #draw-arrow(450, 195, 570, 75, paint: arrow-color, thickness: 3, head: 14, wing: 6)
    #label(480, 100, [面积密度 $dif A$], width: 180, size: 18, fill: muted)

    #quantity-card(
      580,
      140,
      220,
      [辐射强度],
      [$I_e = (dif Phi_e) / (dif Omega)$],
      [$"W" dot "sr"^(-1)$],
      rgb("#f7efff"),
      rgb("#c4a1e4"),
    )
    #draw-arrow(450, 195, 570, 195, paint: arrow-color, thickness: 3, head: 14, wing: 6)
    #label(525, 180, [方向密度 $dif Omega$], width: 200, height: 30, size: 18, fill: muted)

    #quantity-card(
      580,
      260,
      220,
      [辐亮度],
      [$L_e = (dif^2 Phi_e) / (dif A_(perp) dif Omega)$],
      [$"W" dot "m"^(-2) dot "sr"^(-1)$],
      rgb("#fff0f3"),
      rgb("#e6a2b2"),
      symbol-size: 21,
    )
    #draw-arrow(450, 195, 570, 315, paint: arrow-color, thickness: 3, head: 14, wing: 6)
    #label(470, 290, [面积与方向密度], width: 200, height: 30, size: 18, fill: muted)

    #panel(
      840,
      40,
      320,
      310,
      rgb("#f5f8fa"),
      rgb("#b8c7d1"),
      radius: 20,
      thickness: 2,
    )
    #label(
      980,
      80,
      [变量被保留到哪一步？],
      width: 300,
      size: 24,
      fill: ink,
      weight: 600,
    )

    #label(920, 145, [$E_e slash M_e$], width: 100, height: 30, size: 20, fill: rgb("#8b5e20"), weight: 600, alignment: left + horizon)
    #label(1050, 145, [保留位置，积分方向], width: 180, height: 30, size: 20, fill: muted, alignment: left + horizon)
    #label(920, 200, [$I_e$], width: 100, height: 30, size: 20, fill: rgb("#765097"), weight: 600, alignment: left + horizon)
    #label(1050, 200, [保留方向，积分面积], width: 180, height: 30, size: 20, fill: muted, alignment: left + horizon)
    #label(920, 255, [$L_e$], width: 100, height: 30, size: 20, fill: rgb("#9a4059"), weight: 600, alignment: left + horizon)
    #label(1050, 255, [同时保留位置和方向], width: 180, height: 30, size: 20, fill: muted, alignment: left + horizon)
    #label(920, 310, [下标 $lambda$], width: 100, height: 30, size: 20, fill: blue-text, weight: 600, alignment: left + horizon)
    #label(1050, 310, [再保留波长分辨率], width: 180, height: 30, size: 20, fill: muted, alignment: left + horizon)

    #label(
      600,
      400,
      [箭头表示取密度或边缘化后的定义关系，并不表示这些量可以无条件互相反演],
      width: 1000,
      size: 22,
      fill: muted,
    )
    #label(
      600,
      435,
      [不要把相同单位或相近日常名称当成相同物理量],
      width: 1200,
      size: 22,
      fill: rgb("#7b4b74"),
    )
  ]
}, width: width)
