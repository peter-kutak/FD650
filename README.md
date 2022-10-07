# FD650
reuse set-top box with display and keys

FD650 is similar to TM1650 (just keys need to be read from address 0x27 not from 0x24)

sleep zhasne display a po stlaceni tlacidla sa rozsvieti (funguje to iba na polovici tlacidiel na mriezke KI1-KI4 and DIG1-DIG4; tlacidlo treba podrzat cez dva cykly)

v 7bit rezime je pin16 dp/kp volny na signalizaciu stlacenia klavesy, takze sa da pripojit na irq pin procesora a citat hodnotu az po stlaceni tlacidla, bez neustaleho citania po zbernici 
- po zapnuti elektriky je tam nula a par dlhych inpulzov (mozno ignorovat)
- po zapnuti zapisom 0x01 na 0x24 tam je 5V (signal 0.1ms 2v / 8ms 5v; prepadlina v signale zodpoveda brightness = cim jasnejsi tym dlhsii cas iba 2v)
- po stlaceni klavesy je tam 0v; pozor ked sa stlaci rovnaka klavesa ako v predoslom kole tak to nezafunguje => nie je mozny dvojklik; takze este treba nieco ved stlacanie rovnakej klavesy je bezne = volume up, nic nepomaha anipnut/zapnut displey, ten je zjavne nezavysly klavesy funguju aj pri vypnutom led; preto to asi nikto nepouziva, ani ja to nemam vyvedene; aj tak potrtrebuju 8bit pre dvojbodku/bodku
- po vycitani stavu z 0x27 sa vrati signal 5v

# connection

| name | notice |
|------|--------|
| +3.3v | 3V - 5.5V |
| SCL | |
| SDA | |
| ir  | IR receiver; -led red |
| stb | 0v when on/stb button pressed |
| lock| +led green |
| GND | red cable |

na plosaku je oznacenie ir<->stb prehodene ale to nedava zmysel; bude to zlozitejsie aby pri vypnutom svietila led a ritom islo zapnut tlacitkom aj dialkovym

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

| bits      | description |
|-----------|-------------|
| xxxx xxxO | On/off      |
| xxxx xxIx | Invalid (must be 0) |
| xxxx xSxx | Sleep       |
| xxxx 7xxx | 7/8-bit (dot segment) |
| xBBB xxxx | Brightness  |
| Ixxx xxxx | Invalid (must be 0) |


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
