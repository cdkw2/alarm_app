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

class AlarmApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Alarm App")
        self.master.geometry("500x700")
        self.master.resizable(False, False)

        self.alarm_sound = "default_alarm.wav"
        self.alarms = []
        
        self.load_images()
        self.setup_ui()
        
    def load_images(self):
        # Load and resize images for buttons
        button_size = (50, 50)  # Consistent size for all icons
        self.img_alarm = ImageTk.PhotoImage(Image.open("alarm_icon.png").resize(button_size))
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
        self.canvas = tk.Canvas(self.master, width=500, height=700, bg="#2c0bb0")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0, 620, 500, 700, fill="#1a0663", outline="")
        
    def create_buttons(self):
        buttons = [
            ('Alarms', self.img_alarm, 30, 630),
            ('World\nClock', self.img_world, 150, 630, self.open_world_clock),
            ('Stopwatch', self.img_stopwatch, 270, 630, self.open_stopwatch),
            ('Timer', self.img_timer, 390, 630, self.open_timer)
        ]
        
        for text, image, x, y, *args in buttons:
            command = args[0] if args else None
            btn = tk.Button(self.master, image=image, text=text, compound=tk.TOP, 
                            font=("Helvetica", 10, "bold"), fg="white", bg="#1a0663", 
                            bd=0, command=command)
            btn.place(x=x, y=y)
        
        add_alarm_btn = tk.Button(self.master, text="+ Add New Alarm", font=("Helvetica", 12, "bold"), 
                                  fg="white", bg="#4CAF50", command=self.open_alarm_page)
        add_alarm_btn.place(x=175, y=310, width=150, height=40)
        
    def create_labels(self):
        tk.Label(self.master, text='Good Afternoon, User', font=("Helvetica", 24, "bold"), 
                 fg="white", bg="#2c0bb0").place(x=20, y=20)
        tk.Label(self.master, text='Your Alarms', font=("Helvetica", 18, "bold"), 
                 fg="white", bg="#2c0bb0").place(x=20, y=360)
        
    def create_analog_clock(self):
        self.clock_canvas = tk.Canvas(self.master, width=250, height=250, bg='#2c0bb0', highlightthickness=0)
        self.clock_canvas.place(x=125, y=60)
        self.draw_clock_face()
        self.update_clock()
        
    def draw_clock_face(self):
        # Draw clock circle
        self.clock_canvas.create_oval(10, 10, 240, 240, outline="white", width=3)
        # Draw hour markers
        for i in range(12):
            angle = i * math.pi/6 - math.pi/2
            x1 = 125 + 105 * math.cos(angle)
            y1 = 125 + 105 * math.sin(angle)
            x2 = 125 + 115 * math.cos(angle)
            y2 = 125 + 115 * math.sin(angle)
            self.clock_canvas.create_line(x1, y1, x2, y2, fill="white", width=3)
        
    def update_clock(self):
        # Clear previous hands
        self.clock_canvas.delete("hands")
        
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second

        # Hour hand
        hour_angle = (hour + minute/60) * math.pi/6 - math.pi/2
        hour_x = 125 + 70 * math.cos(hour_angle)
        hour_y = 125 + 70 * math.sin(hour_angle)
        self.clock_canvas.create_line(125, 125, hour_x, hour_y, fill="white", width=6, tags="hands")

        # Minute hand
        minute_angle = (minute + second/60) * math.pi/30 - math.pi/2
        minute_x = 125 + 90 * math.cos(minute_angle)
        minute_y = 125 + 90 * math.sin(minute_angle)
        self.clock_canvas.create_line(125, 125, minute_x, minute_y, fill="white", width=4, tags="hands")

        # Second hand
        second_angle = second * math.pi/30 - math.pi/2
        second_x = 125 + 100 * math.cos(second_angle)
        second_y = 125 + 100 * math.sin(second_angle)
        self.clock_canvas.create_line(125, 125, second_x, second_y, fill="red", width=2, tags="hands")

        # Draw center circle
        self.clock_canvas.create_oval(120, 120, 130, 130, fill="white", outline="")

        self.master.after(1000, self.update_clock)

    def create_alarm_list(self):
        self.alarm_frame = tk.Frame(self.master, bg="#2c0bb0")
        self.alarm_frame.place(x=20, y=400, width=460, height=210)
        
        self.alarm_canvas = tk.Canvas(self.alarm_frame, bg="#2c0bb0", highlightthickness=0)
        self.alarm_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.inner_frame = tk.Frame(self.alarm_canvas, bg="#2c0bb0")
        self.alarm_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Only add scrollbar if needed
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
            frame = tk.Frame(self.inner_frame, bg="#3d14d1", bd=1, relief=tk.RAISED)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            name_label = tk.Label(frame, text=alarm_name, font=("Helvetica", 12, "bold"), fg="white", bg="#3d14d1")
            name_label.pack(side=tk.LEFT, padx=10)
            
            time_label = tk.Label(frame, text=alarm_time.strftime("%H:%M"), font=("Helvetica", 12), fg="white", bg="#3d14d1")
            time_label.pack(side=tk.LEFT, padx=10)
            
            delete_btn = tk.Button(frame, text="Delete", command=lambda idx=i: self.delete_alarm(idx))
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
                winsound.PlaySound(self.alarm_sound, winsound.SND_ASYNC | winsound.SND_LOOP)
                if messagebox.askokcancel("Alarm", f"{alarm_name}\nTime to wake up! Click OK to stop the alarm."):
                    winsound.PlaySound(None, 0)  # Stop the sound
                break
            
    def open_alarm_page(self):
        AlarmPage(self.master, self)

    def open_world_clock(self):
        WorldClockPage(self.master)

    def open_stopwatch(self):
        StopwatchPage(self.master)

    def open_timer(self):
        TimerPage(self.master)


