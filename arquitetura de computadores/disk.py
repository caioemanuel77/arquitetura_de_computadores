import memory as mem

def read(img):
    disk = open(img, 'rb')
    byte = disk.read(1)
    byte_adress = 0
    while (byte):
        mem.write_byte(byte_adress, int.from_bytes(byte, byteorder='little'))
        byte = disk.read(1)
        byte_adress += 1
    disk.close()