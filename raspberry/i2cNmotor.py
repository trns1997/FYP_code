import smbus
import RPi.GPIO as IO
import pigpio
""
""
import time
import struct

dutyC = 0

address = 0x0A
bus = smbus.SMBus(1)

"""
IO.cleanup()
IO.setwarnings(False)
IO.setmode(IO.BOARD)
IO.setup(13,IO.OUT)
p = IO.PWM(13,800)
p.start(dutyC)
"""
pi = pigpio.pi()
pi.set_PWM_dutycycle(13,0)
pi.write(19,0)

while True:
    #bus.write_byte(address, 5)
    #data = bus.read_byte(address)
    #print('waiting to add')
    #name = raw_input("")
    
    #dutyC += 1
    #print(dutyC)
    #p.ChangeDutyCycle(dutyC)
    #pi.set_PWM_dutycycle(13,dutyC)
    try:
        pack = bus.read_i2c_block_data(address,0,24)
    except Exception:
        print('GG')
    data = bytes(pack)
    data = struct.unpack("iIfiIf",data)
    print(data[2]-data[5])
    if (data[2]-data[5]<0):
        pi.write(19,0)
    else:
        pi.write(19,1)        
    if (abs(data[2]-data[5]) > 2):
        pi.set_PWM_dutycycle(13,255)
    else:
        pi.set_PWM_dutycycle(13,0)
    time.sleep(0.05)
    
