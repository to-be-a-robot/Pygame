# Rocks On My Head

A 2D space survival arcade game built with Python and Pygame. Control a spacecraft at the bottom of the screen, dodge waves of falling asteroids, and survive for as long as possible as the barrage speeds up.

## Features

- **Pixel-Perfect Collision Detection:** Uses `pygame.mask` overlap checks rather than loose bounding boxes, ensuring hits only register when visible sprite pixels intersect.
- **Dynamic JPG Transparency:** Custom image preprocessing via Pillow (`PIL`) that strips solid backgrounds from JPEG sprites at runtime based on corner color sampling and tolerance thresholds.
- **Progressive Difficulty Scaling:** Asteroid spawn intervals dynamically decrease over time (from 2000 ms down to a frantic 200 ms floor).
- **Multi-Hazard Spawns:** Asteroids rain down in batches across randomized screen coordinates.
- **Survival Timer & End Screen:** Tracks total seconds survived and displays a final game-over report.

## Tech Stack

- **Python 3.8+**
- **Pygame** — Game loop, rendering, input handling, and mask collisions
- **Pillow (PIL)** — Runtime asset processing and color-key transparency

## Getting Started

### Prerequisites

Make sure you have Python installed, then install the dependencies:

```bash
pip install pygame pillow
