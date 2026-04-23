import time
import rasterio

URLS = [
    f"https://people.math.sc.edu/Burkardt/data/tif/at3_1m4_0{i}.tif" 
    for i in range(1, 8)
]

def run_rasterio():
    print(f"Start Rasterio (sequentially, {len(URLS)} files)...")
    start = time.perf_counter()
    with rasterio.Env(CPL_CURL_VERBOSE=False):
        for url in URLS:
            try:
                with rasterio.open(f"/vsicurl/{url}") as src:
                    _ = src.read(1, window=((0, 100), (0, 100)))
            except Exception as e:
                print(f"Rasterio error on {url}: {e}")
    print(f"Rasterio total: {time.perf_counter() - start:.2f}s")



if __name__ == "__main__":
    run_rasterio()
