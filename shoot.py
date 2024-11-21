import sys
cam = Camera(spi, cs)

R_LED = Pin(46, Pin.OUT)
G_LED = Pin(0, Pin.OUT)

cam.resolution = '1280x720'
cam.set_brightness_level(cam.BRIGHTNESS_PLUS_4)
cam.set_contrast(cam.CONTRAST_MINUS_3)
counter = 0

while True:
    caracter = input("Presiona P para tomar una foto o Q para salir: ")
    if caracter.lower() == 'p':
        print("tomando foto...")
        R_LED.off()
        start_time_capture = utime.ticks_ms()
        cam.capture_jpg()
        cam.saveJPG('image' +str(counter) + '.jpg')
        R_LED.on()
        G_LED.off()
        G_LED.on()
        counter += 1
        total_time_ms = utime.ticks_diff(utime.ticks_ms(), start_time_capture)
        print('Time take: {}s'.format(total_time_ms/1000))
    elif caracter.lower() == 'q':
        print("Saliendo del programa.")
        sys.exit()