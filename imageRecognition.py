from PIL import Image
import re
import pytesseract as tess
import os
import csv

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