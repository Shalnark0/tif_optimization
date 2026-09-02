import time
import asyncio
import tifffile
import rasterio
import numpy as np
from tiff_numba_parser import process_full_tiff_numba, safe_simd_crunch_uint8
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "tiff_example"

def get_file_list():
    if not DATA_PATH.exists():
        print(f"Error: Directory {DATA_PATH} not found!")
        return []
    return [str(f) for f in DATA_PATH.glob('*.tiff')]

def benchmark_tifffile(files):
    start = time.perf_counter()
    count = 0
    for f in files:
        try:
            with tifffile.TiffFile(f) as tif:
                data = tif.asarray()
                res = np.sum(np.square(data.astype(np.float64)))
                count += 1
        except Exception as e: 
            print(f"Tifffile error on {Path(f).name}: {e}") 
            continue
    return time.perf_counter() - start, count

def benchmark_rasterio(files):
    start = time.perf_counter()
    count = 0
    for f in files:
        try:
            with rasterio.open(f) as src:
                data = src.read(1)
                res = np.sum(np.square(data.astype(np.float64)))
                count += 1
        except Exception as e: 
            print(f"Rasterio error on {Path(f).name}: {e}") 
            continue
    return time.perf_counter() - start, count

async def benchmark_my_tech(files):
    safe_simd_crunch_uint8(np.zeros(10, dtype=np.uint8))
    start = time.perf_counter()
    tasks = [process_full_tiff_numba(f) for f in files]
    results = await asyncio.gather(*tasks)
    
    errors = [r for r in results if isinstance(r, str) and "Error" in r]
    if errors:
        print(f"Parser failed on {len(errors)} files. First error example: {errors[0]}")
            
    success_count = sum(1 for r in results if not isinstance(r, str))
    return time.perf_counter() - start, success_count

if __name__ == "__main__":
    all_files = get_file_list()
    print(f"Found files: {len(all_files)}")
    
    if not all_files:
        print("Files not found")
    else:
        t_tiff, c_tiff = benchmark_tifffile(all_files)
        print(f"Tifffile: {t_tiff:.4f} sec (success: {c_tiff})")
        
        t_rast, c_rast = benchmark_rasterio(all_files)
        print(f"Rasterio: {t_rast:.4f} sec (success: {c_rast})")
        
        t_my, c_my = asyncio.run(benchmark_my_tech(all_files))
        print(f"Technology: {t_my:.4f} sec (success: {c_my})")
        
        print("\n" + "="*30)
        print(f"AVERAGE TIME ON FILE:")
        print(f"Tifffile:  {(t_tiff/c_tiff)*1000 if c_tiff else 0:7.2f} ms")
        print(f"Rasterio:  {(t_rast/c_rast)*1000 if c_rast else 0:7.2f} ms")
        print(f"Technology:  {(t_my/c_my)*1000 if c_my else 0:7.2f} ms")
        print("="*30)
        if t_my > 0:
            print(f"Advantage: {t_rast/t_my:.1f} times faster than rasterio")

