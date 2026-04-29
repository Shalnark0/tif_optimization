import tifffile
import numpy as np

def generate_test_tiffs():
    data = np.random.randint(0, 255, (5000, 5000), dtype=np.uint8)

    tifffile.imwrite('test_bigtiff.tif', data, bigtiff=True)
    print("BigTIFF создан.")

    tifffile.imwrite('test_lzw.tif', data, compression='lzw')
    print("LZW TIFF создан.")

    tifffile.imwrite('test_multipage.tif', [data, data])
    print("Multipage TIFF создан.")

generate_test_tiffs()
