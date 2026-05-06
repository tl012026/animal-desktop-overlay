## Animal Desktop Overlay

Input an image, extract the animal cutout (transparent PNG), then show it as a frameless always-on-top desktop overlay at a random position.

### Requirements

- Linux desktop session (X11 or Wayland via Qt)
- Python 3.10+

### Install

```bash
cd /home/yl13095/animal-desktop-overlay
# NOTE: on many HPC setups, $HOME has a small quota.
# Prefer putting the venv on /scratch and keep the repo in $HOME.
python -m venv /scratch/yl13095/animal-desktop-overlay/.venv
source /scratch/yl13095/animal-desktop-overlay/.venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### Run

```bash
source .venv/bin/activate
python -m animal_desktop_overlay --image /path/to/input.jpg
```

Optional flags:

```bash
python -m animal_desktop_overlay --image /path/to/input.jpg --scale 0.6 --seed 0
```

### Notes

- Extraction uses `rembg` (U2Net) to remove the background. The result is saved under `./out/`.
- The overlay window is click-through **off** by default (so you can move/close it). Close with `Esc`.

