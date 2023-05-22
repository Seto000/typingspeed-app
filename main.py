import customtkinter
import threading
import time
import requests


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.endpoint = "https://api.quotable.io"
        self.response = requests.get(f"{self.endpoint}/quotes/random", params={"maxLength": 50})
        self.response.raise_for_status()

        self.title("Typing Speed Test")
        self.geometry("1280x924")
        self.minsize(width=924, height=724)

        self.frame = customtkinter.CTkFrame(master=self, border_width=2, corner_radius=8)

        self.sample_label = customtkinter.CTkLabel(master=self.frame, text=self.response.json()[0]["content"],
                                                   font=("Helvetica", 24), fg_color="#343638", width=600, height=150,
                                                   corner_radius=8)
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=30, pady=(30, 5), ipadx=100, ipady=50)

        self.input_entry = customtkinter.CTkEntry(master=self.frame, width=400, height=30, font=("Helvetica", 24),
                                                  corner_radius=8, placeholder_text="Start Typing...")
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10, ipady=5)
        self.input_entry.bind("<KeyRelease>", self.start)

        self.speed_label = customtkinter.CTkLabel(master=self.frame, text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n"
                                                                          "0.00 WPM\n\nMistakes: 0",
                                                  font=("Helvetica", 16))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=50)

        self.reset_button = customtkinter.CTkButton(master=self.frame, text="Reset", border_width=2, command=self.reset,
                                                    corner_radius=8)
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=30, ipady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.mistakes = 0
        self.running = False

    def reset(self):
        self.after(100, self.update_speed_labels)
        self.running = False
        self.counter = 0
        self.mistakes = 0
        self.input_entry.delete(0, customtkinter.END)
        self.response = requests.get(f"{self.endpoint}/quotes/random", params={"maxLength": 50})
        self.response.raise_for_status()
        self.sample_label.configure(text=self.response.json()[0]["content"])

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get().split(" ")) / self.counter
            wpm = wps * 60
            self.speed_label.configure(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM\n{wps:.2f} WPS\n {wpm:.2F} WPM\n\n"
                                            f"Mistakes: {self.mistakes}")

    def update_speed_labels(self):
        self.input_entry.configure(text_color="white")
        self.speed_label.configure(text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM\n\nMistakes: 0")

    def start(self, event):
        if not self.running:
            if event.keycode not in [8, 9, 16, 17, 18, 20, 91]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.daemon = True
                t.start()
        if not self.sample_label.cget("text").startswith(self.input_entry.get()):
            if event.keycode not in [8, 9, 16, 17, 18, 20, 91]:
                self.input_entry.configure(text_color="red")
                self.mistakes += 1
        else:
            self.input_entry.configure(text_color="white")
        if self.input_entry.get() == self.sample_label.cget("text"):
            self.running = False
            self.input_entry.configure(text_color="green")


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
app = App()
app.mainloop()
