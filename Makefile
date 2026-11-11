# Requiere Python 3.9+ y rsvg-convert (librsvg) para exportar PNG/PDF.
PY ?= python3

all: quickstart vibration plots

install:
	$(PY) -m pip install -e .

quickstart:
	$(PY) examples/quickstart/pipeline.py

vibration:
	$(PY) examples/vibration_monitoring/diagram.py

plots:
	$(PY) examples/signal_plots/make_demo_data.py
	$(PY) examples/signal_plots/plot_signals.py

.PHONY: all install quickstart vibration plots
