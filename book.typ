#import "cyhs_template.typ": *

#show: article.with(language: "zh")

#let book-heading-numbering(..numbers) = {
  let values = numbers.pos()
  if values.len() == 1 {
    {
      set text(cjk-latin-spacing: none)
      numbering("第1章", ..values)
    } + [ ]
  } else {
    numbering("1.1", ..values) + [ ]
  }
}

#set heading(
  numbering: book-heading-numbering,
  supplement: none,
)
#set math.equation(numbering: "(1)")
#show math.equation: set text(font: "New Computer Modern Math")

#make-title(
  title: [摄影的数学与物理],
  subtitle: [从光子到图像：成像、感知与表达的统一导论],
  authors: (
    author(
      name: [沈照影]
    ),
  ),
)

#abstract[
  摄影可以看成一条从场景光线到最终观看的受限信息链。本书围绕“信息怎样进入系统、在哪里损失、哪些损失可由计算补偿、如何用最小实验验证”来组织数学、物理与计算机原理。内容先从光、投影、理想透镜和景深建立直观成像模型，再进入光的计量、曝光、传感器与噪声；随后讨论衍射、像差、运动、采样、色彩与 RAW 管线，并由布光和视觉明确拍摄与观看目标，最后进入图像复原、AI、多帧、器材选择、色彩管理和归档。

  本书用数学公式用于给出可检验的数量级、条件与边界，但这些不替代审美判断。读者最终应能把虚、糊、噪、过曝、偏色和假细节定位到成像链，用受控实验区分焦距与透视、光圈与衍射、快门与运动、曝光与 ISO、RAW 与 JPEG，并根据目标输出在拍摄和后期之间分配有限余量。
]

#keywords(("摄影科学", "计算成像", "辐射度学", "数字图像", "视觉感知"))

#v(1fr)

#align(center)[
  #text(size: 9pt, fill: luma(80))[Presented in collaboration with ChatGPT · 2026]
]

#make-outline(depth: 2, indent: 2em)

#include "chapters/01-introduction.typ"
#include "chapters/02-light-models.typ"
#include "chapters/03-projective-geometry.typ"
#include "chapters/04-gaussian-optics.typ"
#include "chapters/05-defocus-depth-of-field.typ"
#include "chapters/06-radiometry.typ"
#include "chapters/07-exposure-metering.typ"
#include "chapters/08-sensor-physics.typ"
#include "chapters/09-noise-dynamic-range.typ"
#include "chapters/10-diffraction-aperture.typ"
#include "chapters/11-aberrations-mtf.typ"
#include "chapters/12-motion-stabilization.typ"
#include "chapters/13-sampling-resolution.typ"
#include "chapters/14-colorimetry.typ"
#include "chapters/15-tone-encoding.typ"
#include "chapters/16-raw-pipeline.typ"
#include "chapters/17-lighting-materials.typ"
#include "chapters/18-perception-composition-style.typ"
#include "chapters/19-convolution-restoration.typ"
#include "chapters/20-denoising-ai.typ"
#include "chapters/21-multiframe-computational.typ"
#include "chapters/22-task-based-system-selection.typ"
#include "chapters/23-output-color-archive.typ"
#include "chapters/24-quality-diagnosis-experiments.typ"

#bibliography(
  "references.bib",
  full: true,
  newpage: true,
  lang: "en",
)
