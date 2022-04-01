# FD650
reuse set-top box with display and keys

FD650 is similar to TM1650 (just keys need to be read from address 0x27 not from 0x24)

# connection

+5v (3V - 5.5V)
SDA
SCL
GND

# linux

connected on i2c bus 1


```bash
# i2cdetect 1                
WARNING! This program can confuse your I2C bus, cause data loss and worse!
I will probe file /dev/i2c-1.
I will probe address range 0x03-0x77.
Continue? [Y/n] 
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: 30 31 32 33 34 35 36 37 -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: 50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --                         
```

## read keys
```bas
watch -n 1 i2cget -y 1 0x27
```

Ctrl+C to exit watch command

## set LEDs mode

+-----------+--------+
| xxxx xxxO | On/off |
+-----------+--------+
| xxxx xSxx | Sleep  |
+-----------+--------+
| xxxx 7xxx | 7/8-bit (dot segment) |
+-----------+--------+
| xBBB xxxx | Brightness |
+-----------+--------+


7-bit data; highest intensity; turned on
```bash
i2cset -y 1 0x24 0x79
```

8-bit data; lowest intensity; turned on
```bash
i2cset -y 1 0x24 0x11
```


## set text on LED

1st digit, segment A
```bash
i2cset -y 1 0x34 0x01
```

2st digit, dot segment (8bit mode)
```bash
i2cset -y 1 0x35 0x80
```

4-th digit; segment G
```bash
i2cset -y 1 0x37 0x40
```

HELO
```bash
i2cset -y 1 0x34 0x76
i2cset -y 1 0x35 0x79
i2cset -y 1 0x36 0x38
i2cset -y 1 0x37 0x3f
```

# linux driver

exists but not tested

https://github.com/arthur-liberman/linux_openvfd/blob/master/driver/controllers/fd650.c


# fremd
https://allenchak.wordpress.com/2020/11/23/tm1650-fd650/

https://github.com/jinzhifeng/SourceCode_old/blob/master/fd650.h
