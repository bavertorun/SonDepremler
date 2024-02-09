#    Son Depremler V1  #
# Coder by Baver Torun #


import tkinter.messagebox as msgbox
import customtkinter
import tkintermapview
import webbrowser
import requests

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title('Son Depremler')
        self.iconbitmap('./Assets/icon.ico')
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Son Depremler", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        

        self.instagarm_btn = customtkinter.CTkButton(self.sidebar_frame,text="İnstagram", command=self.open_instagram)
        self.instagarm_btn.grid(row=1, column=0, padx=20, pady=10)
        

        self.sourcecode_button = customtkinter.CTkButton(self.sidebar_frame,text="Kaynak Kodu", command=self.open_sourcecode)
        self.sourcecode_button.grid(row=2, column=0,)
        
        self.info_button = customtkinter.CTkButton(self.sidebar_frame,text="Uygulama Kullanımı", command=self.open_infoapp)
        self.info_button.grid(row=3, column=0, padx=20, pady=10)

        # self.refresh_button = customtkinter.CTkButton(self.sidebar_frame,text="Yenile", command=self.refresh)
        # self.refresh_button.grid(row=4, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Görünüm Modu:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark","Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Arayüzü Ölçeklendirme:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))




        # create earthquake list frame
        self.earthquake_list_frame = customtkinter.CTkScrollableFrame(self, width=1000, height=1000)
        self.earthquake_list_frame.grid(row=1,column=1,padx=(20,20),pady=(20,20))

        url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"
        rq = requests.get(url)
        data = rq.json()

        total = data['metadata']['total']


        for i in range(total):
            title = data['result'][i]['title']
            date  = data['result'][i]['date']
            lon   = data['result'][i]['geojson']['coordinates'][0]
            lat   = data['result'][i]['geojson']['coordinates'][1]
            mag   = float(data['result'][i]['mag']) # Deprem Büyüklüğü
            depth = float(data['result'][i]['depth']) #Deprem Derinliği

            info_text = f'{date} - {title} => {mag}'            

            self.label = customtkinter.CTkLabel(self.earthquake_list_frame,text=info_text)
            self.label.grid(row=i,column=0,padx=100)
    
            self.btn = customtkinter.CTkButton(self.earthquake_list_frame,text="Haritada Gör",command=lambda t=title, la=lat,lo=lon: self.open_map(t,la,lo))
            self.btn.grid(row=i,column=1,padx=(10,10), pady=(5,5))


       


    def open_map(self,title,lat,lon):
        new_window = customtkinter.CTkToplevel(self)
        new_window.title(f"{title} - Harita Konumu")
        new_window.iconbitmap('./Assets/icon.ico')
        new_window.geometry('540x400')
        new_window.resizable(width=False,height=False)


        map_widget = tkintermapview.TkinterMapView(new_window, width=800, height=600, corner_radius=0)
        map_widget.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        map_widget.set_marker(lat,lon, text=title)
        map_widget.set_position(lat,lon)
        map_widget.set_zoom(15)
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_instagram(self):
        webbrowser.open("https://www.instagram.com/bavertorun_/")

    def refresh(self):
        pass

    def open_sourcecode(self):
        webbrowser.open("https://github.com/bavertorun/SonDepremler")

    def open_infoapp(self):

        info_text = "Deprem Bilgileri: `Tarih - Yer --> Büyüklüğü` \nŞeklinde gösterilmektedir."

        msgbox.showinfo("Uygulama Kullanımı",info_text)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()

## Coder by Baver Torun ##