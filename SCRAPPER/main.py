# This is a sample Python script.
import json

from Helper import Helper
from Model.StockForm import StockForm
from SiteScrapper import SiteScrapper
import tkinter
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class MainApplication():
    stock_form = StockForm()
    data_json = ""

    name_selected = ""
    helper = Helper()
    input_x = 200
    label_x = 50



    #search_text_box = tkinter.Entry()
    #ticker_txtbox = tkinter.Entry()
    #stock_names_listbox = Listbox()


    def load_data(self):

        my_name = self.my_name_str.get()

        if my_name == "":
            self.__selected_item()
            self.stock_form.Ticker = self.name_selected
        else:
            self.stock_form.Ticker = my_name

        tck = self.stock_form.Ticker
        pos_df = self.helper.subpositions_df

        pos = pos_df[pos_df["name"] == self.stock_form.Sub_Position]["website_name"].iloc[0]

        part = "raporty-finansowe-bilans"

        ss = SiteScrapper()
        data = ss.get_from_website(tck, pos, part)

        cleaned_data = []

        data_table_view = ttk.Treeview(self.parent, columns=('Ticker', 'Period', 'Value'), show='headings', height=5)

        data_table_view.column("# 1", anchor=CENTER,width=100)
        data_table_view.heading("# 1", text="Ticker")
        data_table_view.column("# 2", anchor=CENTER,width=90)
        data_table_view.heading("# 2", text="Period")
        data_table_view.column("# 3", anchor=CENTER,width=90)
        data_table_view.heading("# 3", text="Value")

        json_str = ""

        for d in data:
            cleaned_data.append((d[0], d[1], d[2]))
            json_obj = "{\"Ticker\":\"" + d[0] + "\",\"Period\":\"" + d[1] + "\",\"Value\":\"" + str(d[2]) + "\"},"
            json_str += json_obj

        json_str = "[" + json_str[:-1] + "]"

        self.data_json = str(json_str)

        for cd in cleaned_data:
            data_table_view.insert("", index=0, values=cd)

        data_table_view.place(x=self.label_x, y=280)
        style = ttk.Style(self.parent)

        style.theme_use("clam")  # set theam to clam
        style.configure("Treeview", background="black", fieldbackground="black", foreground="white")
        style.configure("Buttons", font=('calibri', 10, 'bold'), foreground='red',background="blue")
    def file_save(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text2save = self.data_json  # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close()
    def get_subpositions(self,event):
        main_position = event.widget.get()
        self.helper.load_subpostions(str(main_position))
        subpositions_lst = list(np.array(self.helper.subpositions_df["name"]))
        subposition_combo = ttk.Combobox(self.parent, values=subpositions_lst)
        subposition_combo.place(x=self.input_x, y=60)
        subposition_combo.bind("<<ComboboxSelected>>", self.get_subposition)

        self.stock_form.Main_Position = main_position
    def get_subposition(self,event):
        sub_position = event.widget.get()

        self.stock_form.Sub_Position = sub_position
    def fill_listbox(self,main_data):
        for item in main_data:
            self.stock_names_listbox.insert(-1,item)
    def name_search(self,event):
        sstr = self.search_text_box.get()
        self.stock_names_listbox.delete(0, END)
        # If filter removed show all data
        if sstr == "":
            self.fill_listbox(self.helper.names_df["NAME"])
            return

        filtered_data = list()
        for item in self.helper.names_df["NAME"]:
            if item.find(sstr) >= 0:
                filtered_data.append(item)

        self.fill_listbox(filtered_data)

    def __selected_item(self):
        for i in self.stock_names_listbox.curselection():
            self.name_selected=self.stock_names_listbox.get(i)

    def __init__(self, *args, **kwargs):
        self.helper.load_tickers()

        self.parent = tkinter.Tk()

        self.search_str = StringVar()
        self.my_name_str = StringVar()

        self.parent.title("SCRAPPER")
        self.parent.geometry("640x640")
        self.parent.minsize(640, 640)
        self.parent.maxsize(640, 640)

        main_position_lbl = Label(self.parent, text="Main Position").place(x=self.label_x, y=20)
        subposition_lbl = Label(self.parent, text="Sub Position").place(x=self.label_x, y=60)
        ticker_lbl = Label(self.parent, text="Ticker").place(x=self.label_x, y=100)

        choose_stock_lbl = Label(self.parent, text="Choose Stock").place(x=400, y=20)

        choose_ticker_lbl = Label(self.parent, text="1. Choose main position from drop-down.").place(x=200, y=460)
        choose_ticker_lbl = Label(self.parent, text="2. Choose sub-position from drop-down.").place(x=200, y=480)
        choose_ticker_lbl = Label(self.parent, text="3. Choose stock from listview.").place(x=200, y=500)
        choose_ticker_lbl = Label(self.parent, text="4. Click scrap.").place(x=200, y=520)
        choose_ticker_lbl = Label(self.parent, text="*** Some stock from listview may be obsolete ***").place(x=200,y=560)
        choose_ticker_lbl = Label(self.parent,text="*** If ticker or name is not working the try ticker txtbox field and write yourself ***").place(x=200, y=580)

        main_position_combo = ttk.Combobox(self.parent, values=["balance_sheet"], textvariable=tkinter.StringVar())
        main_position_combo.place(x=self.input_x, y=20)
        main_position_combo.bind("<<ComboboxSelected>>", self.get_subpositions)

        subposition_combo = ttk.Combobox(self.parent, values=[])
        subposition_combo.place(x=self.input_x, y=60)
        subposition_combo.bind("<<ComboboxSelected>>", self.get_subposition)

        my_name_text_box = tkinter.Entry(self.parent, textvariable=self.my_name_str, width=10)
        my_name_text_box.place(x=self.input_x, y=100)

        scrap_button = tkinter.Button(self.parent, text="SCRAP", command=self.load_data)
        scrap_button.place(x=self.input_x, y=200)
        scrap_button = tkinter.Button(self.parent, text="DOWNLOAD", command=self.file_save)
        scrap_button.place(x=self.input_x + 100, y=200)

        self.stock_names_listbox = Listbox(self.parent)
        self.stock_names_listbox.place(x=400, y=60)

        self.fill_listbox(self.helper.names_df["NAME"])

        self.search_text_box = tkinter.Entry(self.parent, textvariable=self.search_str, width=20)
        self.search_text_box.place(x=400, y=40)
        self.search_text_box.bind("<Return>", self.name_search)

        #tv = ttk.Treeview(self.parent)

        self.parent.mainloop()


if __name__ == "__main__":
    ma = MainApplication()

    #root = tkinter.Tk()
    #MainApplication(root).pack(side="top", fill="both", expand=True)

    #root.mainloop()