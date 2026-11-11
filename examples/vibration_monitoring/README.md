# Ejemplo: monitoreo de condición de un motor

Diagrama de un sistema de mantenimiento predictivo: un acelerómetro en el motor, acondicionamiento de señal,
dos ramas de características (espectral y estadística) que se fusionan y un clasificador embebido que
decide *Healthy / Fault*.

- `diagram.py` → `figures/vibration_paper.*` (180 mm) y `figures/vibration_slide.*` (16:9).
- El espectrograma y las barras se **calculan** con `paperfig.signals.simulate_vibration()`: armónicos del
  eje (25 Hz), engrane (600 Hz) e impactos de un fallo de rodamiento que excitan una resonancia (1.8 kHz)
  a partir de t = 1 s. Es un ejemplo ilustrativo con datos sintéticos.
