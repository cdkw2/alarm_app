import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import time
import winsound
from threading import Thread
import pytz
import os
import math
from PIL import Image, ImageTk
import random

class AlarmApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Alarm App")
        self.master.geometry("500x700")
        self.master.resizable(False, False)

        self.alarm_sound = "default_alarm.wav"
        self.alarms = []
        self.ringtones = ["default_alarm.wav", "surfing.wav", "megalovania.wav", "metal_pipe.wav"]
        
        self.themes = {
            "Default": {
                "bg": "#2c0bb0", "fg": "white", "button_bg": "#1a0663",
                "clock_bg": "grey", "clock_fg": "white", "clock_hands": "white", "clock_second_hand": "red"
            },
            "Dark": {
                "bg": "#1e1e1e", "fg": "white", "button_bg": "#2e2e2e",
                "clock_bg": "#2e2e2e", "clock_fg": "white", "clock_hands": "white", "clock_second_hand": "red"
            },
            "Light": {
                "bg": "#f0f0f0", "fg": "black", "button_bg": "#e0e0e0",
                "clock_bg": "#e0e0e0", "clock_fg": "black", "clock_hands": "black", "clock_second_hand": "red"
            },
            "Pink": {
                "bg": "#ffc0cb", "fg": "#ff69b4", "button_bg": "#ffb6c1",
                "clock_bg": "#ffb6c1", "clock_fg": "#ff69b4", "clock_hands": "#ff69b4", "clock_second_hand": "#ff1493"
            },
            "Purple": {
                "bg": "#6a0dad", "fg": "white", "button_bg": "#4b0082",
                "clock_bg": "#4b0082", "clock_fg": "white", "clock_hands": "white", "clock_second_hand": "#8a2be2"
            },
            "Ocean": {
                "bg": "#00bcd4", "fg": "white", "button_bg": "#0097a7",
                "clock_bg": "#0097a7", "clock_fg": "white", "clock_hands": "white", "clock_second_hand": "#ff5722"
            },
            "Sunset": {
                "bg": "#ff5722", "fg": "white", "button_bg": "#e64a19",
                "clock_bg": "#e64a19", "clock_fg": "white", "clock_hands": "white", "clock_second_hand": "#ff9800"
            },
            "Forest": {
                "bg": "#228b22", "fg": "white", "button_bg": "#006400",
                "clock_bg": "#006400", "clock_fg": "white", "clock_hands": "white", "clock_second_hand": "#2e8b57"
            }
        }
        
        self.current_theme = "Default"
        
        self.load_images()
        self.setup_ui()
        
    def load_images(self):
        button_size = (50, 50)
        self.img_settings = ImageTk.PhotoImage(Image.open("settings_icon.png").resize(button_size))
        self.img_world = ImageTk.PhotoImage(Image.open("world_icon.png").resize(button_size))
        self.img_stopwatch = ImageTk.PhotoImage(Image.open("stopwatch_icon.png").resize(button_size))
        self.img_timer = ImageTk.PhotoImage(Image.open("timer_icon.png").resize(button_size))
        
    def setup_ui(self):
        self.create_canvas()
        self.create_buttons()
        self.create_labels()
        self.create_analog_clock()
        self.create_alarm_list()
        
    def create_canvas(self):
        self.canvas = tk.Canvas(self.master, width=500, height=700, bg=self.themes[self.current_theme]["bg"])
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0, 620, 500, 700, fill=self.themes[self.current_theme]["button_bg"], outline="")
        
    def create_buttons(self):
        buttons = [
            ('Settings', self.img_settings, 30, 630, self.open_settings),
            ('World\nClock', self.img_world, 150, 630, self.open_world_clock),
            ('Stopwatch', self.img_stopwatch, 270, 630, self.open_stopwatch),
            ('Timer', self.img_timer, 390, 630, self.open_timer)
        ]
        
        for text, image, x, y, command in buttons:
            btn = tk.Button(self.master, image=image, text=text, compound=tk.TOP, 
                            font=("Helvetica", 10, "bold"), fg=self.themes[self.current_theme]["fg"], 
                            bg=self.themes[self.current_theme]["button_bg"], 
                            bd=0, command=command)
            btn.place(x=x, y=y)
        
        add_alarm_btn = tk.Button(self.master, text="+ Add New Alarm", font=("Helvetica", 12, "bold"), 
                              fg=self.themes[self.current_theme]["fg"], bg="#4CAF50", command=self.open_alarm_page)
        add_alarm_btn.place(relx=0.5, y=340, anchor=tk.CENTER, width=150, height=40)
        
    def create_labels(self):
        greeting_label = tk.Label(self.master, text='SANS', font=("Consolas", 24, "bold"), 
                 fg=self.themes[self.current_theme]["fg"], bg=self.themes[self.current_theme]["bg"])
        greeting_label.place(relx=0.5, y=20, anchor=tk.N)
        
        alarms_label = tk.Label(self.master, text='Your Alarms', font=("Helvetica", 18, "bold"), 
                 fg=self.themes[self.current_theme]["fg"], bg=self.themes[self.current_theme]["bg"])
        alarms_label.place(relx=0.5, y=380, anchor=tk.CENTER)

    def create_analog_clock(self):
        self.clock_canvas = tk.Canvas(self.master, width=250, height=250, bg=self.themes[self.current_theme]["clock_bg"], highlightthickness=0)
        self.clock_canvas.place(relx=0.5, y=185, anchor=tk.CENTER)
        self.draw_clock_face()
        self.update_clock()
        
    def draw_clock_face(self):
        self.clock_canvas.create_oval(10, 10, 240, 240, outline=self.themes[self.current_theme]["clock_fg"], width=3)
        for i in range(12):
            angle = i * math.pi/6 - math.pi/2
            x1 = 125 + 105 * math.cos(angle)
            y1 = 125 + 105 * math.sin(angle)
            x2 = 125 + 115 * math.cos(angle)
            y2 = 125 + 115 * math.sin(angle)
            self.clock_canvas.create_line(x1, y1, x2, y2, fill=self.themes[self.current_theme]["clock_fg"], width=3)
        
    def update_clock(self):
        self.clock_canvas.delete("hands")
        
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second

        hour_angle = (hour + minute/60) * math.pi/6 - math.pi/2
        hour_x = 125 + 70 * math.cos(hour_angle)
        hour_y = 125 + 70 * math.sin(hour_angle)
        self.clock_canvas.create_line(125, 125, hour_x, hour_y, fill=self.themes[self.current_theme]["clock_hands"], width=6, tags="hands")

        minute_angle = (minute + second/60) * math.pi/30 - math.pi/2
        minute_x = 125 + 90 * math.cos(minute_angle)
        minute_y = 125 + 90 * math.sin(minute_angle)
        self.clock_canvas.create_line(125, 125, minute_x, minute_y, fill=self.themes[self.current_theme]["clock_hands"], width=4, tags="hands")

        second_angle = second * math.pi/30 - math.pi/2
        second_x = 125 + 100 * math.cos(second_angle)
        second_y = 125 + 100 * math.sin(second_angle)
        self.clock_canvas.create_line(125, 125, second_x, second_y, fill=self.themes[self.current_theme]["clock_second_hand"], width=2, tags="hands")

        self.clock_canvas.create_oval(120, 120, 130, 130, fill=self.themes[self.current_theme]["clock_hands"], outline="")

        self.master.after(1000, self.update_clock)

    def create_alarm_list(self):
        self.alarm_frame = tk.Frame(self.master, bg=self.themes[self.current_theme]["bg"])
        self.alarm_frame.place(relx=0.5, y=510, anchor=tk.CENTER, width=460, height=210)
        
        self.alarm_canvas = tk.Canvas(self.alarm_frame, bg=self.themes[self.current_theme]["bg"], highlightthickness=0)
        self.alarm_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.inner_frame = tk.Frame(self.alarm_canvas, bg=self.themes[self.current_theme]["bg"])
        self.alarm_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.alarm_canvas.configure(scrollregion=self.alarm_canvas.bbox("all"))
        if self.inner_frame.winfo_height() > self.alarm_frame.winfo_height():
            if not hasattr(self, 'scrollbar'):
                self.scrollbar = ttk.Scrollbar(self.alarm_frame, orient=tk.VERTICAL, command=self.alarm_canvas.yview)
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                self.alarm_canvas.configure(yscrollcommand=self.scrollbar.set)
        elif hasattr(self, 'scrollbar'):
            self.scrollbar.pack_forget()
            del self.scrollbar

    def add_alarm(self, alarm_time, alarm_name):
        self.alarms.append((alarm_time, alarm_name))
        self.update_alarm_list()
        Thread(target=self.run_alarm, args=(alarm_time, alarm_name), daemon=True).start()

    def update_alarm_list(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        for i, (alarm_time, alarm_name) in enumerate(self.alarms):
            frame = tk.Frame(self.inner_frame, bg=self.themes[self.current_theme]["button_bg"], bd=1, relief=tk.RAISED)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            name_label = tk.Label(frame, text=alarm_name, font=("Helvetica", 12, "bold"), 
                                  fg=self.themes[self.current_theme]["fg"], 
                                  bg=self.themes[self.current_theme]["button_bg"])
            name_label.pack(side=tk.LEFT, padx=10)
            
            time_label = tk.Label(frame, text=alarm_time.strftime("%H:%M"), font=("Helvetica", 12), 
                                  fg=self.themes[self.current_theme]["fg"], 
                                  bg=self.themes[self.current_theme]["button_bg"])
            time_label.pack(side=tk.LEFT, padx=10)
            
            delete_btn = tk.Button(frame, text="Delete", command=lambda idx=i: self.delete_alarm(idx),
                                   fg=self.themes[self.current_theme]["fg"], 
                                   bg=self.themes[self.current_theme]["button_bg"])
            delete_btn.pack(side=tk.RIGHT, padx=10)

        self.on_frame_configure(None)

    def delete_alarm(self, index):
        del self.alarms[index]
        self.update_alarm_list()

    def run_alarm(self, alarm_time, alarm_name):
        while True:
            time.sleep(1)
            now = datetime.now()
            if now.strftime("%H:%M") == alarm_time.strftime("%H:%M"):
                print(f"Time to Wake up - {alarm_name}")
                self.play_alarm_sound()
                if self.show_math_challenge():
                    self.stop_alarm_sound()
                    self.delete_alarm_by_time(alarm_time)
                    break

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        self.canvas.config(bg=self.themes[theme_name]["bg"])
        self.canvas.create_rectangle(0, 620, 500, 700, fill=self.themes[theme_name]["button_bg"], outline="")
        
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(fg=self.themes[theme_name]["fg"], bg=self.themes[theme_name]["button_bg"])
            elif isinstance(widget, tk.Label):
                widget.config(fg=self.themes[theme_name]["fg"], bg=self.themes[theme_name]["bg"])
        
        self.alarm_frame.config(bg=self.themes[theme_name]["bg"])
        self.alarm_canvas.config(bg=self.themes[theme_name]["bg"])
        self.inner_frame.config(bg=self.themes[theme_name]["bg"])
        
        self.clock_canvas.config(bg=self.themes[theme_name]["clock_bg"])
        self.clock_canvas.delete("all")
        self.draw_clock_face()
        
        self.update_alarm_list()
        
    def get_theme_colors(self):
        return self.themes[self.current_theme]
        
    def open_settings(self):
        SettingsPage(self.master, self) 

    def delete_alarm_by_time(self, alarm_time):
        self.alarms = [(time, name) for time, name in self.alarms if time != alarm_time]
        self.update_alarm_list()

    def open_settings(self):
        SettingsPage(self.master, self)
            
    def open_alarm_page(self):
        AlarmPage(self.master, self)

    def open_world_clock(self):
        WorldClockPage(self.master, self)

    def open_stopwatch(self):
        StopwatchPage(self.master, self)

    def open_timer(self):
        TimerPage(self.master, self)

    def play_alarm_sound(self):
        winsound.PlaySound(self.alarm_sound, winsound.SND_ASYNC | winsound.SND_LOOP)

    def stop_alarm_sound(self):
        winsound.PlaySound(None, 0)

    def show_math_challenge(self):
        theme_colors = self.get_theme_colors()
        challenge_window = MathChallenge(self.master, self, theme_colors)
        self.master.wait_window(challenge_window)
        return challenge_window.is_solved

class MathChallenge(tk.Toplevel):
    def __init__(self, parent, app, theme_colors):
        super().__init__(parent)
        self.app = app
        self.theme_colors = theme_colors
        self.title("Wake Up Challenge")
        self.geometry("300x250")
        self.is_solved = False
        self.questions_answered = 0
        self.total_questions = random.randint(3, 4)  # Randomly choose 3 or 4 questions
        self.configure(bg=self.theme_colors["bg"])
        self.setup_ui()
        
    def setup_ui(self):
        self.question, self.answer = self.generate_question()
        
        self.main_frame = tk.Frame(self, bg=self.theme_colors["bg"])
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.question_label = tk.Label(self.main_frame, text="Solve to stop the alarm:", 
                                       font=("Helvetica", 14, "bold"),
                                       fg=self.theme_colors["fg"],
                                       bg=self.theme_colors["bg"])
        self.question_label.pack(pady=10)
        
        self.math_label = tk.Label(self.main_frame, text=self.question, 
                                   font=("Helvetica", 18),
                                   fg=self.theme_colors["fg"],
                                   bg=self.theme_colors["bg"])
        self.math_label.pack(pady=10)
        
        self.entry = tk.Entry(self.main_frame, font=("Helvetica", 14),
                              bg=self.theme_colors["button_bg"],
                              fg=self.theme_colors["fg"],
                              insertbackground=self.theme_colors["fg"])
        self.entry.pack(pady=10)
        self.entry.focus()
        
        self.submit_button = tk.Button(self.main_frame, text="Submit", 
                                       command=self.check_answer,
                                       bg=self.theme_colors["button_bg"],
                                       fg=self.theme_colors["fg"],
                                       activebackground=self.theme_colors["bg"],
                                       activeforeground=self.theme_colors["fg"])
        self.submit_button.pack(pady=10)
        
        self.progress_label = tk.Label(self.main_frame, 
                                       text=f"Question {self.questions_answered + 1} of {self.total_questions}", 
                                       font=("Helvetica", 10),
                                       fg=self.theme_colors["fg"],
                                       bg=self.theme_colors["bg"])
        self.progress_label.pack(pady=5)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def generate_question(self):
        operations = ['+', '-', '*']
        operation = random.choice(operations)
        
        if operation == '+':
            a, b = random.randint(10, 50), random.randint(10, 50)
            return f"{a} + {b}", a + b
        elif operation == '-':
            a, b = random.randint(25, 75), random.randint(1, 25)
            return f"{a} - {b}", a - b
        else:  # multiplication
            a, b = random.randint(2, 12), random.randint(2, 12)
            return f"{a} × {b}", a * b
        
    def check_answer(self):
        user_answer = self.entry.get()
        self.questions_answered += 1
        
        if self.questions_answered < self.total_questions:
            self.new_question()
        else:
            try:
                if int(user_answer) == self.answer:
                    self.is_solved = True
                    messagebox.showinfo("Success", "Alarm turned off. Have a great day!")
                    self.destroy()
                else:
                    messagebox.showerror("Failed", "Wrong answer on the final question. Alarm continues!")
                    self.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")
                self.questions_answered -= 1  # Don't count this attempt
                
    def new_question(self):
        self.question, self.answer = self.generate_question()
        self.math_label.config(text=self.question)
        self.entry.delete(0, tk.END)
        self.progress_label.config(text=f"Question {self.questions_answered + 1} of {self.total_questions}")
        
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit? The alarm will continue."):
            self.destroy()

class AlarmPage(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("Set Alarm")
        self.geometry("400x300")
        self.setup_ui()
        
    def setup_ui(self):
        theme_colors = self.app.get_theme_colors()
        self.configure(bg=theme_colors["bg"])
        
        tk.Label(self, text="Set New Alarm", font=("Helvetica", 20, "bold"), fg=theme_colors["fg"], bg=theme_colors["bg"]).pack(pady=10)
        
        name_frame = tk.Frame(self, bg=theme_colors["bg"])
        name_frame.pack(pady=10)
        tk.Label(name_frame, text="Alarm Name:", font=("Helvetica", 12), fg=theme_colors["fg"], bg=theme_colors["bg"]).pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(name_frame, font=("Helvetica", 12))
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        time_frame = tk.Frame(self, bg=theme_colors["bg"])
        time_frame.pack(pady=10)
        tk.Label(time_frame, text="Set Time (HH:MM):", font=("Helvetica", 12), fg=theme_colors["fg"], bg=theme_colors["bg"]).pack(side=tk.LEFT, padx=5)
        
        self.time_entry = tk.Entry(time_frame, font=("Helvetica", 12), width=5)
        self.time_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self, text="Set Alarm", font=("Helvetica", 12, "bold"), fg=theme_colors["fg"], bg=theme_colors["button_bg"], command=self.set_alarm).pack(pady=20)
        
        tk.Label(self, text="Select Ringtone:", font=("Helvetica", 12), fg=theme_colors["fg"], bg=theme_colors["bg"]).pack()
        self.ringtone_var = tk.StringVar(value=self.app.alarm_sound)
        ringtone_menu = ttk.Combobox(self, textvariable=self.ringtone_var, values=self.app.ringtones, state="readonly")
        ringtone_menu.pack(pady=5)
        
    def set_alarm(self):
        alarm_name = self.name_entry.get() or "Alarm"
        time_str = self.time_entry.get()
        try:
            alarm_time = datetime.strptime(time_str, "%H:%M").time()
            alarm_datetime = datetime.combine(datetime.now().date(), alarm_time)
            if alarm_datetime <= datetime.now():
                alarm_datetime += timedelta(days=1)
            self.app.alarm_sound = self.ringtone_var.get()
            self.app.add_alarm(alarm_datetime, alarm_name)
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter a valid time in HH:MM format.")
    
    def select_ringtone(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.app.alarm_sound = file_path
            self.ringtone_label.config(text=f"Current ringtone: {os.path.basename(file_path)}")
            
class StopPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Stop Alarm")
        self.geometry("400x200")
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)
        
        tk.Label(main_frame, text="68 + 1 = ", font=("Serif", 18, "bold")).pack(pady=10)
        
        self.entry = tk.Entry(main_frame)
        self.entry.pack(pady=10)
        
        tk.Button(main_frame, text="Submit", command=self.check_answer).pack(pady=10)
        
    def check_answer(self):
        if self.entry.get() == "69":
            winsound.PlaySound(None, 0)
            self.destroy()

class WorldClockPage(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("World Clock")
        self.geometry("500x500")
        self.cities = [
            ("New York", "America/New_York"),
            ("London", "Europe/London"),
            ("Tokyo", "Asia/Tokyo"),
            ("Sydney", "Australia/Sydney"),
            ("Moscow", "Europe/Moscow")
        ]
        self.setup_ui()
        
    def setup_ui(self):
        theme_colors = self.app.get_theme_colors()
        self.configure(bg=theme_colors["bg"])
        
        tk.Label(self, text="World Clock", font=("Helvetica", 20, "bold"), fg=theme_colors["fg"], bg=theme_colors["bg"]).pack(pady=10)
        
        self.clock_frame = tk.Frame(self, bg=theme_colors["bg"])
        self.clock_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.clock_labels = {}
        self.update_clock_display()
        
        control_frame = tk.Frame(self, bg=theme_colors["bg"])
        control_frame.pack(pady=10, fill=tk.X)
        
        self.timezone_var = tk.StringVar()
        self.timezone_combo = ttk.Combobox(control_frame, textvariable=self.timezone_var, values=sorted(pytz.all_timezones), state="readonly", width=30)
        self.timezone_combo.pack(side=tk.LEFT, padx=5)
        
        add_button = tk.Button(control_frame, text="Add", command=self.add_timezone, fg=theme_colors["fg"], bg=theme_colors["button_bg"])
        add_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = tk.Button(control_frame, text="Remove", command=self.remove_timezone, fg=theme_colors["fg"], bg=theme_colors["button_bg"])
        remove_button.pack(side=tk.LEFT, padx=5)
        
    def update_clock_display(self):
        for widget in self.clock_frame.winfo_children():
            widget.destroy()
        
        theme_colors = self.app.get_theme_colors()
        for city, timezone in self.cities:
            frame = tk.Frame(self.clock_frame, bg=theme_colors["bg"])
            frame.pack(fill=tk.X, pady=2)
            
            city_label = tk.Label(frame, text=f"{city}:", font=("Helvetica", 14, "bold"), fg=theme_colors["fg"], bg=theme_colors["bg"], width=20, anchor="e")
            city_label.pack(side=tk.LEFT, padx=(0, 10))
            
            time_label = tk.Label(frame, text="", font=("Helvetica", 14), fg=theme_colors["fg"], bg=theme_colors["bg"], width=20, anchor="w")
            time_label.pack(side=tk.LEFT)
            
            self.clock_labels[city] = time_label
        
        self.update_world_clocks()
        
    def update_world_clocks(self):
        for city, timezone in self.cities:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz).strftime('%H:%M:%S %p')
            self.clock_labels[city].config(text=current_time)
        
        self.after(1000, self.update_world_clocks)
    
    def add_timezone(self):
        new_timezone = self.timezone_var.get()
        if new_timezone:
            city_name = new_timezone.split('/')[-1].replace('_', ' ')
            self.cities.append((city_name, new_timezone))
            self.update_clock_display()
    
    def remove_timezone(self):
        selected_timezone = self.timezone_var.get()
        self.cities = [city for city in self.cities if city[1] != selected_timezone]
        self.update_clock_display()

class TimerPage(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("Timer")
        self.geometry("300x500")
        self.running = False
        self.remaining_time = timedelta()
        self.timer_sound = "default_alarm.wav"
        self.setup_ui()

    def setup_ui(self):
        theme_colors = self.app.get_theme_colors()
        self.configure(bg=theme_colors["bg"])
        
        main_frame = tk.Frame(self, bg=theme_colors["bg"])
        main_frame.pack(expand=True)
        
        input_frame = tk.Frame(main_frame, bg=theme_colors["bg"])
        input_frame.pack(pady=10)

        self.hours_entry = tk.Entry(input_frame, width=3)
        self.hours_entry.pack(side=tk.LEFT)
        tk.Label(input_frame, text="h", fg=theme_colors["fg"], bg=theme_colors["bg"]).pack(side=tk.LEFT)

        self.minutes_entry = tk.Entry(input_frame, width=3)
        self.minutes_entry.pack(side=tk.LEFT)
        tk.Label(input_frame, text="m", fg=theme_colors["fg"], bg=theme_colors["bg"]).pack(side=tk.LEFT)

        self.seconds_entry = tk.Entry(input_frame, width=3)
        self.seconds_entry.pack(side=tk.LEFT)
        tk.Label(input_frame, text="s", fg=theme_colors["fg"], bg=theme_colors["bg"]).pack(side=tk.LEFT)

        self.canvas = tk.Canvas(main_frame, width=250, height=250, bg=theme_colors["clock_bg"], highlightthickness=0)
        self.canvas.pack(pady=20)

        self.draw_timer_face()

        self.time_label = tk.Label(main_frame, text="00:00:00", font=("Helvetica", 18), fg=theme_colors["fg"], bg=theme_colors["bg"])
        self.time_label.pack(pady=10)

        tk.Label(main_frame, text="Select Ringtone:", font=("Helvetica", 12), fg=theme_colors["fg"], bg=theme_colors["bg"]).pack()
        self.ringtone_var = tk.StringVar(value=self.timer_sound)
        ringtone_menu = ttk.Combobox(main_frame, textvariable=self.ringtone_var, values=self.app.ringtones, state="readonly")
        ringtone_menu.pack(pady=5)

        button_frame = tk.Frame(main_frame, bg=theme_colors["bg"])
        button_frame.pack(pady=10)

        self.start_stop_button = tk.Button(button_frame, text="Start", command=self.toggle_timer, fg=theme_colors["fg"], bg=theme_colors["button_bg"])
        self.start_stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_timer, fg=theme_colors["fg"], bg=theme_colors["button_bg"])
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def draw_timer_face(self):
        theme_colors = self.app.get_theme_colors()
        self.canvas.create_oval(10, 10, 240, 240, outline=theme_colors["clock_fg"], width=2)
        for i in range(60):
            angle = i * math.pi / 30 - math.pi / 2
            start = 110 if i % 5 == 0 else 115
            x1 = 125 + start * math.cos(angle)
            y1 = 125 + start * math.sin(angle)
            x2 = 125 + 120 * math.cos(angle)
            y2 = 125 + 120 * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill=theme_colors["clock_fg"])

    def toggle_timer(self):
        if self.running:
            self.running = False
            self.start_stop_button.config(text="Start")
        else:
            if self.remaining_time.total_seconds() == 0:
                try:
                    hours = int(self.hours_entry.get() or 0)
                    minutes = int(self.minutes_entry.get() or 0)
                    seconds = int(self.seconds_entry.get() or 0)
                    self.remaining_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter valid numbers for hours, minutes, and seconds.")
                    return

            self.running = True
            self.start_stop_button.config(text="Stop")
            self.update_timer()

    def update_timer(self):
        if self.running and self.remaining_time.total_seconds() > 0:
            self.remaining_time -= timedelta(seconds=1)
            self.update_display()
            self.after(1000, self.update_timer)
        elif self.remaining_time.total_seconds() <= 0:
            self.running = False
            self.start_stop_button.config(text="Start")
            self.time_label.config(text="00:00:00")
            self.canvas.delete("hands")
            self.play_timer_sound()
            self.show_times_up_message()

    def update_display(self):
        theme_colors = self.app.get_theme_colors()
        total_seconds = self.remaining_time.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        self.time_label.config(text=time_str)

        self.canvas.delete("hands")
        
        hour_angle = (hours + minutes / 60) * math.pi / 6 - math.pi / 2
        hour_x = 125 + 60 * math.cos(hour_angle)
        hour_y = 125 + 60 * math.sin(hour_angle)
        self.canvas.create_line(125, 125, hour_x, hour_y, fill=theme_colors["clock_hands"], width=4, tags="hands")

        minute_angle = (minutes + seconds / 60) * math.pi / 30 - math.pi / 2
        minute_x = 125 + 90 * math.cos(minute_angle)
        minute_y = 125 + 90 * math.sin(minute_angle)
        self.canvas.create_line(125, 125, minute_x, minute_y, fill=theme_colors["clock_hands"], width=3, tags="hands")

        second_angle = seconds * math.pi / 30 - math.pi / 2
        second_x = 125 + 110 * math.cos(second_angle)
        second_y = 125 + 110 * math.sin(second_angle)
        self.canvas.create_line(125, 125, second_x, second_y, fill=theme_colors["clock_second_hand"], width=2, tags="hands")

    def reset_timer(self):
        self.running = False
        self.start_stop_button.config(text="Start")
        self.remaining_time = timedelta()
        self.time_label.config(text="00:00:00")
        self.hours_entry.delete(0, tk.END)
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.canvas.delete("hands")

    def play_timer_sound(self):
        selected_sound = self.ringtone_var.get()
        winsound.PlaySound(selected_sound, winsound.SND_ASYNC | winsound.SND_LOOP)

    def show_times_up_message(self):
        messagebox.showinfo("Timer", "Time's up!")
        winsound.PlaySound(None, winsound.SND_PURGE)

