import tkinter as tk
import customtkinter as ctk
from tkinter import PhotoImage
import csv
import pandas as pd

import pytesseract as tess
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tess.tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
my_config = r'--oem 3 --psm 6 -l pol'

from PIL import Image, ImageTk

pd.set_option('display.max_columns', None)
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")
appearance_mode = "Ciemny"
bg_c = "#2b2b2b"
bg_c_invert = "#dbdbdb"
side_bar = None
row_number = 1
picture_path = ' '


from FromData import save_data_back
from FromData import save_products_back
from FromData import prepare_to_generate_invoice_back
from Plots import prepare_plots
from imageRecognition import mark_recognized_data

def initializeMainWindow():
    root = tk.Tk()
    root.geometry('1280x720')
    root.title('Faktury')
    root.resizable(False, False)

    root.background_image = PhotoImage(file="pictures/background.png")
    background_label = tk.Label(root, image=root.background_image)
    background_label.place(relwidth=1, relheight=1)

    return root

def initializeSideMenu(main_window):
    global bg_c
    global side_bar
    side_bar = ctk.CTkFrame(main_window, width=400, height=720, bg_color=bg_c)
    side_bar.pack(side="left", fill="none", padx=440, pady=70)
    side_bar.pack_propagate(False)

    label_faktury = ctk.CTkLabel(side_bar, text="Faktury", font=("Aharoni", 72))
    label_faktury.place(relx=0.5, rely=0.1, anchor="n")

    def from_data_menu():
        side_bar.destroy()
        fromDataSideMenu()

    def from_picture_menu():
        side_bar.destroy()
        initialize_from_picture_menu(main_window)

    def from_plot_menu():
        side_bar.destroy()
        initialize_plot_menu()

    button_fromData = ctk.CTkButton(
        side_bar,
        text='Stwórz fakturę wpisując dane',
        command=from_data_menu,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_fromData.place(relx=0.5, rely=0.3, anchor="n")

    button_fromPhoto = ctk.CTkButton(
        side_bar,
        text='Pobierz dane ze zdjęcia',
        command=from_picture_menu,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_fromPhoto.place(relx=0.5, rely=0.45, anchor="n")

    button_reports = ctk.CTkButton(
        side_bar,
        text='Pokaż raporty',
        command=from_plot_menu,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_reports.place(relx=0.5, rely=0.6, anchor="n")

    combobox = ctk.CTkOptionMenu(
        master=side_bar,
        values=["Ciemny", "Jasny"],
        command=mode_selected,
        width = 240,
        height = 50,
        font=("Aharoni", 16)
    )
    combobox.place(relx=0.5, rely=0.8, anchor="n")
    combobox.set(appearance_mode)

    label_faktury = ctk.CTkLabel(side_bar, text="Tryb wyświetlania", font=("Aharoni", 16))
    label_faktury.place(relx=0.5, rely=0.75, anchor="n")

def fromDataSideMenu():
    global bg_c
    y_position = 0.65
    side_bar = ctk.CTkFrame(main_window, width=400, height=720, bg_color=bg_c)
    side_bar.pack(side="left", fill="none", padx=10, pady=10)
    side_bar.pack_propagate(False)

    label_faktury = ctk.CTkLabel(side_bar, text="Faktury", font=("Aharoni", 72))
    label_faktury.place(relx=0.5, rely=0, anchor="n")

    def switch_menu():
        side_bar.destroy()
        right_window.destroy()
        initializeSideMenu(main_window)

    def prepare_data_dict():
        data_dict = {
            "invoice_nr": entry_invoice_nr.get() or "brak",
            "invoice_place": entry_invoice_place.get() or "brak",
            "invoice_date": entry_invoice_date.get() or "brak",
            "payment_method": entry_payment_method.get() or "brak",
            "seller_name": entry_seller_name.get() or "brak",
            "seller_adress": entry_seller_adress.get() or "brak",
            "seller_postal_code": entry_seller_postal_code.get() or "brak",
            "seller_city": entry_seller_city.get() or "brak",
            "seller_nip": entry_seller_nip.get() or "brak",
            "seller_regon": entry_seller_regon.get() or "brak",
            "seller_bank": entry_seller_bank.get() or "brak",
            "seller_account_nr": entry_seller_account_nr.get() or "brak",
            "buyer_name": entry_buyer_name.get() or "brak",
            "buyer_adress": entry_buyer_adress.get() or "brak",
            "buyer_postal_code": entry_buyer_postal_code.get() or "brak",
            "buyer_city": entry_buyer_city.get() or "brak",
            "buyer_nip": entry_buyer_nip.get() or "brak",
            "buyer_regon": entry_buyer_regon.get() or "brak",
        }
        return data_dict

    def prepare_product_dict():
        product_dict = {"Lp": [], "PKWiu CN": [], "Nazwa": [], "Cena netto": [], "Ilość": [], "JM": [], "VAT %": []}
        for row in range(1, row_number + 1):
            product_dict["Lp"].append(row)
            product_dict["PKWiu CN"].append(product_frame.grid_slaves(row=row, column=1)[0].get() or "")
            product_dict["Nazwa"].append(product_frame.grid_slaves(row=row, column=2)[0].get() or "")
            product_dict["Cena netto"].append(product_frame.grid_slaves(row=row, column=3)[0].get() or "")
            product_dict["Ilość"].append(product_frame.grid_slaves(row=row, column=4)[0].get() or "")
            product_dict["JM"].append(product_frame.grid_slaves(row=row, column=5)[0].get() or "")
            product_dict["VAT %"].append(product_frame.grid_slaves(row=row, column=6)[0].get() or "")
        return product_dict

    def save_data():
        data_dict = prepare_data_dict()
        save_data_back(data_dict)

    def load_data():
        show_data("data/saved_fill_data.csv")

    def load_data_from_pic():
        show_data("data/saved_fill_data_from_pic.csv")

    def show_data(csv_file_path):
        try:
            with open(csv_file_path, 'r', newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                row = next(csv_reader)

                entry_invoice_nr.delete(0, 'end')
                entry_invoice_place.delete(0, 'end')
                entry_invoice_date.delete(0, 'end')
                entry_payment_method.delete(0, 'end')
                entry_seller_name.delete(0, 'end')
                entry_seller_adress.delete(0, 'end')
                entry_seller_postal_code.delete(0, 'end')
                entry_seller_city.delete(0, 'end')
                entry_seller_nip.delete(0, 'end')
                entry_seller_regon.delete(0, 'end')
                entry_seller_bank.delete(0, 'end')
                entry_seller_account_nr.delete(0, 'end')
                entry_buyer_name.delete(0, 'end')
                entry_buyer_adress.delete(0, 'end')
                entry_buyer_postal_code.delete(0, 'end')
                entry_buyer_city.delete(0, 'end')
                entry_buyer_nip.delete(0, 'end')
                entry_buyer_regon.delete(0, 'end')

                entry_invoice_nr.insert(0, row["invoice_nr"])
                entry_invoice_place.insert(0, row["invoice_place"])
                entry_invoice_date.insert(0, row["invoice_date"])
                entry_payment_method.insert(0, row["payment_method"])
                entry_seller_name.insert(0, row["seller_name"])
                entry_seller_adress.insert(0, row["seller_adress"])
                entry_seller_postal_code.insert(0, row["seller_postal_code"])
                entry_seller_city.insert(0, row["seller_city"])
                entry_seller_nip.insert(0, row["seller_nip"])
                entry_seller_regon.insert(0, row["seller_regon"])
                entry_seller_bank.insert(0, row["seller_bank"])
                entry_seller_account_nr.insert(0, row["seller_account_nr"])
                entry_buyer_name.insert(0, row["buyer_name"])
                entry_buyer_adress.insert(0, row["buyer_adress"])
                entry_buyer_postal_code.insert(0, row["buyer_postal_code"])
                entry_buyer_city.insert(0, row["buyer_city"])
                entry_buyer_nip.insert(0, row["buyer_nip"])
                entry_buyer_regon.insert(0, row["buyer_regon"])

        except FileNotFoundError:
            print(f"Plik CSV nie istnieje")

    def add_product():
        global row_number

        entry = ctk.CTkEntry(master=product_frame, width=30,height=25,corner_radius=5)
        entry.grid(row=row_number+1, column=0, padx=5, pady=5)
        entry.insert(0, str(row_number+1))

        entry = ctk.CTkEntry(master=product_frame, width=90, height=25, corner_radius=5)
        entry.grid(row=row_number+1, column=1, padx=5, pady=5)

        entry = ctk.CTkEntry(master=product_frame, width=350, height=25, corner_radius=5)
        entry.grid(row=row_number+1, column=2, padx=5, pady=5)

        entry = ctk.CTkEntry(master=product_frame, width=90, height=25, corner_radius=5)
        entry.grid(row=row_number+1, column=3, padx=5, pady=5)

        entry = ctk.CTkEntry(master=product_frame, width=50, height=25, corner_radius=5)
        entry.grid(row=row_number+1, column=4, padx=5, pady=5)

        entry = ctk.CTkEntry(master=product_frame, width=40, height=25, corner_radius=5)
        entry.grid(row=row_number+1, column=5, padx=5, pady=5)

        entry = ctk.CTkEntry(master=product_frame, width=40, height=25, corner_radius=5)
        entry.grid(row=row_number+1, column=6, padx=5, pady=5)

        row_number += 1

    def save_products():
        product_dict = prepare_product_dict()
        save_products_back(product_dict)

    def delete_row():
        global row_number

        if(row_number > 1):
            for widget in product_frame.grid_slaves(row=row_number):
                widget.grid_forget()
            product_frame.grid_rowconfigure(row_number, weight=0)
            row_number-=1

    def load_products():
        global row_number

        if (row_number > 0):
            for widget in product_frame.grid_slaves(row=row_number):
                widget.grid_forget()
            product_frame.grid_rowconfigure(row_number, weight=0)
            row_number = product_frame.grid_size()[1] -1

        csv_file_path = "data/saved_products.csv"

        try:
            df = pd.read_csv(csv_file_path)

            for i, row in df.iterrows():
                entry = ctk.CTkEntry(master=product_frame, width=30, height=25, corner_radius=5)
                entry.grid(row=i + 1, column=0, padx=5, pady=5)
                entry.insert(0, row["Lp"])

                entry = ctk.CTkEntry(master=product_frame, width=90, height=25, corner_radius=5)
                entry.grid(row=i + 1, column=1, padx=5, pady=5)
                entry.insert(0, row["PKWiu CN"])

                entry = ctk.CTkEntry(master=product_frame, width=350, height=25, corner_radius=5)
                entry.grid(row=i + 1, column=2, padx=5, pady=5)
                entry.insert(0, row["Nazwa"])

                entry = ctk.CTkEntry(master=product_frame, width=90, height=25, corner_radius=5)
                entry.grid(row=i + 1, column=3, padx=5, pady=5)
                entry.insert(0, row["Cena netto"])

                entry = ctk.CTkEntry(master=product_frame, width=50, height=25, corner_radius=5)
                entry.grid(row=i + 1, column=4, padx=5, pady=5)
                entry.insert(0, row["Ilość"])

                entry = ctk.CTkEntry(master=product_frame, width=40, height=25, corner_radius=5)
                entry.grid(row=i + 1, column=5, padx=5, pady=5)
                entry.insert(0, row["JM"])

                entry = ctk.CTkEntry(master=product_frame, width=40, height=25, corner_radius=5)
                entry.grid(row=i + 1, column=6, padx=5, pady=5)
                entry.insert(0, row["VAT %"])
            row_number = df.shape[0]

        except FileNotFoundError:
            print(f"Nie znaleziono pliku")

    def prepare_to_generate_invoice():
        global row_number
        number = row_number
        data_dict = prepare_data_dict()
        product_dict = prepare_product_dict()
        prepare_to_generate_invoice_back(data_dict,product_dict,number)



    button_back = ctk.CTkButton(
        side_bar,
        text='Wróć',
        command=switch_menu,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_back.place(relx=0.5, rely=0.9, anchor="n")

    button_back = ctk.CTkButton(
        side_bar,
        text='Zapisz wpisane dane',
        command=save_data,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_back.place(relx=0.5, rely=0.4, anchor="n")

    button_back = ctk.CTkButton(
        side_bar,
        text='Wczytaj zapisane dane',
        command=load_data,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_back.place(relx=0.5, rely=0.5, anchor="n")

    button_back = ctk.CTkButton(
        side_bar,
        text='Generuj fakturę',
        command=prepare_to_generate_invoice,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_back.place(relx=0.5, rely=0.3, anchor="n")

    button_back = ctk.CTkButton(
        side_bar,
        text='Wczytaj dane z obrazka',
        command=load_data_from_pic,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_back.place(relx=0.5, rely=0.2, anchor="n")

    label = ctk.CTkLabel(side_bar, text="Podaj dane do faktury:", font=("Aharoni", 24))
    label.place(relx=0.5, rely=y_position, anchor="n")

    ##NUMER FAKTURY##

    label = ctk.CTkLabel(side_bar, text="Numer faktury:", font=("Aharoni", 16))
    label.place(relx=0.305, rely=(y_position+0.05), anchor="n")

    entry_invoice_nr = ctk.CTkEntry(
        master=side_bar,
        width=200,
        height=25,
        corner_radius=5
    )
    entry_invoice_nr.place(relx=0.7, rely=(y_position+0.055), anchor="n")

    ##MIEJSCE WYSTAWIENIA FAKTURY##

    label = ctk.CTkLabel(side_bar, text="Miejsce wystawienia:", font=("Aharoni", 16))
    label.place(relx=0.25, rely=(y_position+0.09), anchor="n")

    entry_invoice_place = ctk.CTkEntry(
        master=side_bar,
        width=200,
        height=25,
        corner_radius=5
    )
    entry_invoice_place.place(relx=0.7, rely=(y_position+0.095), anchor="n")

    ##DATA WYSTAWIENIA##

    label = ctk.CTkLabel(side_bar, text="Data wystawienia:", font=("Aharoni", 16))
    label.place(relx=0.275, rely=(y_position+0.13), anchor="n")

    entry_invoice_date = ctk.CTkEntry(
        master=side_bar,
        width=200,
        height=25,
        corner_radius=5
    )
    entry_invoice_date.place(relx=0.7, rely=(y_position+0.135), anchor="n")
    entry_invoice_date.insert(1, "yyyy-mm-dd")

    ##FORMA PŁATNOŚCI##

    label = ctk.CTkLabel(side_bar, text="Forma płatności:", font=("Aharoni", 16))
    label.place(relx=0.29, rely=(y_position+0.17), anchor="n")

    entry_payment_method = ctk.CTkEntry(
        master=side_bar,
        width=200,
        height=25,
        corner_radius=5
    )
    entry_payment_method.place(relx=0.7, rely=(y_position+0.175), anchor="n")

    ###DRUGIE MENU#################################
    y2_position = 0.01

    right_window = ctk.CTkFrame(main_window, width=860, height=720, bg_color=bg_c)
    right_window.pack(side="right", fill="none", padx=10, pady=10)
    right_window.pack_propagate(False)

    ######SPRZEDAWCA#######

    label = ctk.CTkLabel(right_window, text="Dane Sprzedawcy:", font=("Aharoni", 30))
    label.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###NAZWA SPRZEDAWCY###

    y2_position += 0.06
    label = ctk.CTkLabel(right_window, text="Nazwa:", font=("Aharoni", 16))
    label.place(relx=0.285-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_seller_name = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_seller_name.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###ADRES SPRZEDAWCY###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="Adres:", font=("Aharoni", 16))
    label.place(relx=0.288-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_seller_adress = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_seller_adress.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###KOD POCZTOWY I MIASTO###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="Kod pocztowy:", font=("Aharoni", 16))
    label.place(relx=0.251-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_seller_postal_code = ctk.CTkEntry(
        master=right_window,
        width=100,
        height=25,
        corner_radius=5
    )
    entry_seller_postal_code.place(relx=0.3815-0.15, rely=y2_position, anchor="n")

    label = ctk.CTkLabel(right_window, text="Miasto:", font=("Aharoni", 16))
    label.place(relx=0.485-0.15, rely=y2_position, anchor="n")

    entry_seller_city = ctk.CTkEntry(
        master=right_window,
        width=130,
        height=25,
        corner_radius=5
    )
    entry_seller_city.place(relx=0.6-0.15, rely=y2_position, anchor="n")

    ###NIP SPRZEDAWCY###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="NIP:", font=("Aharoni", 16))
    label.place(relx=0.298-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_seller_nip = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_seller_nip.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###REGON SPRZEDAWCY###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="REGON:", font=("Aharoni", 16))
    label.place(relx=0.281-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_seller_regon = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_seller_regon.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###BANK SPRZEDAWCY###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="Bank:", font=("Aharoni", 16))
    label.place(relx=0.291-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_seller_bank = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_seller_bank.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###NR KONTA SPRZEDAWCY###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="Nr konta:", font=("Aharoni", 16))
    label.place(relx=0.275-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_seller_account_nr = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_seller_account_nr.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ######KUPUJĄCY#######

    y2_position += 0.05
    label = ctk.CTkLabel(right_window, text="Dane Kupującego:", font=("Aharoni", 30))
    label.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###NAZWA SPRZEDAWCY###

    y2_position += 0.06
    label = ctk.CTkLabel(right_window, text="Nazwa:", font=("Aharoni", 16))
    label.place(relx=0.285-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_buyer_name = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_buyer_name.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###ADRES SPRZEDAWCY###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="Adres:", font=("Aharoni", 16))
    label.place(relx=0.288-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_buyer_adress = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_buyer_adress.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###KOD POCZTOWY I MIASTO###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="Kod pocztowy:", font=("Aharoni", 16))
    label.place(relx=0.251-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_buyer_postal_code = ctk.CTkEntry(
        master=right_window,
        width=100,
        height=25,
        corner_radius=5
    )
    entry_buyer_postal_code.place(relx=0.3815-0.15, rely=y2_position, anchor="n")

    label = ctk.CTkLabel(right_window, text="Miasto:", font=("Aharoni", 16))
    label.place(relx=0.485-0.15, rely=y2_position, anchor="n")

    entry_buyer_city = ctk.CTkEntry(
        master=right_window,
        width=130,
        height=25,
        corner_radius=5
    )
    entry_buyer_city.place(relx=0.6-0.15, rely=y2_position, anchor="n")

    ###NIP SPRZEDAWCY###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="NIP:", font=("Aharoni", 16))
    label.place(relx=0.298-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_buyer_nip = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_buyer_nip.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ###REGON SPRZEDAWCY###

    y2_position += 0.035
    label = ctk.CTkLabel(right_window, text="REGON:", font=("Aharoni", 16))
    label.place(relx=0.281-0.15, rely=y2_position, anchor="n")

    y2_position += 0.005
    entry_buyer_regon = ctk.CTkEntry(
        master=right_window,
        width=300,
        height=25,
        corner_radius=5
    )
    entry_buyer_regon.place(relx=0.5-0.15, rely=y2_position, anchor="n")

    ### PRODUKTY ###
    y2_position += 0.05
    product_frame = ctk.CTkScrollableFrame(right_window, width=800, height=230, bg_color=bg_c)
    product_frame.place(relx=0.5, rely=y2_position, anchor="n")


    label = ctk.CTkLabel(product_frame, text="Lp", font=("Aharoni", 16))
    label.grid(row=0, column=0)

    label = ctk.CTkLabel(product_frame, text="PKWiu CN", font=("Aharoni", 16))
    label.grid(row=0, column=1)

    label = ctk.CTkLabel(product_frame, text="Nazwa towaru lub usługi", font=("Aharoni", 16))
    label.grid(row=0, column=2)

    label = ctk.CTkLabel(product_frame, text="Cena netto", font=("Aharoni", 16))
    label.grid(row=0, column=3)

    label = ctk.CTkLabel(product_frame, text="Ilość", font=("Aharoni", 16))
    label.grid(row=0, column=4)

    label = ctk.CTkLabel(product_frame, text="JM", font=("Aharoni", 16))
    label.grid(row=0, column=5)

    label = ctk.CTkLabel(product_frame, text="VAT %", font=("Aharoni", 16))
    label.grid(row=0, column=6)

    entry = ctk.CTkEntry(master=product_frame, width=30, height=25, corner_radius=5)
    entry.grid(row=row_number, column=0, padx=5, pady=5)
    entry.insert(0, "1")

    entry = ctk.CTkEntry(master=product_frame, width=90, height=25, corner_radius=5)
    entry.grid(row=row_number, column=1, padx=5, pady=5)

    entry = ctk.CTkEntry(master=product_frame, width=350, height=25, corner_radius=5)
    entry.grid(row=row_number, column=2, padx=5, pady=5)

    entry = ctk.CTkEntry(master=product_frame, width=90, height=25, corner_radius=5)
    entry.grid(row=row_number, column=3, padx=5, pady=5)

    entry = ctk.CTkEntry(master=product_frame, width=50, height=25, corner_radius=5)
    entry.grid(row=row_number, column=4, padx=5, pady=5)

    entry = ctk.CTkEntry(master=product_frame, width=40, height=25, corner_radius=5)
    entry.grid(row=row_number, column=5, padx=5, pady=5)

    entry = ctk.CTkEntry(master=product_frame, width=40, height=25, corner_radius=5)
    entry.grid(row=row_number, column=6, padx=5, pady=5)

    product_insert_frame = ctk.CTkFrame(right_window, width=350, height=400, bg_color=bg_c)
    product_insert_frame.place(relx=0.765, rely=0.03, anchor="n")

    label = ctk.CTkLabel(product_insert_frame, text="Produkty/Usługi:", font=("Aharoni", 30))
    label.place(relx=0.5, rely=0.1, anchor="n")

    button_add_product = ctk.CTkButton(
        product_insert_frame,
        text='Dodaj produkt',
        command=add_product,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_add_product.place(relx=0.5, rely=0.8, anchor="n")

    button_delete_row = ctk.CTkButton(
        product_insert_frame,
        text='Usuń wiersz',
        command=delete_row,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_delete_row.place(relx=0.5, rely=0.65, anchor="n")

    button_save_products = ctk.CTkButton(
        product_insert_frame,
        text='Zapisz produkty',
        command=save_products,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_save_products.place(relx=0.5, rely=0.35, anchor="n")

    button_load_products = ctk.CTkButton(
        product_insert_frame,
        text='Wczytaj produkty',
        command=load_products,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_load_products.place(relx=0.5, rely=0.5, anchor="n")

    #########################################################################################################################

def initialize_from_picture_menu(main_window):
    global picture_path
    picture_menu = ctk.CTkFrame(main_window, width=400, height=720, bg_color=bg_c)
    picture_menu.pack(side="left", fill="none", padx=10, pady=10)

    picture_preview = ctk.CTkFrame(main_window, width=860, height=720, bg_color=bg_c)
    picture_preview.pack(side="right", fill="none", padx=10, pady=10)
    picture_preview.pack_propagate(False)

    label_picture = ctk.CTkLabel(master=picture_preview, text="Pobierz obrazek",  font=("Aharoni", 48))
    label_picture.place(relx=0.5, rely=0.45, anchor="n")


    label_faktury = ctk.CTkLabel(picture_menu, text="Faktury", font=("Aharoni", 72))
    label_faktury.place(relx=0.5, rely=0, anchor="n")


    def switch_menu():
        picture_menu.destroy()
        picture_preview.destroy()
        initializeSideMenu(main_window)

    def get_path():
        global picture_path
        picture_path = entry_picture_path.get()
        show_picture(picture_path)

    def show_picture(path):
        img = ctk.CTkImage(light_image=Image.open(path), size=(750, 650))
        label_picture = ctk.CTkLabel(master=picture_preview, image=img)
        label_picture.place(relx=0.5, rely=0.035, anchor="n")

    def rotate_picture():
        global picture_path
        img = Image.open(picture_path)
        img = img.rotate(90)
        img.save("data/image_processed.jpg")
        picture_path = "data/image_processed.jpg"
        show_picture(picture_path)

    def grey_scale():
        global picture_path
        img = Image.open(picture_path)
        img = img.convert('L')
        img.save("data/image_processed.jpg")
        picture_path = "data/image_processed.jpg"
        show_picture(picture_path)

    def remove_background():
        global picture_path
        img = Image.open(picture_path)
        img = img.convert('L')
        img = img.point(lambda x: 0 if x < 150 else 255, '1')
        img.save("data/image_processed.jpg")
        picture_path = "data/image_processed.jpg"
        show_picture(picture_path)

    def image_recognition():
        global picture_path
        mark_recognized_data(picture_path)
        show_picture("data/recognized_text.jpg")

    button_back = ctk.CTkButton(
        picture_menu,
        text='Wróć',
        command=switch_menu,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_back.place(relx=0.5, rely=0.85, anchor="n")

    button_back = ctk.CTkButton(
        picture_menu,
        text='Pobierz dane',
        command=image_recognition,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_back.place(relx=0.5, rely=0.75, anchor="n")

    button_generate = ctk.CTkButton(
        picture_menu,
        text='Zatwierdź',
        command=get_path,
        width=50,
        height=25,
        font=("Aharoni", 16)
    )
    button_generate.place(relx=0.82, rely=0.2, anchor="n")

    label = ctk.CTkLabel(picture_menu, text="Podaj ścieżkę do obrazka", font=("Aharoni", 16))
    label.place(relx=0.5, rely=0.15, anchor="n")

    label = ctk.CTkLabel(picture_menu, text="Przygotuj obrazek", font=("Aharoni", 16))
    label.place(relx=0.5, rely=0.25, anchor="n")

    button_rotate = ctk.CTkButton(
        picture_menu,
        text='Obróć',
        command=rotate_picture,
        width=100,
        height=50,
        font=("Aharoni", 16)
    )
    button_rotate.place(relx=0.5, rely=0.3, anchor="n")

    button_grey_scale = ctk.CTkButton(
        picture_menu,
        text='Skala szarości',
        command=grey_scale,
        width=100,
        height=50,
        font=("Aharoni", 16)
    )
    button_grey_scale.place(relx=0.2, rely=0.3, anchor="n")

    button_background_remove = ctk.CTkButton(
        picture_menu,
        text='Usuń tło',
        command=remove_background,
        width=100,
        height=50,
        font=("Aharoni", 16)
    )
    button_background_remove.place(relx=0.78, rely=0.3, anchor="n")

    entry_picture_path = ctk.CTkEntry(
        master=picture_menu,
        width=250,
        height=25,
        corner_radius=5
    )
    entry_picture_path.place(relx=0.4, rely=0.2, anchor="n")
    entry_picture_path.insert(1, 'data/image.jpg')
    picture_path = entry_picture_path.get()
def mode_selected(mode):
    global  appearance_mode
    global bg_c
    global bg_c_invert
    global side_bar
    if mode == "Ciemny":
        ctk.set_appearance_mode("dark")
        appearance_mode = "Ciemny"
        bg_c = "#2b2b2b"
        bg_c_invert = "#dbdbdb"
    elif mode == "Jasny":
        ctk.set_appearance_mode("light")
        appearance_mode = "Jasny"
        bg_c = "#dbdbdb"
        bg_c_invert = "#2b2b2b"

    side_bar.destroy()
    initializeSideMenu(main_window)



def initialize_plot_menu():
    plot_menu = ctk.CTkFrame(main_window, width=1000, height=500, bg_color=bg_c)
    plot_menu.place(relx=0.5, rely=0.153, anchor='n')
    plot_menu.pack_propagate(False)

    df_plot_1, df_plot_2 = prepare_plots()
    def switch_menu():
        plot_menu.destroy()
        initializeSideMenu(main_window)

    button_back = ctk.CTkButton(
        plot_menu,
        text='Wróć',
        command=switch_menu,
        width=240,
        height=50,
        font=("Aharoni", 16)
    )
    button_back.place(relx=0.5, rely=0.875, anchor="n")

    plot_frame_1 = ctk.CTkFrame(plot_menu, width=480, height=410, bg_color=bg_c)
    plot_frame_1.place(relx=0.255, rely=0.03, anchor='n')
    plot_frame_1.pack_propagate(False)

    plot_frame_2 = ctk.CTkFrame(plot_menu, width=480, height=410, bg_color=bg_c)
    plot_frame_2.place(relx=0.745, rely=0.03, anchor='n')
    plot_frame_2.pack_propagate(False)



    # WYKRES 1
    figure = Figure(figsize=(5, 4), dpi=100)
    figure.set_facecolor(bg_c)
    subplot = figure.add_subplot(1, 1, 1)
    subplot.bar(df_plot_1['Nazwa'], df_plot_1['Cena'], color='#1f6aa5')
    subplot.set_xticks(range(len(df_plot_1['Nazwa'])))
    subplot.set_xticklabels(df_plot_1['Nazwa'], rotation=45)
    subplot.set_facecolor(bg_c)
    subplot.tick_params(axis='both', color=bg_c_invert, labelcolor=bg_c_invert)
    subplot.spines['top'].set_color(bg_c_invert)
    subplot.spines['bottom'].set_color(bg_c_invert)
    subplot.spines['left'].set_color(bg_c_invert)
    subplot.spines['right'].set_color(bg_c_invert)
    subplot.title.set_color(bg_c_invert)
    subplot.xaxis.label.set_color(bg_c_invert)
    subplot.yaxis.label.set_color(bg_c_invert)
    figure.subplots_adjust(bottom=0.3)
    subplot.set_title('Największa sprzedaż netto')

    canvas = FigureCanvasTkAgg(figure, master=plot_frame_1)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side="left", fill="none", padx=20, pady=20)


    # WYKRES 2
    figure2 = Figure(figsize=(5, 4), dpi=100)
    figure2.set_facecolor(bg_c)
    subplot2 = figure2.add_subplot(1, 1, 1)
    subplot2.bar(df_plot_2['Klient'], df_plot_2['Ilość'], color='#1f6aa5')
    subplot2.set_xticks(range(len(df_plot_2['Klient'])))
    subplot2.set_xticklabels(df_plot_2['Klient'], rotation=45)
    subplot2.set_facecolor(bg_c)
    subplot2.tick_params(axis='both', color=bg_c_invert, labelcolor=bg_c_invert)
    subplot2.spines['top'].set_color(bg_c_invert)
    subplot2.spines['bottom'].set_color(bg_c_invert)
    subplot2.spines['left'].set_color(bg_c_invert)
    subplot2.spines['right'].set_color(bg_c_invert)
    subplot2.title.set_color(bg_c_invert)
    subplot2.xaxis.label.set_color(bg_c_invert)
    subplot2.yaxis.label.set_color(bg_c_invert)
    figure2.subplots_adjust(bottom=0.3)
    figure2.subplots_adjust(left=0.2)
    subplot2.set_title('Klienci')
    subplot2.set_ylabel('Ilość faktur', color=bg_c_invert)

    canvas = FigureCanvasTkAgg(figure2, master=plot_frame_2)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side="left", fill="none", padx=20, pady=20)



if __name__ == '__main__':
    main_window = initializeMainWindow()
    initializeSideMenu(main_window)
    main_window.mainloop()
