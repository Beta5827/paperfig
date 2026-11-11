"""Figura de 3 paneles: (a) señal limpia vs ruidosa, (b) señal con ráfagas + envolvente RMS, (c) espectro FFT.

Uso: python examples/signal_plots/plot_signals.py [ruta.csv]
"""
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))   # no hace falta si se instaló con pip install -e .
from paperfig.plotstyle import PALETTE, apply_publication_style, panel_labels, finalize_figure  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402


def main(csv=HERE / "data" / "demo_signals.csv"):
    d = np.genfromtxt(csv, delimiter=",", names=True)
    t = d["tiempo_s"]
    fs = 1 / np.median(np.diff(t))
    apply_publication_style()
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))

    m = t <= 1.0
    ax[0].plot(t[m], d["seno_ruidoso"][m], color=PALETTE["neutral"], lw=1.6, label="Noisy")
    ax[0].plot(t[m], d["seno_5Hz"][m], color=PALETTE["blue_main"], lw=2.6, label="Clean (5 Hz)")
    ax[0].set(xlabel="Time (s)", ylabel="Amplitude (a.u.)", ylim=(-2.2, 2.2))
    ax[0].legend(loc="upper right", ncol=2, fontsize=13, bbox_to_anchor=(1.0, 1.12))

    ax[1].plot(t, d["rafaga_simulada"], color=PALETTE["gray"], lw=0.9, alpha=0.8, label="Burst signal")
    ax[1].plot(t, d["envolvente_RMS"], color=PALETTE["red_strong"], lw=2.8, label="RMS envelope")
    ax[1].plot(t, -d["envolvente_RMS"], color=PALETTE["red_strong"], lw=2.8)
    ax[1].set(xlabel="Time (s)", ylabel="Amplitude (a.u.)")
    ax[1].legend(loc="upper right", ncol=2, fontsize=13, bbox_to_anchor=(1.0, 1.12))

    x = d["seno_ruidoso"]
    w = np.hanning(x.size)
    X = np.abs(np.fft.rfft(x * w)) * 2 / w.sum()
    f = np.fft.rfftfreq(x.size, 1 / fs)
    ax[2].fill_between(f, X, color=PALETTE["blue_secondary"], alpha=0.18, lw=0)
    ax[2].plot(f, X, color=PALETTE["blue_main"], lw=2.2)
    k = np.argmax(X)
    ax[2].annotate(f"{f[k]:.1f} Hz", xy=(f[k], X[k]), xytext=(f[k] + 12, X[k] * 0.92), fontsize=14,
                   color=PALETTE["blue_main"], arrowprops=dict(arrowstyle="-", color=PALETTE["blue_main"], lw=1.4))
    ax[2].set(xlim=(0, 60), xlabel="Frequency (Hz)", ylabel="|X(f)| (a.u.)")

    panel_labels(ax)
    finalize_figure(fig, HERE / "figures" / "signals_demo")
    print("Figura guardada en", HERE / "figures")


if __name__ == "__main__":
    main(*sys.argv[1:])
