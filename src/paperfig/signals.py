"""Señales de ejemplo y extracción de características para ilustrar diagramas.

- simulate_vibration: vibración de un motor (armónicos del eje, engranes y fallo de rodamiento).
- stft_matrix: |STFT| promediada en una rejilla, lista para icons.spectrogram.
- band_levels: niveles por banda (banco de filtros logarítmico), listo para icons.band_bars.
- stat_features: rasgos estadísticos normalizados, listos para icons.band_bars.
"""
import numpy as np
from scipy import signal, stats


def simulate_vibration(fs=5000, dur=2.0, f_shaft=25.0, f_mesh=600.0, f_res=1800.0, fault_rate=87.0,
                       fault_start=1.0, seed=3):
    """Vibración sintética: armónicos 1x/2x del eje + engrane + impactos periódicos de un fallo de
    rodamiento (excitan una resonancia) a partir de fault_start. Devuelve (t, x)."""
    rng = np.random.default_rng(seed)
    t = np.arange(0, dur, 1 / fs)
    x = (np.sin(2*np.pi*f_shaft*t) + 0.5*np.sin(2*np.pi*2*f_shaft*t) + 0.3*np.sin(2*np.pi*f_mesh*t)
         + 0.15 * rng.standard_normal(t.size))
    imp = np.zeros_like(t)
    for ti in np.arange(fault_start, dur, 1 / fault_rate):
        imp[int(ti * fs)] = 1.0
    h = np.exp(-np.arange(0, 0.01, 1 / fs) * 900) * np.sin(2 * np.pi * f_res * np.arange(0, 0.01, 1 / fs))
    return t, x + 6 * np.convolve(imp, h)[: t.size]


def stft_matrix(x, fs, nperseg=128, fmax=None, grid=(14, 20), gamma=0.8):
    """|STFT| promediada en una rejilla (frecuencia x tiempo) y normalizada a [0, 1]."""
    f, _, Z = signal.stft(x, fs=fs, nperseg=nperseg, noverlap=nperseg // 2)
    S = np.abs(Z)[f <= (fmax or fs / 2)]
    fi = np.array_split(np.arange(S.shape[0]), grid[0])
    ti = np.array_split(np.arange(S.shape[1]), grid[1])
    M = np.array([[S[np.ix_(a, b)].mean() for b in ti] for a in fi])
    return np.clip((M / np.percentile(M, 98)) ** gamma, 0, 1)


def band_levels(x, fs, fmin, fmax, n=7, q=1.5):
    """Nivel RMS por unidad de ancho de banda en n bandas logarítmicas, normalizado a [0, 1]."""
    out = []
    for c in np.geomspace(fmin, fmax, n):
        lo, hi = c / q, min(c * q, fs / 2 * 0.99)
        b, a = signal.butter(2, [lo, hi], btype="band", fs=fs)
        out.append(np.sqrt(np.mean(signal.filtfilt(b, a, x) ** 2) / (hi - lo)))
    out = np.array(out)
    return out / out.max()


def stat_features(x):
    """RMS, pico, factor de cresta, curtosis, desviación estándar y |asimetría|, normalizados a [0, 1]."""
    rms = np.sqrt(np.mean(x**2)); peak = np.max(np.abs(x))
    v = np.array([rms, peak, peak / rms, stats.kurtosis(x, fisher=False), np.std(x), abs(stats.skew(x))])
    return v / v.max()
