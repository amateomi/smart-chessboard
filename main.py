import RPi.GPIO as GPIO
import time

MUX_OUT = 16
MUX_ADDR = [11, 13, 15, 29, 31, 33]

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MUX_OUT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(MUX_ADDR[0], GPIO.OUT)
GPIO.setup(MUX_ADDR[1], GPIO.OUT)
GPIO.setup(MUX_ADDR[2], GPIO.OUT)
GPIO.setup(MUX_ADDR[3], GPIO.OUT)
GPIO.setup(MUX_ADDR[4], GPIO.OUT)
GPIO.setup(MUX_ADDR[5], GPIO.OUT)


try:
    while True:
        for addr in range(64):
            
            addr_str = f'{addr:06b}'[::-1]
            for i in range(6):
                GPIO.output(MUX_ADDR[i], int(addr_str[i]))
                
            value = GPIO.input(MUX_OUT)
            if value == GPIO.HIGH:
                t = time.localtime()
                print(f'{time.strftime("%H:%M:%S", t)} {addr}')
        time.sleep(0.25)
        
except KeyboardInterrupt:
    print("End")
    GPIO.cleanup()
