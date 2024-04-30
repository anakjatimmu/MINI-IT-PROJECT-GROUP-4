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

        # TIMER LABEL
        minutes, seconds = divmod(WORK_TIME, 60)
        self.timer_label = tk.Label(self.root, text="{:02d}:{:02d}".format(minutes, seconds), font=("TkDefaultFont", 40))
        self.timer_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        # START BUTTON
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer,width = 10)
        self.start_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        # EDIT BUTTON 
        self.edit_button = ttk.Button(self.root, text="Edit", command=self.edit_timer, width = 10)
        self.edit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.work_time, self.break_time = WORK_TIME, SHORT_BREAK_TIME
        self.is_work_time, self.pomodoros_completed, self.is_running = True, 0, False

        self.root.mainloop()

    def start_timer(self):
        self.start_button.config(state=tk.DISABLED)
        self.edit_button.config(text="Stop", command=self.stop_timer)
        self.is_running = True
        self.update_timer()
    
    def stop_timer(self):
        if messagebox.askyesno("Pomodoro Timer","Are you sure you want to give up"):
            self.start_button.config(state=tk.NORMAL)
            self.edit_button.config(text="Edit", command=self.edit_timer)
            self.is_running = False
            
            self.work_time, self.break_time = WORK_TIME, SHORT_BREAK_TIME
            self.is_work_time, self.pomodoros_completed = True, 0
            minutes, seconds = divmod(self.work_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))

    def edit_timer(self):
        # Add your edit functionality here
        pass

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