class AlarmPage(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("Set Alarm")
        self.geometry("400x300")
        self.configure(bg="#2c0bb0")
        self.setup_ui()
        
    def setup_ui(self):
        tk.Label(self, text="Set New Alarm", font=("Helvetica", 20, "bold"), fg="white", bg="#2c0bb0").pack(pady=10)
        
        name_frame = tk.Frame(self, bg="#2c0bb0")
        name_frame.pack(pady=10)
        tk.Label(name_frame, text="Alarm Name:", font=("Helvetica", 12), fg="white", bg="#2c0bb0").pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(name_frame, font=("Helvetica", 12))
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        time_frame = tk.Frame(self, bg="#2c0bb0")
        time_frame.pack(pady=10)
        tk.Label(time_frame, text="Set Time:", font=("Helvetica", 12), fg="white", bg="#2c0bb0").pack(side=tk.LEFT, padx=5)
        
        self.hour = tk.StringVar(value="00")
        self.minute = tk.StringVar(value="00")
        
        ttk.OptionMenu(time_frame, self.hour, "00", *[f"{i:02d}" for i in range(24)]).pack(side=tk.LEFT, padx=5)
        ttk.OptionMenu(time_frame, self.minute, "00", *[f"{i:02d}" for i in range(60)]).pack(side=tk.LEFT, padx=5)
        
        tk.Button(self, text="Set Alarm", font=("Helvetica", 12, "bold"), fg="white", bg="#4CAF50", command=self.set_alarm).pack(pady=20)
        
        tk.Button(self, text="Select Ringtone", font=("Helvetica", 12), fg="white", bg="#3d14d1", command=self.select_ringtone).pack()
        
        self.ringtone_label = tk.Label(self, text=f"Current ringtone: {os.path.basename(self.app.alarm_sound)}", 
                                       font=("Helvetica", 10), fg="white", bg="#2c0bb0")
        self.ringtone_label.pack(pady=5)
        
    def set_alarm(self):
        alarm_name = self.name_entry.get() or "Alarm"
        alarm_time = datetime.now().replace(
            hour=int(self.hour.get()),
            minute=int(self.minute.get()),
            second=0,
            microsecond=0
        )
        self.app.add_alarm(alarm_time, alarm_name)
        self.destroy()
    
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
        tk.Label(self, text="68 + 1 = ", font=("Serif", 18, "bold")).place(x=100, y=60)
        
        self.entry = tk.Entry(self)
        self.entry.place(x=200, y=70)
        
        tk.Button(self, text="Submit", command=self.check_answer).place(x=180, y=100)
        
    def check_answer(self):
        if self.entry.get() == "69":
            winsound.PlaySound(None, 0)
            self.destroy()

class WorldClockPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("World Clock")
        self.geometry("500x400")
        self.cities = [
            ("New York", "America/New_York"),
            ("London", "Europe/London"),
            ("Tokyo", "Asia/Tokyo"),
            ("Sydney", "Australia/Sydney"),
            ("Moscow", "Europe/Moscow")
        ]
        self.setup_ui()
        
    def setup_ui(self):
        tk.Label(self, text="World Clock", font=("Helvetica", 20, "bold"), fg="blue").pack(pady=10)
        
        self.clock_frames = {}
        self.clock_labels = {}
        
        for city, timezone in self.cities:
            frame = tk.Frame(self)
            frame.pack(pady=5)
            
            tk.Label(frame, text=f"{city}:", font=("Helvetica", 14, "bold")).pack(side=tk.LEFT, padx=(0, 10))
            
            time_label = tk.Label(frame, text="", font=("Helvetica", 14))
            time_label.pack(side=tk.LEFT)
            
            self.clock_frames[city] = frame
            self.clock_labels[city] = time_label
        
        self.update_world_clocks()
        
    def update_world_clocks(self):
        for city, timezone in self.cities:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz).strftime('%H:%M:%S %p')
            self.clock_labels[city].config(text=current_time)
        
        self.after(1000, self.update_world_clocks)

class StopwatchPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Stopwatch")
        self.geometry("300x200")
        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.setup_ui()

    def setup_ui(self):
        self.time_label = tk.Label(self, text="00:00:00.000", font=("Helvetica", 24))
        self.time_label.pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.start_stop_button = tk.Button(button_frame, text="Start", command=self.toggle_stopwatch)
        self.start_stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_stopwatch)
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def toggle_stopwatch(self):
        if self.running:
            self.running = False
            self.start_stop_button.config(text="Start")
        else:
            self.running = True
            self.start_stop_button.config(text="Stop")
            self.start_time = datetime.now() - self.elapsed_time
            self.update_stopwatch()

    def update_stopwatch(self):
        if self.running:
            self.elapsed_time = datetime.now() - self.start_time
            self.update_display()
            self.after(50, self.update_stopwatch)

    def update_display(self):
        hours, remainder = divmod(self.elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = self.elapsed_time.microseconds // 1000
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}"
        self.time_label.config(text=time_str)

    def reset_stopwatch(self):
        self.running = False
        self.start_stop_button.config(text="Start")
        self.elapsed_time = timedelta()
        self.update_display()

class TimerPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Timer")
        self.geometry("300x250")
        self.running = False
        self.remaining_time = timedelta()
        self.setup_ui()

    def setup_ui(self):
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        self.hours_entry = tk.Entry(input_frame, width=3)
        self.hours_entry.pack(side=tk.LEFT)
        tk.Label(input_frame, text="h").pack(side=tk.LEFT)

        self.minutes_entry = tk.Entry(input_frame, width=3)
        self.minutes_entry.pack(side=tk.LEFT)
        tk.Label(input_frame, text="m").pack(side=tk.LEFT)

        self.seconds_entry = tk.Entry(input_frame, width=3)
        self.seconds_entry.pack(side=tk.LEFT)
        tk.Label(input_frame, text="s").pack(side=tk.LEFT)

        self.time_label = tk.Label(self, text="00:00:00", font=("Helvetica", 24))
        self.time_label.pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.start_stop_button = tk.Button(button_frame, text="Start", command=self.toggle_timer)
        self.start_stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=5)

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
            messagebox.showinfo("Timer", "Time's up!")

    def update_display(self):
        hours, remainder = divmod(self.remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        self.time_label.config(text=time_str)

    def reset_timer(self):
        self.running = False
        self.start_stop_button.config(text="Start")
        self.remaining_time = timedelta()
        self.time_label.config(text="00:00:00")
        self.hours_entry.delete(0, tk.END)
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
