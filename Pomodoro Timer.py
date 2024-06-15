import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style, PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import playsound
import threading
import time
import os
from datetime import datetime
import json

# Set the default time for work and break intervals
WORK_TIME = 1 * 60
SHORT_BREAK_TIME = 5 * 60
LONG_BREAK_TIME = 15 * 60

# Paths to sound files
WORK_SOUND_PATH = r"C:\Pomodoro Timer\Timer Sound Effect.mp3"
SHORT_BREAK_SOUND_PATH = r"C:\Pomodoro Timer\alarm-clock-short_break sound.mp3"
END_WORK_SOUND_PATH = r"C:\Pomodoro Timer\clock-alarm_end work sound.mp3"
END_BREAK_SOUND_PATH = r"C:\Pomodoro Timer\alarm-clock-short_break sound.mp3"
TICK_SOUND_PATH = r"C:\Pomodoro Timer\tick_sound.mp3"  # Path to ticking sound

# Path to history data file
HISTORY_FILE_PATH = "pomodoro_history.json"

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.title("Pomodoro Timer")
        self.style = Style(theme="simplex")
        self.style.theme_use()

        self.work_time = WORK_TIME
        self.short_break_time = SHORT_BREAK_TIME
        self.long_break_time = LONG_BREAK_TIME
        self.is_work_time = True
        self.pomodoros_completed = 0
        self.is_running = False
        self.ticking_thread = None
        self.stop_ticking = threading.Event()

        # Track time spent in work and break
        self.time_spent_working = 0
        self.time_spent_breaking = 0

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(pady=10)

        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.pack_forget()

        self.home_frame = ttk.Frame(self.main_frame)
        self.home_frame.pack(fill="both", expand=True)

        self.stats_frame = ttk.Frame(self.main_frame)
        self.stats_frame.pack_forget()

        self.load_icons()
        self.create_widgets()

        self.history_data = self.load_history()

    def create_widgets(self):
        self.nav_frame_widgets()
        self.home_frame_widgets()
        self.settings_frame_widget()
        self.stats_frame_widgets()

    def load_icons(self):
        icon_paths = {
            "timer_icon": "timer_icon.png",
            "preadded_icon": "preadded.png",
        }
        self.icons = {}
        for name, path in icon_paths.items():
            icon_image = PhotoImage(file=path)
            resize_icon = icon_image.subsample(8)
            self.icons[name] = resize_icon

    def nav_frame_widgets(self):
        self.home_button = ttk.Button(self.nav_frame, text="Home", width=10, command=self.show_home)
        self.home_button.grid(row=0, column=0, padx=10)

        self.settings_button = ttk.Button(self.nav_frame, text="Settings", width=10, command=self.show_settings)
        self.settings_button.grid(row=0, column=1, padx=10)

        self.stats_button = ttk.Button(self.nav_frame, text="Stats", width=10, command=self.show_stats)
        self.stats_button.grid(row=0, column=2, padx=10)

    def home_frame_widgets(self):
        self.timer_minutes = WORK_TIME // 60
        self.timer_seconds = WORK_TIME % 60
        self.timer_label = tk.Label(self.home_frame, text="{:02d}:{:02d}".format(self.timer_minutes, self.timer_seconds), font=("TkDefaultFont", 40))
        self.timer_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.start_button = ttk.Button(self.home_frame, text="Start", command=self.start_timer, width=10)
        self.start_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

    def settings_frame_widget(self):
        self.settings_subtitle_label = ttk.Label(self.settings_frame, text="Timer", font=("TkDefaultFont", 18, "bold"))
        self.settings_subtitle_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        timer_icon = self.icons["timer_icon"]
        self.settings_icon_label = ttk.Label(self.settings_frame, image=timer_icon)
        self.settings_icon_label.place(relx=0.46, rely=0.049, anchor=tk.CENTER)

        self.work_label = ttk.Label(self.settings_frame, text="Work Time (minutes):", font=("TKDefaultFont", 10))
        self.work_label.place(relx=0.5, rely=0.11, anchor=tk.CENTER)
        self.work_entry = ttk.Entry(self.settings_frame)
        self.work_entry.insert(0, str(WORK_TIME // 60))
        self.work_entry.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        self.short_break_label = ttk.Label(self.settings_frame, text="Short Break Time (minutes):", font=("TKDefaultFont", 10))
        self.short_break_label.place(relx=0.5, rely=0.19, anchor=tk.CENTER)
        self.short_break_entry = ttk.Entry(self.settings_frame)
        self.short_break_entry.insert(0, str(SHORT_BREAK_TIME // 60))
        self.short_break_entry.place(relx=0.5, rely=0.23, anchor=tk.CENTER)

        self.long_break_label = ttk.Label(self.settings_frame, text="Long Break Time (minutes):", font=("TKDefaultFont", 10))
        self.long_break_label.place(relx=0.5, rely=0.27, anchor=tk.CENTER)
        self.long_break_entry = ttk.Entry(self.settings_frame)
        self.long_break_entry.insert(0, str(LONG_BREAK_TIME // 60))
        self.long_break_entry.place(relx=0.5, rely=0.31, anchor=tk.CENTER)

        self.save_button = ttk.Button(self.settings_frame, text="Save", command=self.save_settings)
        self.save_button.place(relx=0.5, rely=0.37, anchor=tk.CENTER)

        self.preadded_timers_label = ttk.Label(self.settings_frame, text="Pre-added Timers", font=("TkDefaultFont", 18, "bold"))
        self.preadded_timers_label.place(relx=0.5, rely=0.47, anchor=tk.CENTER)
        preadded_icon = self.icons["preadded_icon"]
        self.settings_icon_label = ttk.Label(self.settings_frame, image=preadded_icon)
        self.settings_icon_label.place(relx=0.41, rely=0.47, anchor=tk.CENTER)

        self.preadded_timers_listbox = tk.Listbox(self.settings_frame, height=4, width=40, bd=0, highlightthickness=0, font=("TkDefaultFont", 12))
        self.preadded_timers_listbox.insert(1, "    Deep Work Session")
        self.preadded_timers_listbox.insert(2, "    Light Work Session")
        self.preadded_timers_listbox.insert(3, "    Exercise Session")
        self.preadded_timers_listbox.insert(4, "    Study Session")
        self.preadded_timers_listbox.place(relx=0.5, rely=0.57, anchor=tk.CENTER)

    def show_home(self):
        self.settings_frame.pack_forget()
        self.stats_frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)

    def show_settings(self):
        self.home_frame.pack_forget()
        self.stats_frame.pack_forget()
        self.settings_frame.pack(fill="both", expand=True)

    def show_stats(self):
        self.home_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.stats_frame.pack(fill="both", expand=True)
        self.update_stats()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(text="Stop", command=self.stop_timer)
            self.stop_ticking.clear()
            self.run_timer()
            self.start_ticking()

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="Start", command=self.start_timer)
            self.stop_ticking.set()

    def run_timer(self):
        def timer_thread():
            time_left = self.work_time if self.is_work_time else self.short_break_time
            while time_left > 0 and self.is_running:
                mins, secs = divmod(time_left, 60)
                self.timer_label.config(text="{:02d}:{:02d}".format(mins, secs))
                self.root.update()
                time.sleep(1)
                time_left -= 1

            if self.is_running:
                self.stop_ticking.set()
                self.timer_finished()

        threading.Thread(target=timer_thread).start()

    def start_ticking(self):
        def tick():
            while not self.stop_ticking.is_set():
                playsound.playsound(TICK_SOUND_PATH)
                time.sleep(1)

        self.ticking_thread = threading.Thread(target=tick)
        self.ticking_thread.start()

    def timer_finished(self):
        if self.is_work_time:
            self.time_spent_working += self.work_time
            self.play_sound(WORK_SOUND_PATH)  # Play work end sound
            self.log_activity("Work", self.work_time)
            self.show_rating_popup("Work")
            messagebox.showinfo("Timer Finished", "Work period has ended. Time for a break!")
        else:
            self.time_spent_breaking += self.short_break_time
            self.play_sound(SHORT_BREAK_SOUND_PATH)  # Play break end sound
            self.log_activity("Break", self.short_break_time)
            messagebox.showinfo("Timer Finished", "Break period has ended. Time to work!")

        self.pomodoros_completed += 1
        self.is_work_time = not self.is_work_time

        if self.pomodoros_completed > 0 and self.pomodoros_completed % 4 == 0:
            self.play_sound(END_BREAK_SOUND_PATH)
            time.sleep(self.long_break_time)
            messagebox.showinfo("Long Break", "Long break period has ended. Time to work!")
        else:
            next_period_time = self.short_break_time if self.is_work_time else self.work_time
            self.play_sound(END_BREAK_SOUND_PATH if not self.is_work_time else END_WORK_SOUND_PATH)
            time.sleep(next_period_time)

        self.is_running = False
        self.start_button.config(text="Start", command=self.start_timer)

    def play_sound(self, sound_file):
        def play():
            if os.path.exists(sound_file):
                try:
                    playsound.playsound(sound_file)
                except Exception as e:
                    print(f"Error playing sound: {e}")
            else:
                print(f"Sound file not found: {sound_file}")

        threading.Thread(target=play).start()

    def save_settings(self):
        try:
            self.work_time = int(self.work_entry.get()) * 60
            self.short_break_time = int(self.short_break_entry.get()) * 60
            self.long_break_time = int(self.long_break_entry.get()) * 60
            messagebox.showinfo("Settings Saved", "Your settings have been saved successfully.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for the time settings.")

    def stats_frame_widgets(self):
        self.stats_label = ttk.Label(self.stats_frame, text="Time Spent on Pomodoro Timer", font=("TkDefaultFont", 18, "bold"))
        self.stats_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.stats_canvas_frame = ttk.Frame(self.stats_frame)
        self.stats_canvas_frame.place(relx=0.5, rely=0.55, anchor=tk.CENTER, relwidth=0.8, relheight=0.7)

        self.fig, self.ax = plt.subplots()
        self.pie_chart = FigureCanvasTkAgg(self.fig, master=self.stats_canvas_frame)
        self.pie_chart.get_tk_widget().pack(fill="both", expand=True)

    def update_stats(self):
        total_time = self.time_spent_working + self.time_spent_breaking
        if total_time > 0:
            work_percentage = self.time_spent_working / total_time * 100
            break_percentage = self.time_spent_breaking / total_time * 100
            labels = ["Work", "Break"]
            sizes = [work_percentage, break_percentage]
            colors = ["#ff9999", "#66b3ff"]
            self.ax.clear()
            self.ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
            self.ax.axis("equal")
            self.pie_chart.draw()
        else:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "No data available", horizontalalignment="center", verticalalignment="center")
            self.pie_chart.draw()

    def run(self):
        self.root.mainloop()

    def load_history(self):
        if os.path.exists(HISTORY_FILE_PATH):
            with open(HISTORY_FILE_PATH, "r") as file:
                return json.load(file)
        return {}

    def save_history(self):
        with open(HISTORY_FILE_PATH, "w") as file:
            json.dump(self.history_data, file)

    def log_activity(self, activity_type, duration):
        date_str = datetime.now().strftime("%Y-%m-%d")
        if date_str not in self.history_data:
            self.history_data[date_str] = []

        activity_entry = {
            "type": activity_type,
            "duration": duration,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history_data[date_str].append(activity_entry)
        self.save_history()

    def show_rating_popup(self, activity_type):
        def submit_rating():
            rating = rating_var.get()
            self.log_activity_rating(activity_type, rating)
            rating_popup.destroy()

        rating_popup = tk.Toplevel(self.root)
        rating_popup.title("Rate Your Task")
        rating_popup.geometry("300x200")

        rating_label = ttk.Label(rating_popup, text="Rate your satisfaction:", font=("TkDefaultFont", 12))
        rating_label.pack(pady=10)

        rating_var = tk.IntVar()
        for i in range(1, 6):
            rating_radio = ttk.Radiobutton(rating_popup, text=f"{i} Star{'s' if i > 1 else ''}", variable=rating_var, value=i)
            rating_radio.pack(anchor=tk.W)

        submit_button = ttk.Button(rating_popup, text="Submit", command=submit_rating)
        submit_button.pack(pady=10)

    def log_activity_rating(self, activity_type, rating):
        date_str = datetime.now().strftime("%Y-%m-%d")
        if date_str not in self.history_data:
            self.history_data[date_str] = []

        rating_entry = {
            "type": activity_type,
            "rating": rating,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history_data[date_str].append(rating_entry)
        self.save_history()

if __name__ == "__main__":
    timer = PomodoroTimer()
    timer.run()