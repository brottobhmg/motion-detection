import requests
import cv2
import numpy as np
import time
from io import BytesIO
from find_device import detect_near_device

TELEGRAM_TOKEN = 'YOUR_TOKEN'
CHAT_ID = 'YOUR_CHATID'

request = requests.get("http://esp32.local/ip")
ip = None
if request.status_code != 200:
    print("Error, status code " + str(request.status_code))
    exit(1)
else:
    ip = request.text

IMAGE_URL = 'http://' + ip + '/capture'

def download_image(url):
    try:
        response = requests.get(url)
    except:
        download_image(url)
    image = np.array(bytearray(response.content), dtype=np.uint8)
    return cv2.imdecode(image, cv2.IMREAD_COLOR)

def detect_motion(image1, image2):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    blurred = cv2.GaussianBlur(diff, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
    num_nonzero = np.count_nonzero(thresh)
    return num_nonzero > 10000

def send_image_telegram(image, token, chat_id):
    _, encoded_image = cv2.imencode('.jpg', image)
    image_bytes = encoded_image.tobytes()
    files = {'photo': ('image.jpg', image_bytes, 'image/jpeg')}
    url = f'https://api.telegram.org/bot{token}/sendPhoto'
    payload = {'chat_id': chat_id}
    response = requests.post(url, data=payload, files=files)
    return response

def rotate_image_90_left(image):
    rotated_image = cv2.transpose(image)
    rotated_image = cv2.flip(rotated_image, flipCode=0)  # flipCode=0 per flip verticale
    return rotated_image


def main():
    prev_image = download_image(IMAGE_URL)
    time.sleep(3)
    
    while True:
        current_image = download_image(IMAGE_URL)
        if detect_motion(prev_image, current_image):
            print("Movimento rilevato!")
            if (not(detect_near_device())):
                print("Dispositivo rilevato vicino.")
                response = send_image_telegram(rotate_image_90_left(current_image), TELEGRAM_TOKEN, CHAT_ID)
                if response.status_code == 200:
                    print("Immagine inviata con successo.")
                else:
                    print("Errore nell'invio dell'immagine.")
        
        prev_image = current_image
        time.sleep(5)

if __name__ == "__main__":
    main()
