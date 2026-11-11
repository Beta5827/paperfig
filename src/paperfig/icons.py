"""Íconos dibujados a mano (vectoriales, sin dependencias de terceros)."""
import math
from .svg import K

SKIN, SKIN_EDGE = "#F3D2B6", "#A86F45"


def hand(d, x, y, h=118):
    """Mano abierta en tono piel. (x, y) = esquina sup. izq.; h = alto total."""
    s = h / 140
    d.group("mano", f"translate({x},{y + 10*s}) scale({s})")
    d.raw(f'<rect x="14" y="96" width="44" height="34" rx="6" fill="{SKIN}" stroke="{SKIN_EDGE}" stroke-width="2.4"/>')  # muñeca
    for k, (fx, top) in enumerate(((8, 8), (24, -8), (40, -4), (55, 14))):          # dedos
        d.raw(f'<rect x="{fx}" y="{top}" width="14" height="{70-top}" rx="7" fill="{SKIN}" stroke="{SKIN_EDGE}" stroke-width="2.2"/>')
    d.raw(f'<rect x="6" y="50" width="64" height="56" rx="16" fill="{SKIN}" stroke="{SKIN_EDGE}" stroke-width="2.4"/>')     # palma
    d.raw(f'<rect x="-14" y="58" width="15" height="40" rx="7.5" transform="rotate(-38 -6 78)" fill="{SKIN}" stroke="{SKIN_EDGE}" stroke-width="2.2"/>')  # pulgar
    d.end()


