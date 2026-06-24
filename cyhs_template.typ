// CYHS template for Typst.
// A reusable template, similar in spirit to a LaTeX .sty file.
// The document calls `#show: article.with(...)` once, then uses front-matter
// commands such as `#make-title`, `#abstract`, `#keywords`, and
// `#make-outline`. Those commands read the locale configured by `article`.

// === 0. Theme Tokens ===

#let main-fonts = (
  "Source Han Serif SC",
  "Times New Roman",
  "SimSun"
)
#let code-fonts = (
  "Consolas",
  "Courier New",
  "LXGW WenKai Mono"
)
#let strong-fonts = (
  "Source Han Serif SC",
  "Times New Roman",
  "SimSun",
  "Microsoft YaHei",
)

#let color-cite-num = rgb("#02468a")
#let color-table-stroke = luma(160)
#let color-raw-bg = luma(240)
#let color-raw-text = rgb("#014523")
#let color-key-bg = rgb("#f3f9ff")
#let color-key-line = rgb("#bddeff")
#let color-struct-bg = rgb("#f0fef7")
#let color-struct-line = rgb("#9cfebd")
#let color-warn-bg = rgb("#fff6ed")
#let color-warn-line = rgb("#ffce9d")

#let box-radius = 8pt

#let font-size = 11pt
#let small-size = 9.5pt
#let table-font-size = 9.5pt
#let table-leading = 6pt
#let footnote-size = 8.5pt
#let footnote-gap = 5pt
#let footnote-clearance = 10pt
#let footnote-numbering = "1"
#let footnote-marker-size = 8pt
#let footnote-marker-gap = 1.5pt
#let footnote-entry-marker-separator = [: ]
#let footnote-separator-length = 40%
#let footnote-separator-stroke = (paint: luma(160), thickness: 0.5pt)
#let paragraph-leading = 10pt
#let paragraph-spacing = 14pt

// A compact, unnumbered label for paragraph-scale topics. Keep it visually
// subordinate to a level-3 heading and outside the document hierarchy.
#let paragraph-heading(body) = block(
  above: 12pt,
  below: 10pt,
  sticky: true,
)[
  #text(font: strong-fonts, size: font-size, weight: "bold")[#body]
]

// Reference entry layout lives in CSL; Typst controls the wrapper around it.
#let default-bibliography-style = "cyhs-reference.csl"

#let list-marker = text(
  font: strong-fonts,
  size: font-size,
  weight: "bold",
)[▪]
#let enum-numbering(n) = {
  text(font: strong-fonts, weight: "bold")[#numbering("1.", n)]
}
#let footnote-separator = line(
  length: footnote-separator-length,
  stroke: footnote-separator-stroke,
)

#let title-page-state = state("cyhs-template-title-page", 1)
#let page-number-footer = context {
  let current-page = counter(page).get().at(0)
  let title-page = title-page-state.get()
  if current-page != title-page {
    align(center)[
      #text(size: small-size)[#counter(page).display("1 / 1", both: true)]
    ]
  }
}

// === 1. Locale ===

#let locale(language: "zh") = {
  if language == "en" {
    (
      key: "en",
      text-lang: "en",
      outline-title: [Contents],
      abstract-title: [Abstract],
      keywords-title: [Keywords],
      bibliography-title: [References],
      keywords-separator: [, ],
      keywords-colon: [: ],
      paragraph-indent: 0em,
    )
  } else {
    (
      key: "zh",
      text-lang: "zh",
      outline-title: [目录],
      abstract-title: [摘要],
      keywords-title: [关键词],
      bibliography-title: [参考文献],
      keywords-separator: [；],
      keywords-colon: [：],
      paragraph-indent: 2em,
    )
  }
}

#let locale-state = state("cyhs-template-locale", locale())

// === 2. Data Constructors ===

