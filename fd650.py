from smbus import SMBus

m=SMBus(1)
while(True):
  m.write_byte(0x24, 0x71)
  m.write_byte(0x34, 0x01)
  m.write_byte(0x35, 0x02)
  k=m.read_byte(0x27)
  m.write_byte(0x36, 3)
  m.write_byte(0x37, k)
  m.write_byte(0x24, 0x11)
