import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style, PhotoImage

# Set the default time for work and break intervals
WORK_TIME = 1 * 60
SHORT_BREAK_TIME = 1 *60
LONG_BREAK_TIME = 1 *60




class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("200x200")
        self.root.title("Pomodoro Timer")
        self.style = Style(theme="simplex")
        self.style.theme_use()

        self.work_time = WORK_TIME
        self.short_break_time = SHORT_BREAK_TIME
        self.long_break_time = LONG_BREAK_TIME
        self.is_work_time = True
        self.pomodoros_completed = 0
        self.is_running = False


        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(pady=10)

        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.pack_forget()

        self.home_frame = ttk.Frame(self.main_frame)
        self.home_frame.pack(fill="both", expand=True)

        self.load_icons()
        self.create_widgets()

    def create_widgets(self):
        self.nav_frame_widgets()
        self.home_frame_widgets()
        self.settings_frame_widget()
    
    def load_icons(self):
        icon_paths = {
            "timer_icon":"timer_icon.png"
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
    
    def home_frame_widgets(self):

        self.timer_minutes = WORK_TIME // 60 
        self.timer_seconds = WORK_TIME % 60
        self.timer_label = tk.Label(self.home_frame, text="{:02d}:{:02d}".format(self.timer_minutes,self.timer_seconds), font=("TkDefaultFont", 40))
        self.timer_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.start_button = ttk.Button(self.home_frame, text="Start", command=self.start_timer,width = 10)
        self.start_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.is_work_time, self.pomodoros_completed, self.is_running = True, 0, False

    def settings_frame_widget(self):

        self.settings_subtitle_label = ttk.Label(self.settings_frame, text="Timer", font=("TkDefaultFont", 18,"bold"))
        self.settings_subtitle_label.place(relx=0.5, rely=0.05,anchor=tk.CENTER)

        timer_icon = self.icons["timer_icon"]
        self.settings_icon_label = ttk.Label(self.settings_frame,image=timer_icon)
        self.settings_icon_label.place(relx=0.46, rely=0.049, anchor = tk.CENTER)

        self.work_label = ttk.Label(self.settings_frame, text="Work Time (minutes):", font=("TKDefaultFont",10))
        self.work_label.place(relx=0.5, rely=0.11,anchor=tk.CENTER)
        self.work_entry = ttk.Entry(self.settings_frame)
        self.work_entry.insert(0, str(WORK_TIME//60))
        self.work_entry.place(relx=0.5, rely=0.15,anchor=tk.CENTER)

        self.short_break_label = ttk.Label (self.settings_frame, text="Short Break Time (minutes):",font=("TKDefaultFont",10))
        self.short_break_label.place(relx=0.5, rely=0.21,anchor=tk.CENTER)
        self.short_break_entry = ttk.Entry(self.settings_frame)
        self.short_break_entry.insert(0, str(SHORT_BREAK_TIME // 60))
        self.short_break_entry.place(relx=0.5, rely=0.25,anchor=tk.CENTER)

        self.long_break_label = ttk.Label(self.settings_frame, text="Long Break Time (minutes):",font=("TKDefaultFont",10))
        self.long_break_label.place(relx=0.5, rely=0.31,anchor=tk.CENTER)
        self.long_break_entry = ttk.Entry(self.settings_frame)
        self.long_break_entry.insert(0, str(LONG_BREAK_TIME // 60))
        self.long_break_entry.place(relx=0.5, rely=0.35,anchor=tk.CENTER)

        self.save_button = ttk.Button(self.settings_frame, text="Save", command=self.save_settings)
        self.save_button.place(relx=0.5, rely=0.4,anchor=tk.CENTER)

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

        self.work_time = int(self.work_entry.get()) * 60
        self.short_break_time = int(self.short_break_entry.get()) * 60
        self.long_break_time = int(self.long_break_entry.get()) * 60 
        
        self.is_work_time = True
        self.pomodoros_completed = 0

        self.timer_minutes = self.work_time // 60
        self.timer_seconds = self.work_time % 60
        self.timer_label.config(text="{:02d}:{:02d}".format(self.timer_minutes, self.timer_seconds))
        messagebox.showinfo("Settings Saved", "Timer settings updated successfully!")

    def start_timer(self):
        self.start_button.config(text="Stop", command=self.stop_timer)
        self.is_running = True
        self.update_timer()
    
    def stop_timer(self):
        if messagebox.askyesno("Pomodoro Timer","Are you sure you want to give up"):
            self.start_button.config(state=tk.NORMAL,text="Start", command=self.start_timer)
            self.is_running = False
            
            self.work_time = int(self.work_entry.get())*60 
            self.short_break_time = int(self.short_break_entry.get())*60
            self.long_break_time = int(self.long_break_entry.get()) * 60
            self.is_work_time, self.pomodoros_completed = True, 0

            self.work_entry.delete(0, tk.END)
            self.work_entry.insert(0, str(self.work_time // 60))

            self.short_break_entry.delete(0, tk.END)
            self.short_break_entry.insert(0, str(self.short_break_time // 60))

            self.long_break_entry.delete(0, tk.END)
            self.long_break_entry.insert(0, str(self.long_break_time // 60))
            minutes, seconds = divmod(self.work_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))


    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.break_time = self.long_break_time if self.pomodoros_completed % 4 == 0 else self.short_break_time
                    messagebox.showinfo("Great job!" if self.pomodoros_completed % 4 == 0
                                        else "Good job!", "Take a long break and rest your mind."
                                        if self.pomodoros_completed % 4 == 0
                                        else "Take a short break and stretch your legs!")  
            else:
                self.break_time -= 1
                if self.break_time == 0:
                    self.is_work_time = True
                    if int(self.work_entry.get()) * 60 != WORK_TIME:
                        self.work_time = int(self.work_entry.get()) * 60
                    else:
                        self.work_time = WORK_TIME 
                    messagebox.showinfo("Work Time", "Get back to work!")        
            minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.root.after(1000, self.update_timer)
           
    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    pomodoro_timer = PomodoroTimer()
    pomodoro_timer.run()