#let author(
  name: none,
  affiliation: none,
  affiliation-marker: none,
  email: none,
  note: none,
  marker: "1",
) = (
  name: name,
  affiliation: affiliation,
  affiliation-marker: affiliation-marker,
  email: email,
  note: note,
  marker: marker,
)

// === 3. Global Article Template ===

#let article(
  language: "zh",
  bibliography-style: default-bibliography-style,
  body,
) = {
  let loc = locale(language: language)
  let resolved-indent = if loc.text-lang == "zh" {
    (amount: loc.paragraph-indent, all: false)
  } else {
    loc.paragraph-indent
  }
  let list-indent = loc.paragraph-indent

  // Store the article locale so front-matter helpers can inherit it.
  locale-state.update(loc)

  set page(
    paper: "a4",
    margin: (x: 2.5cm, y: 2cm),
    numbering: "1 / 1",
    number-align: center,
    footer: page-number-footer,
    footer-descent: 12pt,
  )

  set text(
    font: main-fonts,
    lang: loc.text-lang,
    size: font-size,
  )

  set par(
    first-line-indent: resolved-indent,
    justify: true,
    leading: paragraph-leading,
    spacing: paragraph-spacing,
  )

  set list(
    indent: list-indent,
    body-indent: 0.6em,
    spacing: paragraph-leading,
    marker: list-marker,
  )
  set enum(
    indent: list-indent,
    body-indent: 0.6em,
    spacing: paragraph-leading,
    numbering: enum-numbering,
  )

  set table(
    inset: 6pt,
    stroke: color-table-stroke,
  )

  show table: it => {
    set text(size: table-font-size)
    set par(leading: table-leading, spacing: table-leading)
    show strong: set text(font: strong-fonts, size: table-font-size, weight: "bold")
    show raw.where(block: false): raw-it => {
      text(
        font: code-fonts,
        size: table-font-size,
        fill: color-raw-text
      )[#raw-it]
    }
    it
  }

  show figure.where(kind: table): set figure.caption(position: top)

  show figure.caption: set par(leading: 6pt)

  set figure(numbering: "1")
  set heading(numbering: "1.1 ")
  set footnote(numbering: footnote-numbering)
  set footnote.entry(
    separator: footnote-separator,
    clearance: footnote-clearance,
    gap: footnote-gap,
    indent: 0em,
  )
  set strong(delta: 0)
  set std.cite(style: bibliography-style)
  set std.bibliography(style: bibliography-style)

  show std.cite: it => {
    set text(font: "Times New Roman", fill: color-cite-num)
    it
  }

  show strong: set text(font: strong-fonts, size: font-size, weight: "bold")
  show footnote: it => {
    h(footnote-marker-gap)
    set super(size: footnote-marker-size)
    it
  }
  show footnote.entry: it => {
    let loc = it.note.location()
    let mark = numbering(it.note.numbering, ..counter(footnote).at(loc))
    set text(size: footnote-size)
    set par(
      first-line-indent: 0em,
      justify: true,
      leading: footnote-gap,
      spacing: footnote-gap,
    )
    [#mark#footnote-entry-marker-separator]
    it.note.body
  }
  show std.bibliography: it => {
    set text(font: "Times New Roman", lang: "en")
    it
  }

  show heading.where(level: 1): it => {
    set text(font: strong-fonts, size: 16pt, weight: "bold")
    block(above: 28pt, below: 20pt, it)
  }

  show heading.where(level: 2): it => {
    set text(font: strong-fonts, size: 14pt, weight: "bold")
    block(above: 24pt, below: 16pt, it)
  }

  show heading.where(level: 3): it => {
    set text(font: strong-fonts, size: 12pt, weight: "bold")
    block(above: 16pt, below: 14pt, it)
  }

  show raw.where(block: false): it => {
    text(
      font: code-fonts,
      size: font-size,
      fill: color-raw-text
    )[#it]
  }

  show raw.where(block: true): it => {
    block(
      above: paragraph-leading,
      below: paragraph-leading,
      fill: color-raw-bg,
      inset: 12pt,
      radius: 8pt,
      width: 100%,
    )[
      #set text(font: code-fonts, size: small-size)
      #set par(leading: 8pt, spacing: 8pt)
      #it
    ]
  }

  body
}

// === 4. Front Matter Commands ===

#let collect-affiliations(authors) = {
  let entries = ()
  for a in authors {
    if a.affiliation != none {
      let found = false
      for entry in entries {
        let same-marker = a.affiliation-marker != none and entry.marker == a.affiliation-marker
        let same-affiliation = entry.affiliation == a.affiliation
        if same-marker or same-affiliation {
          found = true
        }
      }
      if not found {
        let marker = if a.affiliation-marker != none {
          a.affiliation-marker
        } else {
          str(entries.len() + 1)
        }
        entries.push((marker: marker, affiliation: a.affiliation))
      }
    }
  }
  entries
}

#let affiliation-marker-for(author, affiliations) = {
  if author.affiliation-marker != none {
    author.affiliation-marker
  } else if author.affiliation != none {
    let marker = none
    for entry in affiliations {
      if marker == none and entry.affiliation == author.affiliation {
        marker = entry.marker
      }
    }
    marker
  } else {
    none
  }
}

#let author-email(body) = {
  text(font: code-fonts, size: small-size, fill: luma(0))[#body]
}

#let inline-authors(
  authors: (),
) = context {
  let affiliations = collect-affiliations(authors)
  let email-authors = authors.filter(a => a.email != none)
  let has-explicit-aff-markers = false
  for a in authors {
    if a.affiliation-marker != none {
      has-explicit-aff-markers = true
    }
  }
  let mark-affiliations = affiliations.len() > 1 or has-explicit-aff-markers

  for (i, a) in authors.enumerate() {
    if i > 0 {h(2em)}
    text(font: strong-fonts, weight: "bold")[#a.name]
    let aff-marker = affiliation-marker-for(a, affiliations)
    if mark-affiliations and aff-marker != none {
      h(footnote-marker-gap)
      super[#text(size: font-size)[#aff-marker]]
    }
    if a.note != none {
      footnote(numbering: a.marker)[#a.note]
    }
  }

  if affiliations.len() > 0 [
    #linebreak()
    #set text(size: small-size)
    #for (i, entry) in affiliations.enumerate() {
      if i > 0 {h(2em)}
      if mark-affiliations {
        super[#text(size: small-size)[#entry.marker]]
        h(footnote-marker-gap)
      }
      entry.affiliation
    }
  ]

  if email-authors.len() > 0 [
    #linebreak()
    #set text(size: small-size)
    #for (i, a) in email-authors.enumerate() {
      if i > 0 {h(2em)}
      author-email(a.email)
    }
  ]
}

#let columns-authors(
  authors: (),
) = context {
  let columns = if authors.len() <= 1 {
    (1fr,)
  } else if authors.len() == 2 {
    (1fr, 1fr)
  } else {
    (1fr, 1fr, 1fr)
  }

  let author-body = grid(
    columns: columns,
    column-gutter: 32pt,
    row-gutter: 16pt,
    ..authors.map(a => [
      #set par(first-line-indent: 0em, justify: false, leading: 8pt, spacing: 4pt)
      #text(font: strong-fonts, weight: "bold")[#a.name]
      #if a.note != none [
        #footnote(numbering: a.marker)[#a.note]
      ]
      #if a.affiliation != none [
        #linebreak()
        #set text(size: small-size)
        #a.affiliation
      ]
      #if a.email != none [
        #linebreak()
        #author-email(a.email)
      ]
    ]),
  )

  align(center)[
    #block(width: 84%,)[#author-body]
  ]
}

