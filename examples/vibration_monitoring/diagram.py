"""Ejemplo: monitoreo de condición de un motor con un clasificador embebido.

Muestra paperfig con dos ramas de características que se fusionan. El espectrograma y los rasgos
estadísticos se CALCULAN a partir de una vibración simulada (paperfig.signals.simulate_vibration).

Genera:
  figures/vibration_paper.{svg,pdf,png}   (180 mm)
  figures/vibration_slide.{svg,pdf,png}   (16:9)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))   # no hace falta si se instaló con pip install -e .
from paperfig.svg import SvgDoc, S1, S3, SN, SC, K, export                 # noqa: E402
from paperfig import icons                                                 # noqa: E402
from paperfig.signals import simulate_vibration, stft_matrix, stat_features  # noqa: E402

OUT = HERE / "figures"
FS = 5000
_, X = simulate_vibration(fs=FS)
SPEC = stft_matrix(X, FS, nperseg=128, fmax=2500)
STATS = stat_features(X[X.size // 2:])          # ventana con fallo


def status_icons(d, x, y):
    d.raw(f'<circle cx="{x}" cy="{y}" r="17" fill="#DDEBD3" stroke="#5B7F3A" stroke-width="2.4"/>'
          f'<path d="M{x-8},{y} l6,6 l11,-12" fill="none" stroke="#3F5F22" stroke-width="3.2" stroke-linecap="round"/>')
    d.raw(f'<path d="M{x+48},{y-17} l18,32 h-36 z" fill="#FBE3CF" stroke="#B5651D" stroke-width="2.4" stroke-linejoin="round"/>'
          f'<line x1="{x+48}" y1="{y-6}" x2="{x+48}" y2="{y+5}" stroke="#9A4A12" stroke-width="3" stroke-linecap="round"/>'
          f'<circle cx="{x+48}" cy="{y+10}" r="2" fill="#9A4A12"/>')


def panel(d):
    d.layer("Pipeline", "pipeline")
    icons.motor_with_sensor(d, 45, 225, w=270)
    icons.burst_trace(d, 85, 450, center=0.7, width=0.2, color="#555")
    d.text(190, 525, ["Vibration", "(simulated)"], 26, "bold")
    d.block_arrow(325, 330, 385, 330, SN)
    d.rbox(395, 285, 200, 90, SN)
    d.text(495, 322, ["Anti-aliasing", "&amp; filters"], 24, "bold", SN["t"])
    d.block_arrow(600, 295, 665, 225, S1, sw=22, hw=54)
    d.block_arrow(600, 365, 665, 435, S3, sw=22, hw=54)
    # rama espectral
    Y1 = 200
    d.text(1060, 92, "Spectral analysis", 30, "bold", S1["t"])
    d.rbox(675, Y1 - 45, 190, 90, S1)
    d.text(770, Y1 - 6, ["Raw signal", "5 kS/s"], 26, "bold", S1["t"])
    d.block_arrow(875, Y1, 935, Y1, S1)
    icons.spectrogram(d, 950, Y1 - 70, SPEC)
    d.text(1048, Y1 + 104, "fault appears at t = 1 s", 22, c=S1["t"], st="italic")
    d.block_arrow(1175, Y1, 1235, Y1, S1)
    d.vector(1250, Y1 - 95, 38, 190, S1)
    d.text(1269, Y1 - 108, "65", 28, "bold", S1["t"])
    # rama estadística
    Y2 = 470
    d.text(1060, Y2 - 110, "Statistical features", 30, "bold", S3["t"])
    d.rbox(675, Y2 - 45, 190, 90, S3)
    d.text(770, Y2 - 6, ["RMS · crest", "kurtosis …"], 24, "bold", S3["t"])
    d.block_arrow(875, Y2, 935, Y2, S3)
    icons.band_bars(d, 950, Y2 - 70, STATS, pad_fill=S3["f"], bar="#93AF78", edge=S3["s"])
    d.text(1048, Y2 + 104, "6 features per window", 22, c=S3["t"], st="italic")
    d.block_arrow(1175, Y2, 1235, Y2, S3)
    d.vector(1250, Y2 - 21, 38, 42, S3)
    d.text(1269, Y2 + 56, "6", 28, "bold", S3["t"])
    # fusión + clasificador
    cx0, cy0, cw0, ch0 = 1400, 235, 190, 200
    d.line(1288, Y1, 1318, 300)
    d.line(1288, Y2, 1318, 372)
    d.vector(1322, 255, 34, 105, S1); d.vector(1322, 360, 34, 22, S3)
    d.text(1339, 240, "fusion", 20, "bold", "#555", st="italic")
    d.line(1358, 318, cx0 - 4, 318, w=2.2)
    d.raw(f'<rect x="{cx0}" y="{cy0}" width="{cw0}" height="{ch0}" rx="34" fill="{SC["f"]}" stroke="{K}" stroke-width="3"/>')
    icons.esp32_board(d, cx0 + 14, cy0 + 22, w=162)
    d.text(cx0 + cw0 / 2, cy0 + 150, ["Edge", "classifier"], 26, "bold")
    d.mlp([1625, 1675, 1725], [[255, 300, 345, 390], [285, 345], [318]], SC, r=10)
    d.line(cx0 + cw0, 318, 1612, 318, w=2.2)
    d.line(1736, 318, 1770, 318, w=2.2)
    d.text(1690, 150, ["Condition", "classifier"], 28, "bold", SC["t"])
    d.text(1680, 495, "Healthy / Fault", 28, "bold", SC["t"])
    status_icons(d, 1656, 545)
    d.end()


def main():
    OUT.mkdir(exist_ok=True)
    d = SvgDoc(); panel(d)
    p = OUT / "vibration_paper.svg"
    d.write(p, 1800, 600, "180mm", "60mm"); export(p)
    d = SvgDoc()
    d.text(960, 110, "Condition monitoring with an embedded classifier", 48, "bold")
    d.group(transform="translate(60,250)"); panel(d); d.end()
    p = OUT / "vibration_slide.svg"
    d.write(p, 1920, 1080, "338.67mm", "190.5mm"); export(p)
    print("Generado en", OUT)


if __name__ == "__main__":
    main()
