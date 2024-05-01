import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

# Set the default time for work and break intervals
WORK_TIME = 1 * 60
SHORT_BREAK_TIME = 1 * 60
LONG_BREAK_TIME = 1 * 60


class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("200x200")
        self.root.title("Pomodoro Timer")
        self.style = Style(theme="simplex")
        self.style.theme_use()

        #*******NAVIGATION PART OI*******
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(pady=10)

        # HOME BUTTON/FRAME
        self.home_frame = ttk.Frame(self.main_frame)
        self.home_frame.pack(fill="both", expand=True)

        self.home_button = ttk.Button(self.nav_frame, text="Home", width=10, command=self.show_home)
        self.home_button.grid(row=0, column=0, padx=10)

        # SETTINGS BUTTON/FRAME
        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.pack_forget()

        self.settings_button = ttk.Button(self.nav_frame, text="Settings", width=10, command=self.show_settings)
        self.settings_button.grid(row=0, column=1, padx=10)

        # TIMER LABEL
        minutes, seconds = divmod(WORK_TIME, 60)
        self.timer_label = tk.Label(self.home_frame, text="{:02d}:{:02d}".format(minutes, seconds), font=("TkDefaultFont", 40))
        self.timer_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        # START BUTTON
        self.start_button = ttk.Button(self.home_frame, text="Start", command=self.start_timer,width = 10)
        self.start_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.work_time, self.break_time = WORK_TIME, SHORT_BREAK_TIME
        self.is_work_time, self.pomodoros_completed, self.is_running = True, 0, False
        #Settings test
        self.save_button = ttk.Button(self.settings_frame, text="Test",command=self.save_settings)
        self.save_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.root.mainloop()

    def show_home(self):
        self.home_frame.pack(fill="both", expand=True)
        if self.settings_frame.winfo_exists():
            self.settings_frame.pack_forget()
        else:
            pass
    
    def show_settings(self):
        self.settings_frame.pack(fill="both",expand=True)
        
        if self.home_frame.winfo_exists():
            self.home_frame.pack_forget()
        else:
            pass

    def save_settings(self):
        # Add your save settings functionality here
        pass

    def start_timer(self):
        self.start_button.config(text="Stop", command=self.stop_timer)
        self.is_running = True
        self.update_timer()
    
    def stop_timer(self):
        if messagebox.askyesno("Pomodoro Timer","Are you sure you want to give up"):
            self.start_button.config(state=tk.NORMAL,text="Start", command=self.start_timer)
            self.is_running = False
            
            self.work_time, self.break_time = WORK_TIME, SHORT_BREAK_TIME
            self.is_work_time, self.pomodoros_completed = True, 0
            minutes, seconds = divmod(self.work_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))


    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.break_time = LONG_BREAK_TIME if self.pomodoros_completed % 4 == 0 else SHORT_BREAK_TIME
                    messagebox.showinfo("Great job!" if self.pomodoros_completed % 4 == 0
                                        else "Good job!", "Take a long break and rest your mind."
                                        if self.pomodoros_completed % 4 == 0
                                        else "Take a short break and stretch your legs!")
            else:
                self.break_time -= 1
                if self.break_time == 0:
                    self.is_work_time, self.work_time = True, WORK_TIME
                    messagebox.showinfo("Work Time", "Get back to work!")        
            minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.root.after(1000, self.update_timer)
PomodoroTimer()