#let make-title(
  title: none,
  subtitle: none,
  authors: (),
  author-layout: "columns",
) = context {
  let loc = locale-state.get()
  title-page-state.update(counter(page).get().at(0))

  align(center)[
    #v(48pt)

    #if title != none [
      #text(font: strong-fonts, size: 20pt, weight: "bold")[#title]
    ]

    #if subtitle != none [
      #v(8pt)
      #text(size:14pt, fill: luma(80))[#subtitle]
    ]

    #if authors.len() > 0 [
      #v(24pt)
      #if author-layout == "columns" {
        columns-authors(authors: authors)
      } else {
        inline-authors(authors: authors)
      }
      #v(8pt)
    ]
  ]
}

#let make-outline(
  title: auto,
  depth: none,
  indent: auto,
  breakpage: true,
) = context {
  let loc = locale-state.get()
  let resolved-title = if title == auto { loc.outline-title } else { title }

  if breakpage {pagebreak()}
  outline(title: resolved-title, depth: depth, indent: indent)
  if breakpage {pagebreak()}
}

#let abstract(
  title: auto,
  width: 80%,
  body,
) = context {
  let loc = locale-state.get()
  let resolved-title = if title == auto { loc.abstract-title } else { title }

  align(center)[
    #block(
      fill: color-raw-bg,
      inset: (x: 12pt, y: 20pt),
      radius: box-radius,
      width: width,
      above: 20pt,
      below: 20pt,
    )[
      #text(font: strong-fonts, weight: "bold")[#resolved-title]
      #v(4pt)
      #align(left)[#body]
    ]
  ]
}