def dip8(d, cx, cy, w=110, label="IC"):
    """Circuito integrado DIP-8 centrado en (cx, cy)."""
    h = w * 0.52
    x, y = cx - w / 2, cy - h / 2
    g = d.lingrad("#454545", "#1C1C1C", vertical=True)
    d.group("chip_dip8")
    pw, ph = w * 0.085, h * 0.26
    for k in range(4):
        px = x + w * 0.16 + k * w * 0.225 - pw / 2
        for py in (y - ph * 0.9, y + h - ph * 0.1):
            d.raw(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="1.5" fill="#CFCFCF" stroke="#8A8A8A" stroke-width="1.2"/>')
    d.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="url(#{g})" stroke="#111" stroke-width="1.6"/>')
    d.raw(f'<path d="M{x},{cy - h*0.14} a{h*0.14},{h*0.14} 0 0 1 0,{h*0.28}" fill="#111" stroke="#555" stroke-width="1"/>')
    d.raw(f'<circle cx="{x + w*0.1}" cy="{y + h*0.75}" r="{h*0.06}" fill="#2E2E2E" stroke="#555" stroke-width="0.8"/>')
    d.text(cx + w * 0.04, cy + w * 0.055, label, round(w * 0.15, 1), "bold", "#EDEDED")
    d.end()


def esp32_board(d, x, y, w=164):
    """Placa de desarrollo tipo ESP32 DevKit, horizontal. (x, y) = esquina sup. izq."""
    h = w * 0.5
    d.group("placa_esp32")
    d.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#1D2528" stroke="#0E1214" stroke-width="1.6"/>')
    n = 15
    for k in range(n):                                            # pines
        px = x + w * 0.06 + k * (w * 0.88) / (n - 1)
        for py in (y + h * 0.09, y + h * 0.91):
            d.raw(f'<circle cx="{px}" cy="{py}" r="{w*0.016}" fill="#D9B44A" stroke="#8C6B12" stroke-width="0.8"/>')
    # antena
    ax0, ay0 = x + w * 0.04, y + h * 0.26
    d.raw(f'<rect x="{ax0}" y="{ay0}" width="{w*0.14}" height="{h*0.48}" fill="#16304A" stroke="#0E1214" stroke-width="1"/>')
    mz = " ".join(f"v{(-1)**k * h*0.34} h{w*0.022}" for k in range(5))
    d.raw(f'<path d="M{ax0 + w*0.015},{ay0 + h*0.06} {mz}" fill="none" stroke="#D9B44A" stroke-width="1.4"/>')
    # módulo blindado
    g = d.lingrad("#E4E4E4", "#A9A9A9", vertical=True)
    mx, my, mw, mh = x + w * 0.18, y + h * 0.2, w * 0.42, h * 0.6
    d.raw(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="2" fill="url(#{g})" stroke="#6F6F6F" stroke-width="1.2"/>')
    d.text(mx + mw / 2, my + mh * 0.48, "ESP32", round(w * 0.085, 1), "bold", "#333")
    d.text(mx + mw / 2, my + mh * 0.78, "WROOM-32", round(w * 0.05, 1), "normal", "#555")
    # chips, botones, LED, USB
    d.raw(f'<rect x="{x + w*0.65}" y="{y + h*0.32}" width="{w*0.1}" height="{h*0.2}" fill="#111" stroke="#444" stroke-width="0.8"/>')
    for by in (y + h * 0.24, y + h * 0.62):
        d.raw(f'<rect x="{x + w*0.8}" y="{by}" width="{w*0.06}" height="{h*0.14}" rx="1" fill="#E6E6E6" stroke="#777" stroke-width="0.8"/>'
              f'<circle cx="{x + w*0.83}" cy="{by + h*0.07}" r="{w*0.012}" fill="#555"/>')
    d.raw(f'<circle cx="{x + w*0.7}" cy="{y + h*0.68}" r="{w*0.014}" fill="#E8463A"/>')
    d.raw(f'<rect x="{x + w*0.9}" y="{y + h*0.36}" width="{w*0.12}" height="{h*0.28}" rx="2" fill="#CFCFCF" stroke="#7A7A7A" stroke-width="1.2"/>')
    d.end()


def spectrogram(d, x, y, M, cw=9.8, ch=10, pad_fill="#FBE3CF", c_hi=(150, 70, 15)):
    """Espectrograma vectorial a partir de una matriz M (frecuencia x tiempo) normalizada en [0, 1]."""
    ny, nx = M.shape
    d.group("espectrograma")
    d.raw(f'<rect x="{x-10}" y="{y-10}" width="{nx*cw+20}" height="{ny*ch+20}" rx="8" fill="{pad_fill}"/>')
    for i in range(nx):
        for j in range(ny):
            v = float(M[j, i])
            r = int(255 - (255 - c_hi[0]) * v); g = int(250 - (250 - c_hi[1]) * v); b = int(245 - (245 - c_hi[2]) * v)
            d.raw(f'<rect x="{x + i*cw}" y="{y + (ny-1-j)*ch}" width="{cw+0.3}" height="{ch+0.3}" fill="rgb({r},{g},{b})"/>')
    d.raw(f'<rect x="{x}" y="{y}" width="{nx*cw}" height="{ny*ch}" fill="none" stroke="{K}" stroke-width="2"/>')
    d.end()


def band_bars(d, x, y, levels, pad_fill="#D6E6F5", bar="#7FA9D3", edge="#2F6DA8"):
    """Barras de 7 bandas (niveles en [0, 1]). (x, y) = esquina sup. izq. del área."""
    d.group("bandas")
    d.raw(f'<rect x="{x-10}" y="{y-10}" width="216" height="160" rx="8" fill="{pad_fill}"/>')
    for k, v in enumerate(levels):
        hgt = round(12 + 108 * float(v))
        d.raw(f'<rect x="{x + 10 + k*26}" y="{y + 130 - hgt}" width="19" height="{hgt}" fill="{bar}" stroke="{edge}" stroke-width="1.8"/>')
    d.raw(f'<line x1="{x}" y1="{y+130}" x2="{x+196}" y2="{y+130}" stroke="{K}" stroke-width="2"/>')
    d.end()


def motor_with_sensor(d, x, y, w=260):
    """Motor eléctrico con acelerómetro montado. (x, y) = esquina sup. izq.; alto ≈ 0.62 w."""
    s = w / 260
    X = lambda v: x + v * s
    Y = lambda v: y + v * s
    body = d.lingrad("#D7DCE0", "#8E979E", vertical=True)
    d.group("motor_sensor")
    d.raw(f'<rect x="{X(30)}" y="{Y(140)}" width="{170*s}" height="{18*s}" rx="3" fill="#6D757B" stroke="#3C4246" stroke-width="2"/>')   # base
    d.raw(f'<rect x="{X(55)}" y="{Y(120)}" width="{18*s}" height="{24*s}" fill="#7C858B" stroke="#3C4246" stroke-width="1.6"/>'
          f'<rect x="{X(157)}" y="{Y(120)}" width="{18*s}" height="{24*s}" fill="#7C858B" stroke="#3C4246" stroke-width="1.6"/>')
    d.raw(f'<rect x="{X(30)}" y="{Y(40)}" width="{170*s}" height="{88*s}" rx="{14*s}" fill="url(#{body})" stroke="#3C4246" stroke-width="2.2"/>')
    for k in range(9):                                                                       # aletas
        fx = 48 + k * 17
        d.raw(f'<line x1="{X(fx)}" y1="{Y(46)}" x2="{X(fx)}" y2="{Y(122)}" stroke="#6F787E" stroke-width="2" opacity="0.7"/>')
    d.raw(f'<rect x="{X(200)}" y="{Y(58)}" width="{16*s}" height="{52*s}" rx="4" fill="#A9B1B7" stroke="#3C4246" stroke-width="2"/>')  # tapa
    d.raw(f'<rect x="{X(216)}" y="{Y(78)}" width="{40*s}" height="{12*s}" rx="2" fill="#C9CED2" stroke="#3C4246" stroke-width="1.8"/>')  # eje
    # acelerómetro
    d.raw(f'<rect x="{X(96)}" y="{Y(16)}" width="{40*s}" height="{26*s}" rx="3" fill="#2F6DA8" stroke="#1F3F66" stroke-width="2"/>')
    d.text(X(116), Y(34), "ACC", round(13 * s, 1), "bold", "#ffffff")
    d.raw(f'<path d="M{X(136)},{Y(24)} C{X(170)},{Y(0)} {X(220)},{Y(-6)} {X(255)},{Y(-20)}" stroke="#666" stroke-width="2" fill="none"/>')
    # ondas de vibración
    for k, r in enumerate((14, 24)):
        d.raw(f'<path d="M{X(14 - k*8)},{Y(64 - k*6)} q{-r*0.35*s},{20*s + k*6*s} 0,{40*s + k*12*s}" fill="none" stroke="#B5651D" stroke-width="2" opacity="{0.9 - k*0.3}"/>')
    d.end()


def burst_trace(d, x, y, length=212, amp=26, center=0.5, width=0.18, color="#333"):
    """Trazo de señal con una ráfaga (p. ej. vibración, sonido o actividad eléctrica)."""
    import math as _m
    pts = " ".join(f"{x + t*length/100:.1f},{y + (amp*_m.sin(t*1.9)*_m.exp(-((t/100-center)/width)**2) + 4*_m.sin(t*5.1)):.1f}"
                   for t in range(101))
    d.raw(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/>')
