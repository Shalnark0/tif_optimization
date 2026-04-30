# Ultra-Fast Tiff & Raster Processing Engine 🚀

A high-performance computational engine designed to bypass the overhead of standard libraries like `GDAL`, `Rasterio`, and `Tifffile`. By leveraging **Numba JIT**, **SIMD vectorization**, and **Asynchronous I/O**, this parser achieves up to **25x speedup** on legacy hardware.

## 📊 Performance Benchmark

The following benchmark was conducted by processing **90 TIFF files** (including BigTIFF and LZW-compressed samples).


| Library             | Total Time (sec) | Avg. Time per File |
|---------------------|------------------|--------------------|
| Rasterio            | 31.23s           | 347.0 ms           |
| Tifffile            | 50.37s           | 559.6 ms           |
| **Our Technology**  | **1.87s**        | **20.8 ms**        |

> **Note:** Our engine shows an advantage of **16x** over Rasterio and **27x** over Tifffile in "hot" state (post-JIT warmup).

### Hardware Specifications (Legacy Testbed)
- **CPU:** Intel Core i5-4460 @ 3.2 GHz (4 Cores / 4 Threads)
- **RAM:** 8GB DDR3
- **OS:** Windows / Python 3.11

## 🛠 Key Features

- **Zero-Copy Architecture:** Data is interpreted directly from buffers, eliminating redundant memory allocations.
- **Numba JIT Acceleration:** Core math functions are compiled into LLVM machine code with `@njit(fastmath=True)`.
- **Async Execution:** Utilizes `asyncio` and thread executors to prevent I/O blocking during file reads.
- **Hardware-Level Optimization:** Uses SIMD instructions to handle `NaN` values and sum-of-squares calculations without pipeline stalls.

## 📈 Performance Visualization

![Performance Comparison](performance_benchmark.png)

## 💻 Core Logic Overview

Our engine uses a specialized `safe_simd_crunch` function to process pixel data in parallel across all CPU cores:

```python
@njit(parallel=True, fastmath=True, error_model='numpy')
def safe_simd_crunch(data):
    total = 0.0
    for i in prange(data.size):
        val = data[i]
        # Hardware-level NaN handling (no branching)
        clean_val = val if not np.isnan(val) else 0.0 
        total += clean_val * clean_val
    return total
```

## 🚀 How to Run

1. **Install dependencies:**
   ```bash
   pip install numpy numba tifffile rasterio
   ```
2. **Generate test data:**
   ```bash
   python generate_test_tiffs.py
   ```
3. **Run benchmark:**
   ```bash
   python benchmark_tiff.py
   ```

## 🎯 Strategic Impact

This engine is part of a larger mission to replace rigid, outdated GIS/Radar architectures with flexible, high-speed solutions. It is particularly effective for:
- Real-time Signal Analysis.
- Large-scale Geospatial Analytics.
- Embedded systems with limited hardware resources (Robotics/Aerospace).

---
**Author:** [Shalnark0](https://github.com)  
*Senior Software Engineer focusing on high-performance data systems.*
