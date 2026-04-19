"""
heatmap_japan.py
----------------
Generate a temperature area heatmap for Japan using station data
already collected from JMA for the blog post.

Uses:
- scipy.interpolate.griddata  — interpolate sparse station points onto a grid
- geopandas                   — load Japan prefecture boundaries (WGS84 / EPSG:4326)
- matplotlib                  — render and export PNG

Projection: WGS84 equirectangular (EPSG:4326), the geopandas default.
Japan spans 30–46°N; distortion at this latitude is ~22%, acceptable for
a blog heatmap. No cartopy/proj dependency required.

Output: assets/img/posts/japan-heatmap-{year}-{label}.png
"""

import math
import pathlib
import urllib.request

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from scipy.interpolate import griddata

# ---------------------------------------------------------------------------
# Station data (sparse — stations already fetched for the blog post)
# Format: (lat, lon, max_temp_c, label)
# ---------------------------------------------------------------------------

# Peak-day data: 2025-08-05 (national record day, Isesaki 41.8°C)
STATIONS_2025_AUG05 = [
    # Kantō / northern Kanto — the hotspot
    (36.32, 139.20, 41.8, "Isesaki"),
    (36.00, 139.32, 41.4, "Hatoyama"),
    (36.41, 139.33, 41.2, "Kiryu"),
    (36.39, 139.06, 41.0, "Maebashi"),
    (36.15, 139.39, 40.7, "Kumagaya"),
    (36.18, 139.72, 40.6, "Koga"),
    (36.40, 138.90, 40.5, "Kamisatomi"),
    (35.79, 139.24, 40.4, "Ome"),
    (35.67, 139.31, 40.3, "Hachioji"),
    (35.99, 139.08, 40.0, "Chichibu"),
    (35.80, 139.47, 40.0, "Tokorozawa"),
    (35.67, 139.48, 40.0, "Fuchu"),
    # Tokai / Chubu
    (34.97, 138.40, 35.0, "Shizuoka"),  # cooler on Aug 5 (41.4 was Aug 6)
    (35.07, 136.69, 40.5, "Kuwana"),
    (35.17, 136.96, 40.0, "Nagoya"),
    # Kansai
    (34.65, 135.50, 37.0, "Osaka"),
    # Chugoku / Kinki (cooler)
    (34.80, 133.62, 36.0, "Takahashi"),
    (34.60, 132.33, 34.5, "Kake"),
    # Reference stations (approximate Aug 5 values)
    (35.68, 139.69, 37.5, "Tokyo"),
    (37.90, 139.05, 32.0, "Niigata"),
    (36.56, 136.63, 34.0, "Kanazawa"),
    (38.27, 141.02, 30.5, "Sendai"),
    (40.82, 140.74, 28.0, "Aomori"),
    (43.06, 141.35, 27.0, "Sapporo"),
    (31.57, 130.56, 33.0, "Kagoshima"),
    (33.60, 130.42, 33.5, "Fukuoka"),
    (33.84, 132.77, 34.0, "Matsuyama"),
    (26.21, 127.68, 32.5, "Naha"),        # Okinawa — outside main map but anchors south
    (35.30, 135.13, 38.0, "Fukuchiyama"),
    (35.12, 133.88, 36.5, "Kuse"),
]

# Peak-day data: 2024-07-29 (hottest day of 2024, Sano 41.0°C)
STATIONS_2024_JUL29 = [
    (37.20, 139.58, 41.0, "Sano"),
    (36.24, 139.54, 40.2, "Tatebayashi"),
    (36.32, 139.20, 40.1, "Isesaki"),
    (36.15, 139.39, 40.0, "Kumagaya"),
    (36.18, 139.72, 40.0, "Koga"),
    (34.90, 137.82, 40.2, "Tenryu"),
    (34.97, 138.40, 37.0, "Shizuoka"),
    (35.07, 136.69, 37.5, "Kuwana"),
    (35.55, 136.91, 36.0, "Mino"),
    (35.68, 139.69, 37.3, "Tokyo"),
    (34.65, 135.50, 36.4, "Osaka"),
    (35.17, 136.96, 36.0, "Nagoya"),
    (37.90, 139.05, 35.6, "Niigata"),
    (36.56, 136.63, 33.0, "Kanazawa"),
    (38.27, 141.02, 30.0, "Sendai"),
    (40.82, 140.74, 27.5, "Aomori"),
    (43.06, 141.35, 26.0, "Sapporo"),
    (31.57, 130.56, 32.5, "Kagoshima"),
    (33.60, 130.42, 33.0, "Fukuoka"),
    (33.84, 132.77, 33.5, "Matsuyama"),
    (34.80, 133.62, 35.0, "Takahashi"),
    (34.60, 132.33, 33.5, "Kake"),
    (26.21, 127.68, 32.0, "Naha"),
    (35.99, 139.08, 38.0, "Kofu-area"),  # approx from Kofu July data
    (36.39, 139.06, 39.3, "Maebashi"),
    (35.79, 139.24, 36.8, "Ome"),
]

