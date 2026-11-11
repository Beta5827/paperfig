"""Genera data/demo_signals.csv: señales sintéticas para probar las gráficas (500 Hz, 2 s)."""
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent


def main(seed=42, fs=500, dur=2.0):
    rng = np.random.default_rng(seed)
    t = np.arange(0, dur, 1 / fs)
    seno = np.sin(2 * np.pi * 5 * t)
    ruidosa = seno + 0.3 * rng.standard_normal(t.size)
    amortiguada = np.exp(-1.5 * t) * np.cos(2 * np.pi * 8 * t)
    env = np.exp(-((t - 0.6) / 0.15) ** 2) + 0.7 * np.exp(-((t - 1.4) / 0.2) ** 2)
    rafaga = (0.05 + env) * rng.standard_normal(t.size)
    rms = np.sqrt(np.convolve(rafaga**2, np.ones(25) / 25, mode="same"))   # ventana 50 ms
    caminata = np.cumsum(rng.standard_normal(t.size)) * 0.05
    hdr = "tiempo_s,seno_5Hz,seno_ruidoso,coseno_amortiguado,rafaga_simulada,envolvente_RMS,caminata_aleatoria"
    out = HERE / "data" / "demo_signals.csv"
    out.parent.mkdir(exist_ok=True)
    np.savetxt(out, np.column_stack([t, seno, ruidosa, amortiguada, rafaga, rms, caminata]),
               delimiter=",", header=hdr, comments="", fmt="%.5f")
    print("Datos guardados en", out)


if __name__ == "__main__":
    main()
