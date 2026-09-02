import os 
import asyncio 
import numpy as np 
import time 
from numba import njit, prange, float64, uint8
from pathlib import Path

def get_first_ifd_offset(data): 
    endian = '<' if data[0:2] == b'II' else '>' 
    version = np.frombuffer(data[2:4], dtype=f'{endian}u2')[0] 
    if version == 42: 
        return int(np.frombuffer(data[4:8], dtype=f'{endian}u4')[0]) 
    elif version == 43: 
        return int(np.frombuffer(data[8:16], dtype=f'{endian}u8')[0]) 
    return 8


@njit(float64(uint8[::1]), parallel=True, fastmath=True, error_model='numpy') 
def safe_simd_crunch_uint8(data_uint8): 
    total = 0.0 
    size = data_uint8.size 
    for i in prange(size): 
        val = float(data_uint8[i]) 
        total += val * val 
    return total

async def process_full_tiff_numba(file_path):
    try:
        def read_and_compute():
            with open(file_path, 'rb') as f:
                header = f.read(64)
                if len(header) < 64:
                    return 0.0
                
                pixel_offset = get_first_ifd_offset(header)
                
                f.seek(pixel_offset)
                pixel_data = f.read()
                if not pixel_data:
                    return 0.0
                
                pixels = np.frombuffer(pixel_data, dtype=np.uint8).copy()
                
            return float(safe_simd_crunch_uint8(pixels))

        loop = asyncio.get_running_loop() 
        return await loop.run_in_executor(None, read_and_compute)
    except Exception as e:
        return f"Error: {e}" 

DATA_PATH = Path(__file__).resolve().parent / "tiff_example"

def get_file_list():
    if not DATA_PATH.exists():
        print(f"Error: Directory {DATA_PATH} not found!")
        return []
    return [str(f) for f in DATA_PATH.glob('*.tiff')]

async def main(): 
    warmup_data = np.zeros(10, dtype=np.uint8) 
    safe_simd_crunch_uint8(warmup_data) 
    
    all_files = get_file_list()
    if not all_files:
        print("No files found.")
        return

    print(f"Parsing {len(all_files)} local files with pre-compiled Numba (uint8)...")
    
    start = time.perf_counter()

    tasks = [process_full_tiff_numba(f) for f in all_files]
    results = await asyncio.gather(*tasks)

    duration = time.perf_counter() - start
    
    errors = [r for r in results if isinstance(r, str)]
    if errors:
        print(f"Warning! Errors during reading: {errors}")

    print(f"Total time: {duration:.4f}s")
    print(f"Average: {(duration/len(all_files))*1000:.3f} ms/file")

if __name__ == "__main__": 
    asyncio.run(main())