#let keywords(
  items,
) = context {
  let loc = locale-state.get()
  let title = loc.keywords-title
  let separator = loc.keywords-separator

  align(center)[
    #block(below: 1em)[
      #set par(first-line-indent: 0em, justify: true)
      #text(font: strong-fonts, weight: "bold")[#title#loc.keywords-colon]
      #let res = ""
      #for (i, item) in items.enumerate() {
        if i > 0 {res = res + separator}
        res = res + item
      }
      #res
    ]
  ]
}

#let bibliography(
  sources,
  title: auto,
  full: false,
  newpage: false,
  style: default-bibliography-style,
  lang: "en",
) = context {
  let loc = locale-state.get()
  let resolved-title = if title == auto { loc.bibliography-title } else { title }

  if newpage {pagebreak()} else {v(16pt)}
  
  block[
    #set text(font: "Times New Roman", lang: lang, size: font-size)
    #set par(leading: 7pt, spacing: 7pt)
    #std.bibliography(sources, title: resolved-title, full: full, style: style)
  ]
}

// === 5. Callout Blocks ===

#let key-box(body, width: 100%) = {
  align(center)[
    #block(
      above: paragraph-leading,
      below: paragraph-leading,
      fill: color-key-bg,
      inset: font-size,
      stroke: (left: 2pt + color-key-line),
      width: width,
    )[
      #align(left)[#body]
    ]
  ]
}

#let struct-box(body, title: none, width: 100%) = {
  align(center)[
    #block(
      above: paragraph-leading,
      below: paragraph-leading,
      fill: color-struct-bg,
      inset: font-size,
      stroke: (left: 2pt + color-struct-line),
      width: width,
    )[
      #align(left)[
        #if title != none [
          #text(font: strong-fonts, weight: "bold")[#title]
        ]
        #set enum(indent: 0em)
        #set list(indent: 0em)
        #body
      ]
    ]
  ]
}

#let warn-box(body) = {
  block(
    above: paragraph-leading,
    below: paragraph-leading,
    fill: color-warn-bg,
    inset: 12pt,
    radius: box-radius,
    stroke: color-warn-line,
    width: 100%,
  )[
    #body
  ]
}

// === 6. Utility Rules ===

#let thin-rule() = {
  line(length: 100%, stroke: color-rule)
}

#let colored(color: luma(0), it) = text(fill: color, it)
#let red(it) = text(fill: rgb("#ee0000"), it)
#let blue(it) = text(fill: rgb("#0033ee"), it)
#let green(it) = text(fill: rgb("#11bb33"), it)
#let yellow(it) = text(fill: rgb("#aa9900"), it)
