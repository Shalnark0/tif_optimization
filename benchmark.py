import time
import rasterio
from async_geotiff import GeoTIFF

# Список прямых ссылок на ваши файлы
URLS = [
    f"https://people.math.sc.edu/Burkardt/data/tif/at3_1m4_0{i}.tif" 
    for i in range(1, 8)
]

def run_rasterio():
    print(f"Старт Rasterio (последовательно, {len(URLS)} файлов)...")
    start = time.perf_counter()
    # Для обычных HTTP ссылок включаем настройки сетевого доступа
    with rasterio.Env(CPL_CURL_VERBOSE=False):
        for url in URLS:
            try:
                # В Rasterio для HTTP часто лучше добавлять префикс /vsicurl/
                with rasterio.open(f"/vsicurl/{url}") as src:
                    _ = src.read(1, window=((0, 100), (0, 100)))
            except Exception as e:
                print(f"Ошибка Rasterio на {url}: {e}")
    print(f"Rasterio итого: {time.perf_counter() - start:.2f}s")

async def fetch_async(url):
    try:
        async with GeoTIFF(url) as src:
            # Читаем тот же фрагмент
            return await src.read(window=((0, 100), (0, 100)))
    except Exception as e:
        print(f"Ошибка Async на {url}: {e}")


if __name__ == "__main__":
    run_rasterio()
