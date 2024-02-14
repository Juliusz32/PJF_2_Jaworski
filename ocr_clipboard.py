from PIL import ImageGrab
from PIL import Image
from pynput.mouse import Listener
import pytesseract as tess
import pyperclip

my_config = r'--oem 3 --psm 6 -l pol'
start_x, start_y, end_x, end_y = None, None, None, None
pressed_flag = False
def on_click(x, y, button, pressed):
    global start_x, start_y, end_x, end_y
    global pressed_flag

    if pressed:
        start_x, start_y = x, y
        print(f"Start X: {start_x}, Start Y: {start_y}")
        pressed_flag = True

    else:
        if pressed_flag:
            pressed_flag = False
            end_x, end_y = x, y
            print(f"End X: {end_x}, End Y: {end_y}")
            make_screenshot()
            listener.stop()


def make_screenshot():
    global start_x, start_y, end_x, end_y

    if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
        x1, x2 = start_x, end_x
    else:
        x1, x2 = end_x, start_x

    if start_y < end_y:
        y1, y2 = start_y, end_y
    else:
        y1, y2 = end_y, start_y

    box = (x1, y1, x2, y2)

    screen_shot = ImageGrab.grab(bbox=box)
    screen_shot.save('data/screen_shot.png', 'PNG')
    ocr_from_screen_shot()


def select_box():
    global start_x, start_y, end_x, end_y, listener

    with Listener(on_click=on_click) as listener:
        listener.join()

def ocr_from_screen_shot():
    img = Image.open('data/screen_shot.png')
    text = tess.image_to_string(img, config=my_config)
    pyperclip.copy(text)


