"""Primitivas SVG para diagramas estilo paper (editables en Inkscape)."""
import math
import subprocess
from pathlib import Path

FONT = "font-family:Arial,Helvetica,'Liberation Sans',sans-serif"
K = "#222222"

# Paleta: un color por ruta. f=relleno, s=borde, t=texto/título, d=inicio del degradado de flechas
S1 = dict(f="#FBE3CF", s="#B5651D", t="#9A4A12", d="#C98A55")  # ruta 1 (naranja)
S2 = dict(f="#D6E6F5", s="#2F6DA8", t="#1F4E89", d="#6E9CC8")  # ruta 2 (azul)
S3 = dict(f="#DDEBD3", s="#5B7F3A", t="#3F5F22", d="#93AF78")  # ruta 3 (verde)
S4 = dict(f="#FBF0C9", s="#A8862A", t="#7A6012", d="#C9AE5E")  # ruta 4 (amarillo)
SN = dict(f="#ECECEC", s="#4D4D4D", t="#222222", d="#9A9A9A")  # compartido / neutro
SC = dict(f="#E6DAEC", s="#5B2C6F", t="#4A235A", d="#9C7BAA")  # modelo / salida
ACC = "#7B1F1F"                                                # lazos punteados


class SvgDoc:
    """Acumula elementos SVG y definiciones (degradados) y escribe el archivo."""

    def __init__(self):
        self.items, self.defs = [], []
        self._n = 0

    # ---------- básicos ----------
    def raw(self, s):
        self.items.append(s)

    def uid(self, prefix="id"):
        self._n += 1
        return f"{prefix}{self._n}"

    def layer(self, name, id_):
        self.raw(f'<g inkscape:groupmode="layer" inkscape:label="{name}" id="{id_}">')

    def group(self, id_=None, transform=None):
        attrs = (f' id="{id_}"' if id_ else "") + (f' transform="{transform}"' if transform else "")
        self.raw(f"<g{attrs}>")

    def end(self):
        self.raw("</g>")

    def text(self, x, y, lines, s=28, w="normal", c=K, an="middle", st="normal"):
        if isinstance(lines, str):
            lines = [lines]
        r = (f'<text x="{x}" y="{y}" style="{FONT};font-size:{s}px;font-weight:{w};'
             f'font-style:{st};fill:{c};text-anchor:{an}">')
        for i, l in enumerate(lines):
            r += f'<tspan x="{x}" dy="{0 if i == 0 else round(s * 1.2, 1)}">{l}</tspan>'
        self.raw(r + "</text>")

    def rbox(self, x, y, w, h, st, r=34, sw=3, stroke=None):
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{st["f"]}" '
                 f'stroke="{stroke or st["s"]}" stroke-width="{sw}"/>')

    def line(self, x1, y1, x2, y2, c=K, w=2.6, dash=None, marker="aK"):
        self.raw(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{c}" stroke-width="{w}" fill="none"'
                 + (f' stroke-dasharray="{dash}"' if dash else "")
                 + (f' marker-end="url(#{marker})"' if marker else "") + "/>")

    def path(self, d, c=K, w=2.6, fill="none", dash=None, marker=None):
        self.raw(f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{fill}" stroke-linejoin="round"'
                 + (f' stroke-dasharray="{dash}"' if dash else "")
                 + (f' marker-end="url(#{marker})"' if marker else "") + "/>")

    def lingrad(self, c0, c1, vertical=False):
        gid = self.uid("g")
        x2, y2 = ("0", "1") if vertical else ("1", "0")
        self.defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
                         f'<stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>')
        return gid

    # ---------- elementos de estilo ----------
    def block_arrow(self, x1, y1, x2, y2, st, sw=20, hw=50, hl=38):
        """Flecha gruesa con degradado st['d'] -> st['f'], en cualquier ángulo."""
        gid = self.lingrad(st["d"], st["f"])
        L = math.hypot(x2 - x1, y2 - y1)
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        b = L - hl
        p = f"M0,{-sw/2} L{b},{-sw/2} L{b},{-hw/2} L{L},0 L{b},{hw/2} L{b},{sw/2} L0,{sw/2} Z"
        self.raw(f'<path transform="translate({x1},{y1}) rotate({ang})" d="{p}" fill="url(#{gid})" '
                 f'stroke="#333" stroke-width="1.6" stroke-linejoin="round"/>')

    def vector(self, x, y, w, h, st):
        """Vector de características (barra)."""
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{st["f"]}" stroke="{K}" stroke-width="2.6"/>')

    def segmented_vector(self, x, y, n, c0, c1, cw=10, h=44):
        """Vector horizontal de n celdas con degradado c0 -> c1 (tuplas RGB)."""
        for k in range(n):
            t = k / max(1, n - 1)
            c = tuple(int(c0[q] + (c1[q] - c0[q]) * t) for q in range(3))
            self.raw(f'<rect x="{x + k * cw}" y="{y}" width="{cw}" height="{h}" fill="rgb{c}" '
                     f'stroke="#ffffff" stroke-width="0.8"/>')
        self.raw(f'<rect x="{x}" y="{y}" width="{n * cw}" height="{h}" fill="none" stroke="{K}" stroke-width="2.6"/>')

    def mlp(self, xs, layers_y, st, r=11):
        for li in range(len(layers_y) - 1):
            for y1 in layers_y[li]:
                for y2 in layers_y[li + 1]:
                    self.raw(f'<line x1="{xs[li]}" y1="{y1}" x2="{xs[li + 1]}" y2="{y2}" stroke="#333" stroke-width="1.2"/>')
        for li, ys in enumerate(layers_y):
            for yy in ys:
                self.raw(f'<circle cx="{xs[li]}" cy="{yy}" r="{r}" fill="{st["f"]}" stroke="#555" stroke-width="2"/>')

    # ---------- salida ----------
    def write(self, path, W, H, width, height, background="#ffffff"):
        """width/height con unidades. Paper: '180mm' x alto; slide 16:9: '338.67mm' x '190.5mm' (W,H=1920,1080)."""
        def marker(id_, c):
            return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
                    f'orient="auto"><path d="M0,1 L10,5 L0,9 z" fill="{c}"/></marker>')
        head = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
                f'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" '
                f'width="{width}" height="{height}" viewBox="0 0 {W} {H}">\n'
                f'<sodipodi:namedview pagecolor="#ffffff" inkscape:document-units="mm"/>\n'
                f'<defs>{"".join(self.defs)}{marker("aK", K)}{marker("aG", "#888")}{marker("aR", ACC)}</defs>\n'
                f'<g inkscape:groupmode="layer" inkscape:label="Fondo" id="fondo">'
                f'<rect width="{W}" height="{H}" fill="{background}"/></g>\n')
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(head + "\n".join(self.items) + "\n</svg>\n")


def export(svg_path, png_width=None):
    """Convierte un SVG a PNG y PDF con rsvg-convert (librsvg).

    png_width por defecto: 3840 px para diapositivas 16:9 (nombre con 'slide'), 1800 px en otro caso.
    """
    svg_path = Path(svg_path)
    w = png_width or (3840 if "slide" in svg_path.stem else 1800)
    subprocess.run(["rsvg-convert", "-w", str(w), str(svg_path), "-o", str(svg_path.with_suffix(".png"))], check=True)
    subprocess.run(["rsvg-convert", "-f", "pdf", str(svg_path), "-o", str(svg_path.with_suffix(".pdf"))], check=True)
