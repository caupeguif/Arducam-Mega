import _thread
import time
import sys
import machine
import config
import network
import socket
from time import sleep

""" '320x240'
    '640x480'
    '1280x720'
    '1600x1200'
    '1920x1080'
    '2592x1944'
    '96X96'
    '128X128'
    '320X320' """

cam = Camera(spi, cs)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

while not wifi.isconnected():
    pass

print("Wifi connected")
port = 12345
ip = '192.168.80.43'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
   

R_LED = Pin(46, Pin.OUT)
G_LED = Pin(0, Pin.OUT)
B_LED = Pin(45, Pin.OUT)

#cam.current_resolution = cam.RESOLUTION_640X480
cam.set_pixel_format(cam.CAM_IMAGE_PIX_FMT_JPG)
cam.set_brightness_level(cam.BRIGHTNESS_PLUS_4)
cam.set_contrast(cam.CONTRAST_MINUS_3)

def send_image(s, image_data):
    block_size = 2048
    num_blocks = len(image_data) // block_size + (1 if len(image_data) % block_size != 0 else 0)
    for i in range(num_blocks+1):
        block = image_data[i*block_size:(i+1)*block_size]
        header = f"B:{len(image_data)}:{i}\n"  # Encabezado corregido
        header_encoded = header.encode()
        s.send(header_encoded + block)
        time.sleep(0.1)  # Ajuste en el tiempo de espera
    s.send(b'\n\n')
    print(header_encoded + block)

while True:
    # data = input("Presiona P para tomar una foto o Q para salir: ")
    G_LED.on()
    try:
        data = s.recv(8192)
        print(data)
        if data == b'p':
            R_LED.off()
            start_time_capture = utime.ticks_ms()
            cam.capture_jpg()
            
            raw = cam.save_image_bytes()
            total_time_ms = utime.ticks_diff(utime.ticks_ms(), start_time_capture)
            print(len(raw))
            
            base64_image = cam.convert_to_base64(raw)
            #print(base64_image)
            print(len(base64_image))
            
            time.sleep(0.1)  # Esperar un momento antes de enviar los datos reales de la imagen
            send_image(s, base64_image)
            print('Foto enviada! tiempo de captura: {}s'.format(total_time_ms/1000))
            R_LED.on()
            G_LED.off()
            time.sleep(1)
            base64_image = None
            raw = None
            
    except OSError as e:
        if str(e) == "104":
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
