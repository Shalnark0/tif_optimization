# GeoTIFF Processing Optimization

This project demonstrates a significant performance optimization for extracting data from GeoTIFF files. By improving tile caching and coordinate calculation logic, the processing time was reduced from **55 seconds** to just **0.9 seconds** (a ~60x speedup).

## 🚀 Optimization Overview
The massive performance boost was achieved by bypassing high-level GIS libraries and implementing a low-level approach:

1.  **Numba Integration:** Used JIT (Just-In-Time) compilation with **Numba** to process TIFF data at the byte level. This allows Python to run at near-C++ speeds when iterating over raw buffers.
2.  **Raw Byte Reading:** Instead of using heavy wrappers like `rasterio` or `gdal`, the project reads the TIFF structure directly into memory, significantly reducing overhead.

## 🛠 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com
    cd tif_optimization
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    
    # For Windows:
    .\venv\Scripts\activate
    
    # For Linux/macOS:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

The project contains separate scripts to compare the performance. Run them individually from the root directory:

*   **Original Version (~55.0s):**
    ```bash
    python matrix_test.py
    ```

*   **Optimized Version (~0.9s):**
    ```bash
    python matrix_optimization.py
    ```

## 📊 Benchmark Results


| Version | Processing Time | Performance |
| :--- | :--- | :--- |
| Baseline (Original) | ~55.0 sec | 🐌 Slow |
| **Optimized** | **~0.9 sec** | ⚡ **Fast (60x gain)** |

---
*Developed as part of a TIF data processing optimization study.*
