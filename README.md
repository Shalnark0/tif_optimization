# GeoTIFF Processing Optimization

This project demonstrates a significant performance optimization for extracting data from GeoTIFF files. By improving tile caching and coordinate calculation logic, the processing time was reduced from **55 seconds** to just **0.9 seconds** (a ~60x speedup).

## 🚀 Optimization Overview
The performance boost was achieved through two main strategies:
1.  **Tile Caching:** Instead of frequent disk I/O operations, the algorithm checks if the required coordinates fall within the currently loaded memory tile (`inCurrentTile`).
2.  **Efficient Coordinate Mapping:** Optimized mathematical conversion between geographic degrees and meters using the cosine of the latitude for precise longitude scaling.

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
