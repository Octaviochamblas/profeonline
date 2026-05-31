"""Genera una variante de color del wordmark del logo conservando su forma.

El logo original (`static/img/logo.png`) es un wordmark plano amarillo. Para el
fondo claro del hero necesitamos una variante slate (alto contraste).

Como es un único color plano, no hace falta rediseñar el asset: derivamos una
máscara de "tinta" y la rellenamos con el color destino sobre fondo transparente.
La máscara es robusta tanto si el original es amarillo-sobre-transparente como
amarillo-sobre-blanco (el amarillo #FFD100 tiene azul ~0; el blanco azul ~255).

Uso:
    python scripts/recolor_logo.py SRC DST "#0f172a"
"""
import sys
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "static/img/logo.png"
DST = sys.argv[2] if len(sys.argv) > 2 else "static/img/logo-dark.png"
HEX = (sys.argv[3] if len(sys.argv) > 3 else "#0f172a").lstrip("#")
R, G, B = int(HEX[0:2], 16), int(HEX[2:4], 16), int(HEX[4:6], 16)

im = Image.open(SRC).convert("RGBA")
w, h = im.size
src = im.load()

# ¿El original tiene transparencia real?
has_alpha = False
for y in range(0, h, 5):
    for x in range(0, w, 5):
        if src[x, y][3] < 250:
            has_alpha = True
            break
    if has_alpha:
        break

out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
dst = out.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = src[x, y]
        if has_alpha:
            ink = a
        else:
            # amarillo: azul ~0 -> tinta; blanco: azul ~255 -> fondo
            ink = 255 - b
        dst[x, y] = (R, G, B, ink)

out.save(DST)
print(f"src={SRC} size={w}x{h} has_alpha={has_alpha}")
print(f"-> {DST} fill=#{HEX}")
