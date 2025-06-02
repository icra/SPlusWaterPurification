# Water Purification Plugin for QGIS

## Overview

This QGIS plugin quantifies the **water‑purification ecosystem service** provided by natural landscapes and river channels.
It estimates the capacity of soils, vegetation and channel processes to remove **nitrogen (N)** and **phosphorus (P)**, delivering spatially‑explicit indicators of purification value in both monetary and biophysical terms.

## Key Features

* **Two complementary models**

  * **Landscape model** (`Water Purification (landscape)`): evaluates load reduction across Landscape Spatial Units (LSUs).
  * **Channel model** (`Water Purification (channel)`): evaluates in‑stream load reduction along river reaches.
* **Top‑N ranking approach** – you define how many of the highest‑performing pixels/reaches (parameter `ntop`) are used to calculate mean purification increments.
* **Economic valuation** – converts kg of purified N/P to Euros using life‑cycle cost formulas (CAPEX & OPEX) with user‑supplied discount rate and life expectancy.
* Accepts **SWAT+ spatial outputs** (`*.sqlite`) for baseline and restoration scenarios.
* Produces ready‑to‑map layers (`NitroPurVal_*`, `PhoshPurVal_*`) plus an optional intermediate statistics layer.

## Installation

### From the official QGIS Plugin Repository (recommended)

1. In QGIS, open **Plugins ▸ Manage and Install Plugins…**.
2. Search for **“Water Purification”**.
3. Click **Install Plugin**.

### Manual installation (development copies)

Clone or download this repository into your local QGIS profile’s `python/plugins` directory and restart QGIS.

## Usage

1. Prepare the required input layers/files:

   * `lsus2.shp` – Landscape units (polygons).
   * `rivs1.shp` – Channel network (lines).
   * Baseline SWAT+ `nut*.sqlite`.
   * Restoration SWAT+ `nut*.sqlite`.
2. Launch the model from **Processing ▶ Toolbox ▶ MERLIN**.
3. Fill in parameters:

   | Parameter                                       | Description                                      | Default                 |
   | ----------------------------------------------- | ------------------------------------------------ | ----------------------- |
   | `actualisationrate`                             | Discount rate (decimal)                          | 0.03                    |
   | `lifeexpectancyyears` / `life_expectancy_years` | Asset life (years)                               | 50 (LSU) / 20 (channel) |
   | `ntop`                                          | How many top‑performing cells/reaches to average | 3                       |
   | `yearlyoperationmaintenancecosteurosha`         | O\&M cost (€/ha yr)                              | 3 850                   |
4. Run the model; the plugin writes the outputs to the Processing context and adds them to the map.

## License

This plugin is released under the **MIT License** – see `LICENSE` for details.
