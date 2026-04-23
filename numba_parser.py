import asyncio
import aiohttp
import numpy as np
import time
from numba import njit

@njit
def get_first_ifd_offset(data):
    if len(data) < 8:
        return 0
    
    if data[0] == 73 and data[1] == 73:
        offset = np.uint32(data[4]) | (np.uint32(data[5]) << 8) | \
                 (np.uint32(data[6]) << 16) | (np.uint32(data[7]) << 24)
        return offset
    return 0

async def process_file(session, url):
    try:
        headers = {"Range": "bytes=0-1023"}
        async with session.get(url, headers=headers, timeout=10) as resp:
            if resp.status not in (200, 206):
                return f"HTTP error {resp.status}"
            
            chunk = await resp.read()
            np_data = np.frombuffer(chunk, dtype=np.uint8)
            
            offset = get_first_ifd_offset(np_data)
            return offset
    except Exception as e:
        return f"Error: {e}"

async def main():
    base_url = "https://people.math.sc.edu/Burkardt/data/tif/at3_1m4_0"
    urls = [f"{base_url}{i}.tif" for i in range(1, 8)]
    
    print(f"Starting parallel parsing of {len(urls)} files...")
    start = time.perf_counter()
    
    async with aiohttp.ClientSession() as session:
        tasks = [process_file(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    total_time = time.perf_counter() - start
    
    print("\nResult:")
    for url, offset in zip(urls, results):
        print(f"File: {url.split('/')[-1]} | IFD offset: {offset}")
        
    print(f"\nTotal time: {total_time:.4f} сек")

if __name__ == "__main__":
    asyncio.run(main())
