import os
import asyncio
import numpy as np
import time
from numba import njit, prange

def get_first_ifd_offset(data):
    endian = '<' if data[0:2] == b'II' else '>'
    version = np.frombuffer(data[2:4], dtype=f'{endian}u2')[0]
    
    if version == 42:
        return int(np.frombuffer(data[4:8], dtype=f'{endian}u4')[0])
    elif version == 43:
        return int(np.frombuffer(data[8:16], dtype=f'{endian}u8')[0])
    return 8

@njit(parallel=True, fastmath=True, error_model='numpy')
def safe_simd_crunch(data):
    total = 0.0
    for i in prange(data.size):
        val = data[i]
        clean_val = val if not np.isnan(val) else 0.0 
        total += clean_val * clean_val
    return total


async def process_full_tiff_numba(file_path):
    try:
        def read_and_compute():
            with open(file_path, 'rb') as f:
                header = f.read(64)
                pixel_offset = get_first_ifd_offset(header)
                
                f.seek(pixel_offset)
                
                pixel_data = f.read()
                
                count = len(pixel_data) // 4
                if count == 0: return 0.0
                
                pixels = np.frombuffer(pixel_data, dtype=np.float32, count=count)
                
                return float(safe_simd_crunch(pixels))

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, read_and_compute)
    except Exception as e:
        return f"Error: {str(e)}"







async def main():
    folder = r""
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.tif')]
    
    print(f"Parsing {len(files)} local files...")
    start = time.perf_counter()
    
    # Запускаем задачи параллельно
    tasks = [process_full_tiff_numba(f) for f in files]
    results = await asyncio.gather(*tasks)
    
    duration = time.perf_counter() - start
    print(f"Total time: {duration:.4f}s")
    print(f"Average: {(duration/len(files))*1000:.3f} ms/file")

if __name__ == "__main__":
    asyncio.run(main())
