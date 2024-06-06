import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style, PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set the default time for work and break intervals
WORK_TIME = 1 * 60
SHORT_BREAK_TIME = 5 * 60
LONG_BREAK_TIME = 15 * 60

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
        self.preadded_timers_listbox.insert(4, "    Meditation Session")
        self.preadded_timers_listbox.place(relx=0.5, rely=0.57, anchor=tk.CENTER)

        self.timer_descriptions = {
            "Deep Work Session": "1 hour of focused work followed by a 15-minute break.",
            "Light Work Session": "45 minutes of work followed by a 5-minute break.",
            "Exercise Session": "1-minute work intervals with 15-second breaks for exercise.",
            "Meditation Session": "15 minutes of meditation followed by 5 minutes of stretching."
        }

        self.timer_description_label = ttk.Label(self.settings_frame, text="", font=("TkDefaultFont", 12), wraplength=500)
        self.timer_description_label.place(relx=0.5, rely=0.67, anchor=tk.CENTER)

        self.add_timer_button = ttk.Button(self.settings_frame, text="Try Out!", command=self.add_selected_timer)
        self.add_timer_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        self.preadded_timers_listbox.bind("<<ListboxSelect>>", self.update_description_label)

    def update_description_label(self, event):
        selected_timer = self.preadded_timers_listbox.get(self.preadded_timers_listbox.curselection())
        description = self.timer_descriptions.get(selected_timer.strip(), "No description available.")
        self.timer_description_label.config(text=description)

    def add_selected_timer(self):
        selected_timer = self.preadded_timers_listbox.get(self.preadded_timers_listbox.curselection())
        if selected_timer == "    Deep Work Session":
            self.work_time = 1 * 60
            self.short_break_time = 1 * 60
            self.long_break_time = 15 * 60
        elif selected_timer == "    Light Work Session":
            self.work_time = 45 * 60
            self.short_break_time = 5 * 60
            self.long_break_time = 15 * 60
        elif selected_timer == "    Exercise Session":
            self.work_time = 1 * 60
            self.short_break_time = 15
            self.long_break_time = 15 * 60
        elif selected_timer == "    Meditation Session":
            self.work_time = 15 * 60
            self.short_break_time = 5 * 60
            self.long_break_time = 5 * 60

    def show_home(self):
        self.home_frame.pack(fill="both", expand=True)
        self.settings_frame.pack_forget()
        self.stats_frame.pack_forget()

    def show_settings(self):
        self.home_frame.pack_forget()
        self.settings_frame.pack(fill="both", expand=True)
        self.stats_frame.pack_forget()

    def show_stats(self):
        self.home_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.stats_frame.pack(fill="both", expand=True)
        self.plot_stats()

    def save_settings(self):
        self.work_time = int(self.work_entry.get()) * 60
        self.short_break_time = int(self.short_break_entry.get()) * 60
        self.long_break_time = int(self.long_break_entry.get()) * 60
        messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.update_timer()

    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                if self.work_time > 0:
                    self.work_time -= 1
                    self.update_time_label(self.work_time)
                    self.time_spent_working += 1
                else:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.work_time = WORK_TIME
                    if self.pomodoros_completed % 4 == 0:
                        self.break_time = LONG_BREAK_TIME
                    else:
                        self.break_time = SHORT_BREAK_TIME
            else:
                if self.break_time > 0:
                    self.break_time -= 1
                    self.update_time_label(self.break_time)
                    self.time_spent_breaking += 1
                else:
                    self.is_work_time = True
                    self.break_time = 0

            self.root.after(1000, self.update_timer)

    def update_time_label(self, remaining_time):
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))

    def plot_stats(self):
        # Ensure the pie chart reflects the latest time spent
        labels = ['Work', 'Break']
        sizes = [self.time_spent_working, self.time_spent_breaking]
        colors = ['#ff9999','#66b3ff']
        explode = (0.1, 0)  # explode the 1st slice (i.e. 'Work')

        print(f"Plotting stats: {sizes}")

        # Check if sizes contain valid values
        if all(size >= 0 for size in sizes) and any(size > 0 for size in sizes):
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Update the canvas with the new pie chart
            if hasattr(self, 'canvas'):
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig1, master=self.stats_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()

    def stats_frame_widgets(self):
        self.plot_stats()

if __name__ == "__main__":
    PomodoroTimer().root.mainloop()