class StopwatchPage(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("Stopwatch")
        self.geometry("300x400")
        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.setup_ui()

    def setup_ui(self):
        theme_colors = self.app.get_theme_colors()
        self.configure(bg=theme_colors["bg"])
        
        main_frame = tk.Frame(self, bg=theme_colors["bg"])
        main_frame.pack(expand=True)
        
        self.canvas = tk.Canvas(main_frame, width=250, height=250, bg=theme_colors["clock_bg"], highlightthickness=0)
        self.canvas.pack(pady=20)

        self.draw_stopwatch_face()
        
        self.time_label = tk.Label(main_frame, text="00:00:00.000", font=("Helvetica", 18), fg=theme_colors["fg"], bg=theme_colors["bg"])
        self.time_label.pack(pady=10)

        button_frame = tk.Frame(main_frame, bg=theme_colors["bg"])
        button_frame.pack(pady=10)

        self.start_stop_button = tk.Button(button_frame, text="Start", command=self.toggle_stopwatch, fg=theme_colors["fg"], bg=theme_colors["button_bg"])
        self.start_stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_stopwatch, fg=theme_colors["fg"], bg=theme_colors["button_bg"])
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def draw_stopwatch_face(self):
        theme_colors = self.app.get_theme_colors()
        self.canvas.create_oval(10, 10, 240, 240, outline=theme_colors["clock_fg"], width=2)
        for i in range(60):
            angle = i * math.pi / 30 - math.pi / 2
            start = 110 if i % 5 == 0 else 115
            x1 = 125 + start * math.cos(angle)
            y1 = 125 + start * math.sin(angle)
            x2 = 125 + 120 * math.cos(angle)
            y2 = 125 + 120 * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill=theme_colors["clock_fg"])

    def toggle_stopwatch(self):
        if self.running:
            self.running = False
            self.start_stop_button.config(text="Start")
        else:
            self.running = True
            self.start_stop_button.config(text="Stop")
            self.start_time = time.time() - self.elapsed_time.total_seconds()
            self.update_stopwatch()

    def update_stopwatch(self):
        if self.running:
            self.elapsed_time = timedelta(seconds=time.time() - self.start_time)
            self.update_display()
            self.after(16, self.update_stopwatch)

    def update_display(self):
        theme_colors = self.app.get_theme_colors()
        total_seconds = self.elapsed_time.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}"
        self.time_label.config(text=time_str)

        self.canvas.delete("hands")
        
        minute_angle = total_seconds / 30 - math.pi / 2
        minute_x = 125 + 90 * math.cos(minute_angle)
        minute_y = 125 + 90 * math.sin(minute_angle)
        self.canvas.create_line(125, 125, minute_x, minute_y, fill=theme_colors["clock_hands"], width=3, tags="hands")

        second_angle = (total_seconds % 60) * math.pi / 30 - math.pi / 2
        second_x = 125 + 110 * math.cos(second_angle)
        second_y = 125 + 110 * math.sin(second_angle)
        self.canvas.create_line(125, 125, second_x, second_y, fill=theme_colors["clock_second_hand"], width=2, tags="hands")

    def reset_stopwatch(self):
        self.running = False
        self.start_stop_button.config(text="Start")
        self.elapsed_time = timedelta()
        self.update_display()
        self.canvas.delete("hands")

class SettingsPage(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("Settings")
        self.geometry("300x200")
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)
        
        tk.Label(main_frame, text="Settings", font=("Helvetica", 20, "bold")).pack(pady=10)
        
        tk.Label(main_frame, text="Select Theme:").pack()
        self.theme_var = tk.StringVar(value=self.app.current_theme)
        theme_menu = ttk.Combobox(main_frame, textvariable=self.theme_var, values=list(self.app.themes.keys()), state="readonly")
        theme_menu.pack(pady=5)
        
        apply_button = tk.Button(main_frame, text="Apply Theme", command=self.apply_theme)
        apply_button.pack(pady=10)
        
    def apply_theme(self):
        selected_theme = self.theme_var.get()
        self.app.apply_theme(selected_theme)
        messagebox.showinfo("Theme Applied", f"The {selected_theme} theme has been applied.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
