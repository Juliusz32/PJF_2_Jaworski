import customtkinter as ctk
import tkinter as tk
from tkinter import PhotoImage
class Main:
    def __init__(self):
        self.main_window = self.initializeMainWindow()
        ctk.set_appearance_mode("dark")
        self.appearance_mode = "Ciemny"
        self.bg_c = "#2b2b2b"
        self.bg_c_invert = "#dbdbdb"
        self.main_menu = self.initializeMainMenu(self.main_window, self.bg_c, self.appearance_mode)

    def initializeMainWindow(self):
        root = tk.Tk()
        root.geometry('1280x720')
        root.title('Faktury')
        root.resizable(False, False)

        root.background_image = PhotoImage(file="pictures/background.png")
        background_label = tk.Label(root, image=root.background_image)
        background_label.place(relwidth=1, relheight=1)

        return root

    def mode_selected(self, mode):
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

        self.main_menu.destroy()
        self.main_menu = self.initializeMainMenu(self.main_window, bg_c, appearance_mode)


    def initializeMainMenu(self, main_window, bg_c, appearance_mode):
        main_menu = ctk.CTkFrame(main_window, width=400, height=720, bg_color=bg_c)
        main_menu.pack(side="left", fill="none", padx=440, pady=70)
        main_menu.pack_propagate(False)

        label_faktury = ctk.CTkLabel(main_menu, text="Faktury", font=("Aharoni", 72))
        label_faktury.place(relx=0.5, rely=0.1, anchor="n")

        def from_data_menu():
            # main_menu.destroy()
            # fromDataSideMenu(main_window)
            return 0
        def from_picture_menu():
            # main_menu.destroy()
            # initialize_from_picture_menu(main_window)
            return 0
        def from_plot_menu():
            # main_menu.destroy()
            # initialize_plot_menu()
            return 0

        button_fromData = ctk.CTkButton(
            main_menu,
            text='Stwórz fakturę wpisując dane',
            command=from_data_menu,
            width=240,
            height=50,
            font=("Aharoni", 16)
        )
        button_fromData.place(relx=0.5, rely=0.3, anchor="n")

        button_fromPhoto = ctk.CTkButton(
            main_menu,
            text='Pobierz dane ze zdjęcia',
            command=from_picture_menu,
            width=240,
            height=50,
            font=("Aharoni", 16)
        )
        button_fromPhoto.place(relx=0.5, rely=0.45, anchor="n")

        button_reports = ctk.CTkButton(
            main_menu,
            text='Pokaż raporty',
            command=from_plot_menu,
            width=240,
            height=50,
            font=("Aharoni", 16)
        )
        button_reports.place(relx=0.5, rely=0.6, anchor="n")

        combobox = ctk.CTkOptionMenu(
            master=main_menu,
            values=["Ciemny", "Jasny"],
            command=self.mode_selected,
            width = 240,
            height = 50,
            font=("Aharoni", 16)
        )
        combobox.place(relx=0.5, rely=0.8, anchor="n")
        combobox.set(appearance_mode)

        label_faktury = ctk.CTkLabel(main_menu, text="Tryb wyświetlania", font=("Aharoni", 16))
        label_faktury.place(relx=0.5, rely=0.75, anchor="n")

        return main_menu



if __name__ == '__main__':
    main = Main()
    main.main_window.mainloop()




# def mode_selected_main(appearance_mode, bg_c, bg_c_invert, side_bar):
#     main_bg_c = bg_c
#     main_bg_c_invert = bg_c_invert
#     main_appearance_mode = appearance_mode
#     print("Main:")
#     print(appearance_mode)
#
#     if appearance_mode == "Ciemny":
#         ctk.set_appearance_mode("dark")
#     elif appearance_mode == "Jasny":
#         ctk.set_appearance_mode("light")
#
#     side_bar.destroy()
#     side_bar = sideMenu.initializeSideMenu(main_window, bg_c, appearance_mode)
#     return side_bar



