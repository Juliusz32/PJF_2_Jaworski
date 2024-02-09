from PIL import Image
import re
import pytesseract as tess
import os
import csv
import cv2



tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tess.tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
my_config = r'--oem 3 --psm 6 -l pol'
def image_recognition_back(picture_path):

    img = Image.open(picture_path)
    text = tess.image_to_string(img, config=my_config)


    invoice_nr = re.search(r'Faktura nr\.(\d+)', text).group(1) if re.search(r'Faktura nr\.(\d+)', text) else None
    seller_name = re.search(r'Faktura nr\.\d+\n(.+?)(?:\n|$)', text.replace(' Mechanizm podzielonej płatności', '')).group(1) if re.search(r'Faktura nr\.\d+\n(.+?)(?:\n|$)', text.replace(' Mechanizm podzielonej płatności', '')) else None

    match = re.search(r"Mechanizm podzielonej płatności(.+?)Miejsce wystawienia", text, re.DOTALL)
    seller_adress = match.group(1).strip() if match else ""

    invoice_place = re.search(r'Miejsce wystawienia: (.+)', text).group(1) if re.search(r'Miejsce wystawienia: (.+)',
                                                                                        text) else None
    seller_postal_code = re.search(r'(\d{2}-\d{3})', text).group(1) if re.search(r'(\d{2}-\d{3})', text) else None

    match = re.search(r"(\d{2}-\d{3})\s+(.+?)Data wystawienia", text, re.DOTALL)
    seller_city = match.group(2).strip() if match else ""

    invoice_date = re.search(r'Data wystawienia: (.+)', text).group(1) if re.search(r'Data wystawienia: (.+)',
                                                                                    text) else None
    seller_nip = re.search(r'NIP: (\d+)', text).group(1) if re.search(r'NIP: (\d+)', text) else None
    seller_regon = re.search(r'REGON: (\d+)', text).group(1) if re.search(r'REGON: (\d+)', text) else None
    seller_bank = re.search(r'bank: (.+)', text).group(1) if re.search(r'bank: (.+)', text) else None
    seller_account_nr = re.search(r'konto: (.+)', text).group(1) if re.search(r'konto: (.+)', text) else None

    text_buyer = text.split("Nabywca:")[1]
    lines = text_buyer.split('\n')

    match = re.search(r"(.+?)Forma płatności:przelew", text_buyer, re.DOTALL)
    buyer_name = match.group(1).strip() if match else ""

    match = re.search(r"Forma płatności:(.+)$", text_buyer, re.MULTILINE)
    payment_method = match.group(1).strip() if match else ""

    buyer_address = lines[2].strip() if len(lines) > 1 else ""

    buyer_postal_code = re.search(r'(\d{2}-\d{3})', text_buyer).group(1) if re.search(r'(\d{2}-\d{3})', text) else None

    match = re.search(r"\b\d{2}-\d{3}\s+(.+)$", text_buyer, re.MULTILINE)
    buyer_city = match.group(1).strip() if match else ""

    match = re.search(r"NIP:(.+)$", text_buyer, re.MULTILINE)
    buyer_nip = match.group(1).strip() if match else ""

    match = re.search(r"REGON:(.+)$", text_buyer, re.MULTILINE)
    buyer_regon = match.group(1).strip() if match else ""


    data_dict = {
        "invoice_nr": invoice_nr or "brak",
        "invoice_place": invoice_place or "brak",
        "invoice_date": invoice_date or "brak",
        "payment_method": payment_method or "brak",
        "seller_name": seller_name or "brak",
        "seller_adress": seller_adress or "brak",
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

# def mark_recognized_data(picture_path):
#     img = cv2.imread(picture_path)
#     #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     text = tess.image_to_string(img, config=my_config)
#     detections = tess.image_to_data(img, output_type=tess.Output.DICT)
#     for i in range(len(detections['text'])):
#         # if int(detections['conf'][i]) > 60:
#         #     x, y, w, h = detections['left'][i], detections['top'][i], detections['width'][i], detections['height'][i]
#         #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         #     cv2.putText(img, detections['text'][i], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         if "sprzedawca" in detections['text'][i].lower():
#             next_line_index = i + 1
#             if next_line_index < len(detections['text']):
#                 next_line_x, next_line_y, next_line_w, next_line_h = detections['left'][next_line_index], detections['top'][next_line_index], detections['width'][next_line_index], detections['height'][next_line_index]
#                 cv2.rectangle(img, (next_line_x, next_line_y), (next_line_x + next_line_w, next_line_y + next_line_h), (0, 0, 255), 2)
#                 cv2.putText(img, "Sprzedawca:", (next_line_x, next_line_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 2)
#                 seller_name = detections['text'][i]
#                 print("Seller Name:", seller_name)
#     cv2.imwrite('data/recognized_text.jpg', img)

def mark_recognized_data(picture_path):
    img = cv2.imread(picture_path)
    detections = tess.image_to_data(img, output_type=tess.Output.DICT, config=my_config)
    seller_address_flag = True
    seller_nip_flag = True
    seller_regon_flag = True
    for i in range(len(detections['text'])):
        if "nr" in detections['text'][i].lower():
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i+1], detections['top'][i+1], detections['width'][i+1], detections['height'][i+1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                cv2.putText(img, "Nr faktury:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                invoice_nr = detections['text'][i+1]
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
                print(seller_nip)
                seller_nip_flag = False
        if "regon" in detections['text'][i].lower() and seller_regon_flag:
            if int(detections['conf'][i]) > 60:
                x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
                detections['height'][i + 1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "REGON:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                seller_regon = detections['text'][i + 1]
                print(seller_regon)
                seller_regon_flag = False







        #         i += 3
        #         x, y, w, h = detections['left'][i], detections['top'][i], detections['width'][i], detections['height'][i]
        #         cv2.putText(img, "Sprzedawca:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #         seller_name = ""
        #         seller_adress = ""
        #         while detections['text'][i] != "Mechanizm":
        #             x, y, w, h = detections['left'][i], detections['top'][i], detections['width'][i], detections['height'][i]
        #             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #             seller_name = seller_name + detections['text'][i] + " "
        #             i += 1
        #         print(seller_name)
        # if "podzielonej" in detections['text'][i].lower():
        #     if int(detections['conf'][i]) > 60:
        #         i += 2
        #         x, y, w, h = detections['left'][i + 1], detections['top'][i + 1], detections['width'][i + 1], \
        #         detections['height'][i + 1]
        #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #         cv2.putText(img, "Adres:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #
        #         index = i
        #         while detections['text'][i] != "Miejsce":
        #             if index + 1 <= i:
        #                 x, y, w, h = detections['left'][i], detections['top'][i], detections['width'][i], \
        #                 detections['height'][i]
        #                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #                 seller_adress = seller_adress + detections['text'][i] + " "
        #             i += 1
        #         print(seller_adress)
        # if "wystawienia" in detections['text'][i].lower():
        #     if int(detections['conf'][i]) > 60:
        #         x, y, w, h = detections['left'][i+1], detections['top'][i+1], detections['width'][i+1], detections['height'][i+1]
        #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #         cv2.putText(img, "Miejsce:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #         invoice_place = detections['text'][i+1]
        #         print(invoice_place)
        #     i += 2
        #     x, y, w, h = detections['left'][i], detections['top'][i], detections['width'][i], detections['height'][i]
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     cv2.putText(img, "Kod pocztowy:", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #     invoice_place = detections['text'][i]
        #     print(invoice_place)




    cv2.imwrite('data/recognized_text.jpg', img)