# ---------------------------------------------------------------------------
# Map bounds (excluding Okinawa from main view)
# ---------------------------------------------------------------------------
LON_MIN, LON_MAX = 129.0, 146.0
LAT_MIN, LAT_MAX = 30.5, 45.8
GRID_RES = 0.05   # ~5 km grid cells

JAPAN_GEOJSON = (
    "https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson"
)

# ---------------------------------------------------------------------------
# Color map: white (cool) → yellow → orange → red (hot)
# ---------------------------------------------------------------------------
CMAP = mcolors.LinearSegmentedColormap.from_list(
    "jma_heat",
    [(0.0, "#d0eaf8"),   # ~20°C cool blue-white
     (0.3, "#ffffb2"),   # 29°C yellow
     (0.55, "#fecc5c"),  # 33°C orange-yellow
     (0.72, "#fd8d3c"),  # 36°C orange
     (0.85, "#f03b20"),  # 38.5°C red-orange
     (1.0,  "#bd0026")], # 42°C deep red
)
VMIN, VMAX = 20.0, 42.0


def load_japan_boundary(cache_path: pathlib.Path) -> gpd.GeoDataFrame:
    if not cache_path.exists():
        print(f"  downloading Japan GeoJSON → {cache_path}")
        urllib.request.urlretrieve(JAPAN_GEOJSON, cache_path)
    return gpd.read_file(cache_path)


def make_grid():
    lons = np.arange(LON_MIN, LON_MAX, GRID_RES)
    lats = np.arange(LAT_MIN, LAT_MAX, GRID_RES)
    return np.meshgrid(lons, lats)


def interpolate(stations: list[tuple], grid_lon, grid_lat) -> np.ndarray:
    pts = np.array([(lon, lat) for lat, lon, *_ in stations])
    vals = np.array([t for _, _, t, *_ in stations])
    return griddata(pts, vals, (grid_lon, grid_lat), method="linear")


def render(
    stations: list[tuple],
    gdf: gpd.GeoDataFrame,
    title: str,
    subtitle: str,
    out_path: pathlib.Path,
):
    grid_lon, grid_lat = make_grid()
    temps = interpolate(stations, grid_lon, grid_lat)

    fig, ax = plt.subplots(figsize=(7, 8), dpi=150)
    ax.set_aspect("equal")
    ax.set_xlim(LON_MIN, LON_MAX)
    ax.set_ylim(LAT_MIN, LAT_MAX)
    ax.axis("off")

    # --- interpolated temperature field ---
    mesh = ax.pcolormesh(
        grid_lon, grid_lat, temps,
        cmap=CMAP, vmin=VMIN, vmax=VMAX,
        shading="auto", zorder=1,
    )

    # --- prefecture boundaries ---
    gdf.boundary.plot(ax=ax, color="#555555", linewidth=0.35, zorder=2)

    # --- station dots (only those ≥40°C) ---
    for lat, lon, temp, name in stations:
        if temp >= 40.0:
            ax.plot(lon, lat, "o", ms=5, color="#1a0000",
                    markeredgewidth=0.5, markeredgecolor="white", zorder=4)
            ax.annotate(
                f"{name}\n{temp}°C",
                xy=(lon, lat), xytext=(4, 3), textcoords="offset points",
                fontsize=5.5, color="#1a0000", zorder=5,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", alpha=0.6, lw=0),
            )

    # --- colorbar ---
    cbar = fig.colorbar(mesh, ax=ax, orientation="vertical",
                        fraction=0.025, pad=0.01, shrink=0.6)
    cbar.set_label("Max temperature (°C)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    # --- titles ---
    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.text(0.5, -0.01, subtitle, ha="center", va="top",
            transform=ax.transAxes, fontsize=7, color="#555")
    ax.text(0.5, -0.035, "Source: JMA ETRN · interpolation: scipy.griddata linear",
            ha="center", va="top", transform=ax.transAxes, fontsize=6, color="#888")

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved → {out_path}")


def main():
    repo = pathlib.Path(__file__).parent.parent
    cache = repo / "code" / "_cache_japan.geojson"
    out_dir = repo / "assets" / "img" / "posts"

    print("loading Japan prefecture boundaries …")
    gdf = load_japan_boundary(cache)

    print("rendering 2025-08-05 heatmap …")
    render(
        STATIONS_2025_AUG05, gdf,
        title="Japan Daily Max Temperature — 5 August 2025",
        subtitle="National record: Isesaki (Gunma) 41.8°C  ·  30 JMA stations",
        out_path=out_dir / "japan-heatmap-2025-aug05.png",
    )

    print("rendering 2024-07-29 heatmap …")
    render(
        STATIONS_2024_JUL29, gdf,
        title="Japan Daily Max Temperature — 29 July 2024",
        subtitle="Peak: Sano (Tochigi) 41.0°C  ·  26 JMA stations",
        out_path=out_dir / "japan-heatmap-2024-jul29.png",
    )

    print("done.")


if __name__ == "__main__":
    main()
