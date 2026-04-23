import asyncio
import aiohttp
import numpy as np
import time
from numba import njit

# 1. Сверхбыстрый парсер на Numba
@njit
def get_first_ifd_offset(data):
    # TIFF Header: байты 0-1 (порядок), 2-3 (магия 42), 4-7 (смещение IFD)
    if len(data) < 8:
        return 0
    
    # Проверка Little Endian ('II')
    if data[0] == 73 and data[1] == 73:
        # Собираем uint32 из байтов [4, 5, 6, 7]
        offset = np.uint32(data[4]) | (np.uint32(data[5]) << 8) | \
                 (np.uint32(data[6]) << 16) | (np.uint32(data[7]) << 24)
        return offset
    return 0

# 2. Асинхронное чтение заголовка через Range Request
async def process_file(session, url):
    try:
        # Запрашиваем только самое начало файла
        headers = {"Range": "bytes=0-1023"}
        async with session.get(url, headers=headers, timeout=10) as resp:
            if resp.status not in (200, 206):
                return f"Ошибка HTTP {resp.status}"
            
            chunk = await resp.read()
            # Конвертируем в массив numpy для Numba
            np_data = np.frombuffer(chunk, dtype=np.uint8)
            
            # Парсим смещение
            offset = get_first_ifd_offset(np_data)
            return offset
    except Exception as e:
        return f"Ошибка: {e}"

# 3. Основной цикл
async def main():
    base_url = "https://people.math.sc.edu/Burkardt/data/tif/at3_1m4_0"
    urls = [f"{base_url}{i}.tif" for i in range(1, 8)]
    
    print(f"Начинаю параллельный парсинг {len(urls)} файлов...")
    start = time.perf_counter()
    
    async with aiohttp.ClientSession() as session:
        tasks = [process_file(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    total_time = time.perf_counter() - start
    
    print("\nРезультаты:")
    for url, offset in zip(urls, results):
        print(f"Файл: {url.split('/')[-1]} | Смещение IFD: {offset}")
        
    print(f"\nИтоговое время: {total_time:.4f} сек")

if __name__ == "__main__":
    # Установка: pip install aiohttp numba numpy
    asyncio.run(main())
