import numpy as np
from PIL import Image
import re
import pytesseract as tess
import os
import csv
import cv2


tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tess.tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
my_config = r'--oem 3 --psm 6 -l pol'


def mark_recognized_data(picture_path):
    img = cv2.imread(picture_path)
    detections = tess.image_to_data(img, output_type=tess.Output.DICT, config=my_config)
    seller_address_flag = True
    seller_nip_flag = True
    seller_regon_flag = True
    seller_bank_flag = True
    seller_account_nr_flag = True
    buyer_address_flag = True
    for i in range(len(detections['text'])):
        if "nr" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i+1], detections['top'][i+1], detections['width'][i+1], detections['height'][i+1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                cv2.putText(img, "Nr faktury:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                invoice_nr = detections['text'][i+1]
                print("nr")
                print(invoice_nr)
        if "miejsce" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                i += 1
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
                detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Miejsce:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                invoice_place = detections['text'][i + 1]
                print(invoice_place)
        if "data" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                i += 1
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
                detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Data:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                invoice_date = detections['text'][i + 1]
                print("data faktury")
                print(invoice_date)
        if "sprzedawca" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                i += 1
                x, y, w, h = detections['left'][i+1], detections['top'][i+1], detections['width'][i+1], detections['height'][i+1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Sprzedawca:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                seller_name = detections['text'][i+1]
                while True:
                    if "adres" in detections['text'][i+3].lower():
                        break
                    x, y, w, h = detections['left'][i + 2], detections['top'][i + 2], detections['width'][i + 2], detections['height'][i + 2]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    seller_name = seller_name + " " + detections['text'][i+2]
                    i += 1
                print("sprzedawca")
                print(seller_name)
        if "adres" in detections['text'][i].lower() and seller_address_flag:
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i+1], detections['top'][i+1], detections['width'][i+1], detections['height'][i+1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "adres:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                seller_address = detections['text'][i+1]
                seller_address_flag = False
                while True:
                    if "nip" in detections['text'][i+3].lower():
                        break
                    x, y, w, h = detections['left'][i+2], detections['top'][i+2], detections['width'][i+2], detections['height'][i+2]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    seller_address = seller_address + " " + detections['text'][i+2]
                    i += 1
                parts = seller_address.split()
                postal_code_index = -1
                for j, part in enumerate(parts):
                    if "-" in part and len(part) == 6:
                        postal_code_index = j
                        break
                seller_address = " ".join(parts[:postal_code_index])
                seller_postal_code = parts[postal_code_index]
                seller_city = " ".join(parts[postal_code_index + 1:])
                print("adres sprzedawcy")
                print(seller_postal_code)
                print(seller_city)
                print(seller_address)
        if "nip" in detections['text'][i].lower() and seller_nip_flag:
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
                detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "NIP:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                seller_nip = detections['text'][i + 1]
                print("nip sprzedawcy")
                print(seller_nip)
                seller_nip_flag = False
        if "regon" in detections['text'][i].lower() and seller_regon_flag:
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
                detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "REGON:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                seller_regon = detections['text'][i + 1]
                print("regon sprzedawcy")
                print(seller_regon)
                seller_regon_flag = False
        if "bank" in detections['text'][i].lower() and seller_bank_flag:
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
                detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "bank:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                seller_bank = detections['text'][i + 1]
                print("bank sprzedawcy")
                print(seller_bank)
                seller_bank_flag = False
        if "konto" in detections['text'][i].lower() and seller_account_nr_flag:
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
                detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "konto:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                seller_account_nr = detections['text'][i + 1]
                print("sprzedawca konto")
                print(seller_account_nr)
                seller_account_nr_flag = False
        if "forma" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                i = i + 1
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "platnosc:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                payment_method = detections['text'][i + 1]
                print("metoda płatnosci")
                print(payment_method)
        if "nabywca" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                i += 3
                x, y, w, h = detections['left'][i+1], detections['top'][i+1], detections['width'][i+1], detections['height'][i+1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Nabywca:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                buyer_name = detections['text'][i+1]
                while True:
                    if "adres" in detections['text'][i+3].lower():
                        break
                    x, y, w, h = detections['left'][i + 2], detections['top'][i + 2], detections['width'][i + 2], detections['height'][i + 2]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    buyer_name = seller_name + " " + detections['text'][i+2]
                    i += 1
                print("kupujacy")
                print(buyer_name)
        if "adres" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i+1], detections['top'][i+1], detections['width'][i+1], detections['height'][i+1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "adres:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                buyer_address = detections['text'][i+1]
                while True:
                    if "nip" in detections['text'][i+3].lower():
                        break
                    x, y, w, h = detections['left'][i+2], detections['top'][i+2], detections['width'][i+2], detections['height'][i+2]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    buyer_address = buyer_address + " " + detections['text'][i+2]
                    i += 1
                parts = buyer_address.split()
                postal_code_index = -1
                for j, part in enumerate(parts):
                    if "-" in part and len(part) == 6:
                        postal_code_index = j
                        break
                buyer_address = " ".join(parts[:postal_code_index])
                buyer_postal_code = parts[postal_code_index]
                buyer_city = " ".join(parts[postal_code_index + 1:])
                print("adres sprzedawcy")
                print(buyer_postal_code)
                print(buyer_city)
                print(buyer_address)
        if "nip" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
                detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "NIP:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                buyer_nip = detections['text'][i + 1]
                print("nip sprzedawcy")
                print(buyer_nip)
        if "regon" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
                detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "REGON:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                buyer_regon = detections['text'][i + 1]
                print("regon sprzedawcy")
                print(buyer_regon)
    data_dict = {
        "invoice_nr": invoice_nr or "brak",
        "invoice_place": invoice_place or "brak",
        "invoice_date": invoice_date or "brak",
        "payment_method": payment_method or "brak",
        "seller_name": seller_name or "brak",
        "seller_adress": seller_address or "brak",
        "seller_postal_code": seller_postal_code or "brak",
        "seller_city": seller_city or "brak",
        "seller_nip": seller_nip or "brak",
        "seller_regon": seller_regon or "brak",
        "seller_bank": seller_bank or "brak",
        "seller_account_nr": seller_account_nr or "brak",
        "buyer_name": buyer_name or "brak",
        "buyer_adress": buyer_address or "brak",
        "buyer_postal_code": buyer_postal_code or "brak",
        "buyer_city": buyer_city or "brak",
        "buyer_nip": buyer_nip or "brak",
        "buyer_regon": buyer_regon or "brak",
    }

    data_directory = "data"
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    csv_file_path = os.path.join(data_directory, 'saved_fill_data_from_pic.csv')

    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())
        csv_writer.writeheader()
        csv_writer.writerow(data_dict)
    cv2.imwrite('data/recognized_text.jpg', img)














