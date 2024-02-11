import csv
import os
import glob
import pandas as pd
from docxtpl import DocxTemplate
from docx2pdf import convert

from NumberToWords import kwota_slownie


def save_data_back(data_dict, path):
    data_directory = "data"
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    csv_file_path = os.path.join(data_directory, path)

    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())
        csv_writer.writeheader()
        csv_writer.writerow(data_dict)

def save_products_back(product_dict, path):
    if os.path.exists(path):
        os.remove(path)

    with open(path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = product_dict.keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row_index in range(len(product_dict["Lp"])):
            row_data = {key: product_dict[key][row_index] for key in fieldnames}
            writer.writerow(row_data)

def prepare_to_generate_invoice_back(data_dict, product_dict, row_number):

    invoices_folder = 'data/invoices'
    os.makedirs(invoices_folder, exist_ok=True)

    existing_files = glob.glob(os.path.join(invoices_folder, 'invoice_from_data_*.csv'))
    last_file_number = max([int(file.split('_')[-1].split('.')[0]) for file in existing_files],
                           default=0) if existing_files else 0
    new_file_number = last_file_number + 1
    csv_file_name = os.path.join(invoices_folder, f'invoice_from_data_{new_file_number}.csv')

    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_dict.keys())
        csv_writer.writeheader()
        csv_writer.writerow(data_dict)

    print(f"Plik CSV (invoice) zapisany jako: {csv_file_name}")

    product_csv_file_name = os.path.join(invoices_folder, f'invoice_products_from_data_{new_file_number}.csv')

    with open(product_csv_file_name, 'w', newline='', encoding='utf-8') as product_csv_file:
        product_csv_writer = csv.DictWriter(product_csv_file, fieldnames=product_dict.keys())
        product_csv_writer.writeheader()
        for i in range(row_number):
            product_csv_writer.writerow({key: product_dict[key][i] for key in product_dict})

    print(f"Plik CSV (invoice products) zapisany jako: {product_csv_file_name}")
    generate_invoice()

def generate_invoice():

    csv_files_products = [file for file in os.listdir('data/invoices/') if file.startswith('invoice_products_from_data_') and file.endswith('.csv')]

    max_file_products = max(csv_files_products, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    full_path_products = os.path.join('data/invoices/', max_file_products)

    df = pd.read_csv(full_path_products, encoding='utf-8')

    def convert_to_number(value):
        try:
            return float(value)
        except ValueError:
            return 0.0

    df['Cena netto'] = df['Cena netto'].apply(convert_to_number)

    df['VAT %'] = df['VAT %'].apply(convert_to_number)

    df['Wartość netto'] = df['Cena netto'] * df['Ilość']
    df['Wartość VAT'] = round(df['Wartość netto'] * df['VAT %'] * 0.01, 2)
    df['Wartość Brutto'] = round(df['Wartość netto'] + df['Wartość VAT'], 2)

    df = df[['Lp', 'PKWiu CN', 'Nazwa', 'Cena netto', 'Ilość', 'JM', 'Wartość netto', 'VAT %', 'Wartość VAT',
             'Wartość Brutto']]

    df = df.fillna(' ')
    invoice_list = df.values.tolist()

    csv_files_invoice_data = [file for file in os.listdir('data/invoices/') if file.startswith('invoice_from_data_') and file.endswith('.csv')]

    max_file_invoice_data = max(csv_files_invoice_data, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    full_path_invoice_data = os.path.join('data/invoices/', max_file_invoice_data)

    df1 = pd.read_csv(full_path_invoice_data, encoding='Windows-1250')




    doc = DocxTemplate("data/invoice.docx")

    doc.render({
        "doc_invoice_nr": df1.at[0, 'invoice_nr'],
        "doc_invoice_place": df1.at[0, 'invoice_place'],
        "doc_invoice_date": df1.at[0, 'invoice_date'],
        "doc_payment_method": df1.at[0, 'payment_method'],

        "doc_seller_name": df1.at[0, 'seller_name'],
        "doc_seller_adress": df1.at[0, 'seller_adress'],
        "doc_seller_postal_code": df1.at[0, 'seller_postal_code'],
        "doc_seller_city": df1.at[0, 'seller_city'],
        "doc_seller_nip": df1.at[0, 'seller_nip'],
        "doc_seller_regon": df1.at[0, 'seller_regon'],
        "doc_seller_bank": df1.at[0, 'seller_bank'],
        "doc_seller_account_nr": df1.at[0, 'seller_account_nr'],

        "doc_buyer_name": df1.at[0, 'buyer_name'],
        "doc_buyer_adress": df1.at[0, 'buyer_adress'],
        "doc_buyer_postal_code": df1.at[0, 'buyer_postal_code'],
        "doc_buyer_city": df1.at[0, 'buyer_city'],
        "doc_buyer_nip": df1.at[0, 'buyer_nip'],
        "doc_buyer_regon": df1.at[0, 'buyer_regon'],
        "invoice_list": invoice_list,

        "doc_netto_sum": df['Wartość netto'].sum(),
        "doc_vat": df.at[0, 'VAT %'],
        "doc_vat_sum": round(df['Wartość VAT'].sum(),2),  #zmieniono
        "doc_brutto_sum": df['Wartość Brutto'].sum(),
        "doc_brutto_words": kwota_slownie(round(df['Wartość Brutto'].sum(),2))
    })

    docx_path = os.path.join('output', f'invoice_{str(df1.at[0, 'invoice_nr'])}.docx')
    invoice_path = os.path.join('output', f'invoice_{str(df1.at[0, 'invoice_nr'])}.pdf')

    doc.save(docx_path)
    convert(docx_path, invoice_path)
    return