# FastTIFF Metadata Parser (Numba-Optimized)

A high-performance, asynchronous TIFF header parser designed for extreme-speed scanning of massive datasets. This project demonstrates how a specialized, low-level approach can outperform industry-standard libraries by orders of magnitude.

## 🚀 Performance Benchmarks

Tested on a local dataset of **88 geospatial TIFF files** (SRTM/ASTER GDEM). The results show a definitive leap in efficiency:


| Library | Total Time (88 files) | Avg per File | Performance Gap |
| :--- | :--- | :--- | :--- |
| `tifffile` | 1.300 s | 14.77 ms | Baseline |
| `rasterio` (GDAL) | 0.600 s | 6.81 ms | 2.1x faster |
| **This Parser (Numba + Async)** | **0.020 s** | **0.22 ms** | **30x - 65x faster** |

## 🛠 Technology Stack

The performance breakthrough is achieved through three core strategies:

*   **Numba (JIT Compilation)**: By compiling byte-structure parsing logic into machine code, we eliminate the Python interpreter overhead. The parser operates at near-C speeds while maintaining Python's flexibility.
*   **Zero-Object Overhead**: Standard libraries (`tifffile`, `rasterio`) initialize heavy objects, load drivers, and parse redundant metadata (WKT, OME-XML). This parser uses a "surgical" approach, extracting only the critical bytes needed for indexing.
*   **Async I/O & Low-level OS Calls**: Utilizing `os.pread` (or HTTP Range Requests for remote files) allows for reading only the first 1KB of data. Integrated with an asynchronous event loop, the parser processes files in parallel without blocking.

## 🔍 Why It Wins

While standard libraries are "Swiss Army knives," this parser is a **"Precision Scalpel"**:

*   **Minimal I/O**: We never read the full file; we only target the IFD (Image File Directory) offsets.
*   **Memory Efficiency**: Data flows directly from the buffer to Numba-optimized functions with zero copying.
*   **No Driver Latency**: We bypass the GDAL initialization layer entirely.

## 💻 Quick Start / Example

```python
import asyncio
from your_parser import process_local_file

async def main():
    file_path = "path/to/your/data.tif"
    # Blazing fast metadata extraction
    offset = await process_local_file(file_path)
    print(f"First IFD Offset: {offset}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🗺 Roadmap

The "Numba + Async Byte-Parsing" methodology is being expanded to other industry-standard data formats:

*   **Apache Parquet**: Optimized footer parsing for instant schema discovery.
*   **Zarr**: Micro-second metadata extraction for massive multi-dimensional arrays.

## 💼 Commercial Inquiries

This technology is ideal for Big Data companies, GIS platforms, and Cloud Data Lake providers looking to reduce compute costs and latency.

**Need a commercial license for proprietary software?**  
Contact me: [forlatotskiy@gmail.com](mailto:forlatotskiy@gmail.com)
