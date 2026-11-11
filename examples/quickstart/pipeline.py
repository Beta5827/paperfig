"""Ejemplo mínimo de paperfig: pipeline genérico con dos ramas que se fusionan.

Cambia los textos y colores para tu propio sistema. Genera figures/pipeline.{svg,pdf,png}.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))   # no hace falta si se instaló con pip install -e .
from paperfig.svg import SvgDoc, S1, S3, SN, SC, export  # noqa: E402

d = SvgDoc()
d.layer("Pipeline", "pipeline")

# entrada y preprocesamiento
d.rbox(40, 230, 200, 100, SN); d.text(140, 274, ["Raw", "data"], 28, "bold")
d.block_arrow(250, 280, 310, 280, SN)
d.rbox(320, 230, 220, 100, SN); d.text(430, 274, ["Pre-", "processing"], 28, "bold")

# dos ramas
d.block_arrow(545, 250, 615, 175, S1, sw=22, hw=54)
d.block_arrow(545, 310, 615, 385, S3, sw=22, hw=54)
d.text(760, 92, "Feature extractor A", 30, "bold", S1["t"])
d.rbox(640, 120, 240, 100, S1); d.text(760, 165, ["Time-domain", "features"], 23, "bold", S1["t"])
d.text(760, 470, "Feature extractor B", 30, "bold", S3["t"])
d.rbox(640, 340, 240, 100, S3); d.text(760, 385, ["Frequency-domain", "features"], 23, "bold", S3["t"])
d.block_arrow(890, 170, 950, 170, S1)
d.block_arrow(890, 390, 950, 390, S3)
d.vector(965, 110, 36, 120, S1)
d.vector(965, 340, 36, 100, S3)

# fusión (vector concatenado) y modelo
d.line(1001, 170, 1095, 250); d.line(1001, 390, 1095, 320)
d.text(1120, 92, "Fusion", 30, "bold")
d.vector(1100, 175, 36, 120, S1); d.vector(1100, 295, 36, 100, S3)
d.block_arrow(1150, 285, 1210, 285, SC)
d.raw(f'<rect x="1220" y="200" width="220" height="170" rx="34" fill="{SC["f"]}" stroke="#222" stroke-width="3"/>')
d.text(1330, 296, "Classifier", 30, "bold")
d.mlp([1490, 1550, 1610], [[205, 245, 285, 325, 365], [245, 285, 325], [285]], SC)
d.line(1440, 285, 1476, 285, w=2.2)
d.line(1622, 285, 1660, 285, w=2.2)
d.text(1740, 293, "Output", 32, "bold", SC["t"])
d.end()

out = HERE / "figures" / "pipeline.svg"
out.parent.mkdir(exist_ok=True)
d.write(out, 1800, 520, "180mm", "52mm")
export(out)
print("Generado:", out)
