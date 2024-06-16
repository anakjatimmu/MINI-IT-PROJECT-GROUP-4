import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style, PhotoImage, ttk
from PIL import Image, ImageTk
from database import save_profile, get_profiles, update_profile, initialize_db,delete_profile, save_task, delete_task, get_tasks,update_task


WORK_TIME = 1 * 60
SHORT_BREAK_TIME = 1 *60
LONG_BREAK_TIME = 1 *60

class PomodoroTimer:
    def __init__(self):
        initialize_db()
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
        self.username = ""


        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(pady=10)

        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.configure(style='Custom.TFrame')
        self.settings_frame.pack_forget()

        self.home_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.home_frame.pack(fill="both", expand=True)
        self.home_frame.config(style='Custom.TFrame')

        self.task_frame = ttk.Frame(self.main_frame)
        self.task_frame.config(style='Custom.TFrame')
        self.task_frame.pack_forget()

        self.achievement_frame = ttk.Frame(self.main_frame)
        self.achievement_frame.config(style='Custom.TFrame')
        self.achievement_frame.pack_forget()

        self.style.configure('Custom.TFrame', background='#BA4949')

        self.style.configure('TLabel', background = '#BA4949', foreground ='white')

        self.style.configure('TButton', 
                             foreground='#BA4949', 
                             background='white',
                             font =('TkDfaultFont',10,'bold'),
                             padding = 10,
                             borderwidth = 0)
        self.style.map('TButton',
               foregroun=[('!active', '#BA4949'), ('active', '#BA4949')],
               background=[('!active', 'white'), ('active', 'white')])


        self.load_icons()
        self.create_widgets()

    def create_widgets(self):
        self.settings_frame_widget()
        self.nav_frame_widgets()
        self.home_frame_widgets()
        self.task_frame_widgets()
        self.achievement_frame_widgets()
    
    def load_icons(self):
        icon_paths = {
            "timer_icon":"timer_icon.png",
            "preadded_icon":"preadded.png",
            }
        self.icons = {}
        for name, path in icon_paths.items():
            icon_image = PhotoImage(file="")
            resize_icon = icon_image.subsample(8)
            self.icons[name] = resize_icon

    def nav_frame_widgets(self):
        self.home_button = ttk.Button(self.nav_frame, text="Home", width=10, command=self.show_home)
        self.home_button.grid(row=0, column=0, padx=10)

        self.settings_button = ttk.Button(self.nav_frame, text="Settings", width=10, command=self.show_settings)
        self.settings_button.grid(row=0, column=1, padx=10)

        self.task_button = ttk.Button(self.nav_frame, text="Task", width=10, command=self.show_task)
        self.task_button.grid(row=0, column=2, padx=10)

        self.achievement_button = ttk.Button(self.nav_frame, text="Achievement", width=12, command=self.show_achievement)
        self.achievement_button.grid(row=0, column=3, padx=10)
    def home_frame_widgets(self):

        self.status_label = ttk.Label(self.home_frame, text="", font=("TkDefaultFont", 14))
        self.status_label.place(relx=0.5, rely=0.32, anchor=tk.CENTER)

        self.timer_minutes = WORK_TIME // 60 
        self.timer_seconds = WORK_TIME % 60
        self.timer_label = ttk.Label(self.home_frame, text="{:02d}:{:02d}".format(self.timer_minutes,self.timer_seconds), font=("TkDefaultFont",60))
        self.timer_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.start_button = ttk.Button(self.home_frame, text="Start", command=self.start_timer,width = 15)
        self.start_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.is_work_time, self.pomodoros_completed, self.is_running = True, 0, False

        #**** PREADDED LABEL/ICON ****
        self.preadded_timers_label = ttk.Label(self.home_frame, text="Preset Timers",font=("TkDefaulFont",18,"bold"))
        self.preadded_timers_label.place(relx=0.85, rely=0.15, anchor=tk.CENTER)

        #preadded_icon = self.icons["preadded_icon"]
        self.settings_icon_label = ttk.Label(self.home_frame,image="")
        self.settings_icon_label.place(relx=0.78, rely=0.15, anchor = tk.CENTER)

        self.preadded_timers_listbox = tk.Listbox(self.home_frame)
        self.preadded_timers_listbox.configure(background='#C76D6D',
                                                   height=5,width=40,
                                                   fg='white',
                                                   font=('Arial',12), bd=2,
                                                   selectbackground='white',selectforeground='#C76D6D',
                                                   highlightthickness=0)
            
        self.preadded_timers_listbox.insert(1, "    Deep Work Session")
        self.preadded_timers_listbox.insert(2, "    Light Work Session")
        self.preadded_timers_listbox.insert(3, "    Exercise Session")
        self.preadded_timers_listbox.insert(4, "    Meditation Session")
        self.preadded_timers_listbox.place(relx=0.85, rely=0.25, anchor=tk.CENTER)

        self.timer_descriptions = {
        "Deep Work Session": "1 hour of focused work followed by a 15-minute break.",
        "Light Work Session": "45 minutes of work followed by a 5-minute break.",
        "Exercise Session": "1-minute work intervals with 15-second breaks for exercise.",
        "Meditation Session": "15 minutes of meditation followed by 5 minutes of stretching."
        }

        self.timer_description_label = ttk.Label(self.home_frame, text="", font=("TkDefaultFont", 12), wraplength=500)
        self.timer_description_label.place(relx=0.85, rely=0.335, anchor=tk.CENTER)
        
        self.add_timer_button = ttk.Button(self.home_frame, text="Try Out!", command=self.add_selected_timer)
        self.add_timer_button.place(relx=0.85,rely=0.38, anchor=tk.CENTER)
        self.preadded_timers_listbox.bind("<<ListboxSelect>>", self.update_description_label)

        self.load_profiles_label = ttk.Label(self.home_frame, text="Saved Timers", font=("TkDefaultFont", 18, "bold"))
        self.load_profiles_label.place(relx=0.85, rely=0.45, anchor=tk.CENTER)

        self.home_profile_listbox = tk.Listbox(self.home_frame)
        self.home_profile_listbox.place(relx=0.85, rely=0.55, anchor=tk.CENTER)
        self.home_profile_listbox.configure(background='#C76D6D',
                                                   height=5,width=40,
                                                   fg='white',
                                                   font=('Arial',12), bd=2,
                                                   selectbackground='white',selectforeground='#C76D6D',
                                                   highlightthickness=0)
        

        self.load_profiles_home()

        self.load_profile_button = ttk.Button(self.home_frame, text="Load Timer", command=self.load_selected_profile)
        self.load_profile_button.place(relx=0.85, rely=0.7, anchor=tk.CENTER)

        self.listbox_missions = tk.Listbox(self.home_frame, height=10, width=30, font=("TkDefaultFont", 12))
        self.listbox_missions.configure(background='#C76D6D',
                                                   height=5,width=40,
                                                   fg='white',
                                                   font=('Arial',12), bd=2,
                                                   selectbackground='white',selectforeground='#C76D6D',
                                                   highlightthickness=0)

        self.missions = ["Complete 1 Pomodoro session", "Complete 3 pomodoro session","Use this app for 3 day a row","Use this app for 1 week a row",
                         "Use this app for 12 hours straight", "Use this app for 24 hours straight", "Complete 10 pomodoro sessions a day", "Use this app for 96 hours straight",
                         "Use this app for 365 day a row ", "Use this app for 8760 hours straight"]
        self.listbox_missions = []
        self.reward_buttons = []

        for idx, mission in enumerate(self.missions):
            listbox_missions = tk.Listbox(self.home_frame, height=2, width=47, font=("TkDefaultFont", 12))
            listbox_missions.insert(tk.END, mission)
            listbox_missions.place(relx=0.2, rely=0.25 + idx * 0.055, anchor=tk.CENTER)
            self.listbox_missions.append(listbox_missions)

            reward_button = ttk.Button(self.home_frame, text="Claim Reward", command=lambda idx=idx: self.claim_reward(idx), state=tk.DISABLED)
            reward_button.place(relx=0.3, rely=0.246 + idx * 0.055555, anchor=tk.CENTER)
            self.reward_buttons.append(reward_button)

    def achievement_frame_widgets(self):
        self.achievement_label = ttk.Label(self.achievement_frame, text="Achievement", font=("TkDefaultFont", 20, "bold"))
        self.achievement_label.place(relx=0.5, rely=0.02, anchor=tk.CENTER)

        # Lock/Unlock image functionality in task page
        self.lock_image_path = "lock.png"
        self.unlock_image_path = "badge 1.png"

        # Load and resize lock image
        self.lock_image = Image.open(self.lock_image_path)
        self.lock_image.thumbnail((100, 100))  # Resize lock image to 100x100 pixels
        self.lock_photo = ImageTk.PhotoImage(self.lock_image)

        # Load and resize unlock image
        self.unlock_image = Image.open(self.unlock_image_path)
        self.unlock_image.thumbnail((100, 100))  # Resize unlock image to 100x100 pixels
        self.unlock_photo = ImageTk.PhotoImage(self.unlock_image)

        self.is_locked = True

        # Image label for lock image
        self.image_label = tk.Label(self.achievement_frame, image=self.lock_photo)
        self.image_label.pack(pady=20)

        self.toggle_button = ttk.Button(self.achievement_frame, text="Unlock", command=self.toggle_lock, width=10, state=tk.DISABLED)
        self.toggle_button.pack(pady=10)
 
    
    def task_frame_widgets(self):

        self.task_label = ttk.Label(self.task_frame, text="Task", font=("TkDefaultFont", 20, "bold"))
        self.task_label.place(relx=0.5, rely=0.08, anchor=tk.CENTER)

        self.task_description_label = ttk.Label(self.task_frame, text="Create a task for future needs", font=("TkDefaultFont", 12, ))
        self.task_description_label.place(relx=0.5, rely=0.13, anchor=tk.CENTER)

        self.task_name_label = ttk.Label(self.task_frame, text="Task Name :", font=("TkDefaultFont",12))
        self.task_name_label.place(relx=0.4, rely=0.2, anchor=tk.CENTER)
        self.task_entry = tk.Entry(self.task_frame, width=50)
        self.task_entry.place(relx=0.55, rely=0.2, anchor=tk.CENTER)

        self.work_task_label = ttk.Label(self.task_frame, text="Work Time (mins) :", font=("TKDefaultFont",12))
        self.work_task_label.place(relx=0.43, rely=0.25,anchor=tk.CENTER)
        self.work_task_entry = ttk.Entry(self.task_frame)
        self.work_task_entry.insert(0, str(WORK_TIME//60))
        self.work_task_entry.place(relx=0.55, rely=0.25,anchor=tk.CENTER)

        

        self.short_break_task_label = ttk.Label (self.task_frame, text="Short Break Time (mins) :",font=("TKDefaultFont",12))
        self.short_break_task_label.place(relx=0.43, rely=0.32,anchor=tk.CENTER)
        self.short_break_task_entry = ttk.Entry(self.task_frame)
        self.short_break_task_entry.insert(0, str(SHORT_BREAK_TIME // 60))
        self.short_break_task_entry.place(relx=0.55, rely=0.32,anchor=tk.CENTER)
        
        self.long_break_task_label = ttk.Label(self.task_frame, text="Long Break Time (mins) :",font=("TKDefaultFont",12))
        self.long_break_task_label.place(relx=0.43, rely=0.39,anchor=tk.CENTER)
        self.long_break_task_entry = ttk.Entry(self.task_frame)
        self.long_break_task_entry.insert(0, str(LONG_BREAK_TIME // 60))
        self.long_break_task_entry.place(relx=0.55, rely=0.39,anchor=tk.CENTER)

        self.add_task_button = ttk.Button(self.task_frame, text="Add Task", command=self.add_task)
        self.add_task_button.place(relx=0.5, rely=0.5,anchor=tk.CENTER)

        self.task_label = ttk.Label(self.task_frame, text="Saved Task", font=("TkDefaultFont", 20, "bold"))
        self.task_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.task_listbox = tk.Listbox(self.task_frame)
        self.task_listbox.configure(background='#C76D6D',
                                                   height= 6, width=50,
                                                   fg='white',
                                                   font=('Arial',12), bd=2,
                                                   selectbackground='white',selectforeground='#C76D6D',
                                                   highlightthickness=0)
        self.task_listbox.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        self.load_tasks()

        self.remove_task_button = ttk.Button(self.task_frame, text="Remove Task", command=self.delete_task)
        self.remove_task_button.place(relx=0.45, rely=0.9, anchor=tk.CENTER)
        
        self.edit_button = ttk.Button(self.task_frame, text="Edit Task Timer", command=self.edit_task_timer)
        self.edit_button.place(relx=0.55, rely=0.9, anchor = tk.CENTER)


    def settings_frame_widget(self):

        # Timer LABEL/ICON
        self.settings_subtitle_label = ttk.Label(self.settings_frame, text="Timer", font=("TkDefaultFont", 18,"bold"))
        self.settings_subtitle_label.place(relx=0.5, rely=0.05,anchor=tk.CENTER)
        self.settings_subtitle_label = ttk.Label(self.settings_frame, text="Save your own customize timer!", font=("TkDefaultFont", 10,"bold"))
        self.settings_subtitle_label.place(relx=0.5, rely=0.095,anchor=tk.CENTER)

        timer_icon = self.icons["timer_icon"]
        self.settings_icon_label = ttk.Label(self.settings_frame,image=timer_icon)
        self.settings_icon_label.place(relx=0.46, rely=0.049, anchor = tk.CENTER)

        # Timer Entriessss
        self.work_label = ttk.Label(self.settings_frame, text="Work Time (mins) :", font=("TKDefaultFont",12))
        self.work_label.place(relx=0.43, rely=0.15,anchor=tk.CENTER)
        self.work_entry = ttk.Entry(self.settings_frame)
        self.work_entry.insert(0, str(WORK_TIME//60))
        self.work_entry.place(relx=0.55, rely=0.15,anchor=tk.CENTER)

        

        self.short_break_label = ttk.Label (self.settings_frame, text="Short Break Time (mins) :",font=("TKDefaultFont",12))
        self.short_break_label.place(relx=0.43, rely=0.22,anchor=tk.CENTER)
        self.short_break_entry = ttk.Entry(self.settings_frame)
        self.short_break_entry.insert(0, str(SHORT_BREAK_TIME // 60))
        self.short_break_entry.place(relx=0.55, rely=0.22,anchor=tk.CENTER)
        
        self.long_break_label = ttk.Label(self.settings_frame, text="Long Break Time (mins) :",font=("TKDefaultFont",12))
        self.long_break_label.place(relx=0.43, rely=0.29,anchor=tk.CENTER)
        self.long_break_entry = ttk.Entry(self.settings_frame)
        self.long_break_entry.insert(0, str(LONG_BREAK_TIME // 60))
        self.long_break_entry.place(relx=0.55, rely=0.29,anchor=tk.CENTER)

        self.save_button = ttk.Button(self.settings_frame, text="Save To Timer", command=self.save_settings)
        self.save_button.place(relx=0.45, rely=0.45,anchor=tk.CENTER)

        self.save_button = ttk.Button(self.settings_frame, text="Save To Profile", command=self.save_profile)
        self.save_button.place(relx=0.55, rely=0.45,anchor=tk.CENTER)


        # Profilee
        self.profile_label = ttk.Label(self.settings_frame, text="Profile Name :", font=("TKDefaultFont", 11))
        self.profile_label.place(relx=0.45, rely=0.36, anchor=tk.CENTER)
        self.profile_entry = ttk.Entry(self.settings_frame)
        self.profile_entry.place(relx=0.55, rely=0.36, anchor=tk.CENTER)


        # Load Profile abangku
        self.load_profiles_label = ttk.Label(self.settings_frame, text="Saved Timers", font=("TkDefaultFont", 18, "bold"))
        self.load_profiles_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.settings_profile_listbox = tk.Listbox(self.settings_frame)
        self.settings_profile_listbox.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
        self.settings_profile_listbox.configure(background='#C76D6D',
                                                   height=5,width=40,
                                                   fg='white',
                                                   font=('Arial',12), bd=2,
                                                   selectbackground='white',selectforeground='#C76D6D',
                                                   highlightthickness=0)
        self.settings_profile_listbox.bind("<<ListboxSelect>>", self.profile_selected)
        self.load_profiles_settings()

        self.edit_profile_button = ttk.Button(self.settings_frame, text="Edit Profiles", command=self.edit_profile)
        self.edit_profile_button.place(relx=0.55, rely=0.77, anchor=tk.CENTER)
        self.edit_profile_button.config(state=tk.DISABLED)


        # Delete profile
        self.delete_profile_button = ttk.Button(self.settings_frame, text="Delete Profile", command=self.delete_profile)
        self.delete_profile_button.place(relx=0.45, rely=0.77, anchor=tk.CENTER)
        self.delete_profile_button.config(state=tk.DISABLED)
    def profile_selected(self, event):
        self.edit_profile_button.config(state=tk.NORMAL)
        self.delete_profile_button.config(state=tk.NORMAL)
    def edit_profile(self):
        selected_profile_name = self.settings_profile_listbox.get(self.settings_profile_listbox.curselection())

        if selected_profile_name:
            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title("Edit Profile")
            self.edit_window.configure(background='#BA4949')

            window_width, window_height = 300, 350
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            position_top = int(screen_height / 2 - window_height / 2)
            position_right = int(screen_width / 2 - window_width / 2)

            self.edit_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

            try:
                ttk.Label(self.edit_window, text="Work Time (minutes):").pack(pady=5)
                self.work_time_entry = tk.Entry(self.edit_window)

                self.work_time_entry.pack(pady=5)

                ttk.Label(self.edit_window, text="Short Break Time (minutes):").pack(pady=5)
                self.short_break_time_entry = tk.Entry(self.edit_window)
                self.short_break_time_entry.pack(pady=5)

                ttk.Label(self.edit_window, text="Long Break Time (minutes):").pack(pady=5)
                self.long_break_time_entry = tk.Entry(self.edit_window)
                self.long_break_time_entry.pack(pady=5)

                ttk.Label(self.edit_window, text="Profile Name:").pack(pady=5)
                self.profile_name_entry = tk.Entry(self.edit_window)
                self.profile_name_entry.pack(pady=5)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

            ttk.Button(self.edit_window, text="Save Changes", command=lambda: self.save_edits(selected_profile_name)).pack(pady=10)
        else:
            messagebox.showwarning("No Profile Selected", "Please select a profile to edit.")

    def save_edits(self, selected_profile_name):
        new_profile_name = self.profile_name_entry.get()
        work_time_entry = self.work_time_entry.get()
        short_break_time_entry = self.short_break_time_entry.get()
        long_break_time_entry = self.long_break_time_entry.get()

        if not new_profile_name or not work_time_entry or not short_break_time_entry or not long_break_time_entry:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        work_time = int(work_time_entry) * 60
        short_break_time = int(short_break_time_entry) * 60
        long_break_time = int(long_break_time_entry) * 60
        
        if new_profile_name and work_time and short_break_time and long_break_time:
            update_profile(new_profile_name, work_time, short_break_time, long_break_time, selected_profile_name)
            self.load_profiles_home()
            self.load_profiles_settings()
            self.edit_window.destroy()
            messagebox.showinfo("Profile Updated", f"Profile '{new_profile_name}' has been updated.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def delete_profile(self):
        selected_profile = self.settings_profile_listbox.get(tk.ACTIVE)
        if selected_profile:
            confirmation = messagebox.askyesno("Delete Profile", f"Are you sure you want to delete the profile '{selected_profile}'?")
            if confirmation:
                delete_profile(selected_profile)
                self.load_profiles_home() 
                self.load_profiles_settings() 
                messagebox.showinfo("Profile Deleted", f"Profile '{selected_profile}' has been deleted.")
        else:
            messagebox.showwarning("No Profile Selected", "Please select a profile to delete.")
    
    def load_profiles_settings(self):
        self.settings_profile_listbox.delete(0, tk.END)
        profiles = get_profiles()
        for profile in profiles:
            self.settings_profile_listbox.insert(tk.END, profile[0])

    def load_profiles_home(self):
        self.home_profile_listbox.delete(0, tk.END)
        profiles = get_profiles()
        for profile in profiles:
            self.home_profile_listbox.insert(tk.END, profile[0])

    def load_selected_profile(self):
        selection = self.home_profile_listbox.curselection()
        if selection:
            selected_profile_name = self.home_profile_listbox.get(selection)
            profiles = get_profiles()
            for profile in profiles:
                if profile[0] == selected_profile_name:
                    self.username = profile[0]
                    self.work_time = profile[1]
                    self.short_break_time = profile[2]
                    self.long_break_time = profile[3]
                    self.update_timer_label()

                    self.work_entry.delete(0, tk.END)
                    self.work_entry.insert(0, str(self.work_time // 60))

                    self.short_break_entry.delete(0, tk.END)
                    self.short_break_entry.insert(0, str(self.short_break_time // 60))

                    self.long_break_entry.delete(0, tk.END)
                    self.long_break_entry.insert(0, str(self.long_break_time // 60))

                    self.profile_entry.delete(0, tk.END)
                    self.profile_entry.insert(0, self.username)
                    self.load_profiles_home()  
                    messagebox.showinfo("Timer loaded", "Timer has been loaded")
                    return
            messagebox.showerror("Error", "Profile not found.")
        else:
            messagebox.showerror("Error", "Please select a profile.")
        
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
        
        self.work_entry.delete(0, tk.END)
        self.work_entry.insert(0, str(self.work_time // 60))

        self.short_break_entry.delete(0, tk.END)
        self.short_break_entry.insert(0, str(self.short_break_time // 60))

        self.long_break_entry.delete(0, tk.END)
        self.long_break_entry.insert(0, str(self.long_break_time // 60))
        
        
        self.timer_minutes = self.work_time // 60
        self.timer_seconds = self.work_time % 60
        self.timer_label.config(text="{:02d}:{:02d}".format(self.timer_minutes, self.timer_seconds))
        messagebox.showinfo("Timer Added", f"{selected_timer} added to settings!")

    def show_home(self):
        self.home_frame.pack(fill="both", expand=True)
        if self.settings_frame.winfo_exists():
            self.settings_frame.pack_forget()
        if self.task_frame.winfo_exists():
            self.task_frame.pack_forget()
        if self.achievement_frame.winfo_exists():
            self.achievement_frame.pack_forget()
        else:
            pass
          
    
    def show_settings(self):
        self.settings_frame.pack(fill="both",expand=True)
        
        if self.home_frame.winfo_exists():
            self.home_frame.pack_forget()
        if self.task_frame.winfo_exists():
            self.task_frame.pack_forget()
        if self.achievement_frame.winfo_exists():
            self.achievement_frame.pack_forget()
        else:
            pass

    
    def show_task(self):
        self.task_frame.pack(fill="both", expand=True)
        if self.home_frame.winfo_exists():
            self.home_frame.pack_forget()
        if self.settings_frame.winfo_exists():
            self.settings_frame.pack_forget()
        if self.achievement_frame.winfo_exists():
            self.achievement_frame.pack_forget()

    def show_achievement(self):
        self.achievement_frame.pack(fill="both", expand=True)
        if self.home_frame.winfo_exists():
            self.home_frame.pack_forget()
        if self.settings_frame.winfo_exists():
            self.settings_frame.pack_forget()
        if self.task_frame.winfo_exists():
            self.task_frame.pack_forget()

    def save_settings(self):
        try:
            self.work_time = int(self.work_entry.get()) * 60
            self.short_break_time = int(self.short_break_entry.get()) * 60
            self.long_break_time = int(self.long_break_entry.get()) * 60 

            self.is_work_time = True
            self.pomodoros_completed = 0

            
            self.timer_minutes = self.work_time // 60
            self.timer_seconds = self.work_time % 60
            self.timer_label.config(text="{:02d}:{:02d}".format(self.timer_minutes, self.timer_seconds))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
        messagebox.showinfo("Timer Saved", "Timer Saved Succesfully! ")
    def save_profile(self):
        profile_name = self.profile_entry.get().strip()
        if profile_name:
            self.username = profile_name

            self.work_time = int(self.work_entry.get()) * 60
            self.short_break_time = int(self.short_break_entry.get()) * 60
            self.long_break_time = int(self.long_break_entry.get()) * 60
            self.profile_entry.delete(0, tk.END)
            
            self.profile_entry.insert(0, self.username)

           
            existing_profiles = [profile[0] for profile in get_profiles()]
            if profile_name in existing_profiles:
                update_profile(profile_name, self.work_time, self.short_break_time, self.long_break_time)
            else:
                save_profile(profile_name, self.work_time, self.short_break_time, self.long_break_time)
            self.load_profiles_home()
            self.load_profiles_settings()

        else:
            messagebox.showerror("Error", "Please enter a profile name.")
            return

        messagebox.showinfo("Settings Saved", "Timer settings updated successfully!")
    def update_timer_label(self):
        self.timer_minutes = self.work_time // 60
        self.timer_seconds = self.work_time % 60
        self.timer_label.config(text="{:02d}:{:02d}".format(self.timer_minutes, self.timer_seconds))

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
            self.status_label.config(text="",background="")

    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                   self.is_work_time = False
                   self.pomodoros_completed += 1
                   self.check_task_completion()  # Check if any task is completed
                   self.break_time = self.long_break_time if self.pomodoros_completed % 4 == 0 else self.short_break_time
                   messagebox.showinfo("Great job!" if self.pomodoros_completed == 5
                                    else "Good job!", "Take a long break and rest your mind."
                                    if self.pomodoros_completed % 4 == 0
                                    else "Take a short break and stretch your legs!")
                self.status_label.config(text="   Work Time   ", foreground='white', background='#6F2B2B')
            else:
            self.break_time -= 1
            if self.break_time == 0:
                self.is_work_time = True
                if int(self.work_entry.get()) * 60 != WORK_TIME:
                    self.work_time = int(self.work_entry.get()) * 60
                else:
                    self.work_time = WORK_TIME
                messagebox.showinfo("Work Time", "Get back to work!")
            self.status_label.config(text="   Break Time   " if self.pomodoros_completed % 4 != 0 else "   Long Break   ", foreground='white', background='#6F2B2B')
        
        minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
        self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
        self.root.after(1000, self.update_timer)


    
    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = get_tasks()
        for task in tasks:
            self.task_listbox.insert(tk.END, task[0]) 

    def add_task(self):
        task = self.task_entry.get()
        work_time = int(self.work_task_entry.get()) * 60
        short_break_time = int(self.short_break_task_entry.get()) * 60
        long_break_time = int(self.long_break_task_entry.get()) * 60
        save_task(task, work_time, short_break_time, long_break_time)
        messagebox.showinfo("Success", "Task saved successfully!")
        self.load_tasks()
    def delete_task(self):
        try:
            task_id = self.task_listbox.curselection()[0]
            task_name = self.task_listbox.get(tk.ACTIVE)
            confirmation = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
            if confirmation:
                delete_task(task_id, task_name)
                messagebox.showinfo("Task Deleted", "The task has been deleted successfully.")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
        self.load_tasks()  


    def edit_task_timer(self):
        if not self.task_listbox.curselection():
            messagebox.showwarning("Warning", "Please select a task to edit!")
            return
        task_id = self.task_listbox.curselection()[0]
        task_name = self.task_listbox.get(task_id)
        tasks = get_tasks()
        for task in tasks:
            if task[0] == task_name:
                work_time = task[1]
                short_break_time = task[2]
                long_break_time = task[3]
                break

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.configure(background='#BA4949')
        self.edit_window.title("Edit Timer Settings")


        # Calculate center position
        window_width, window_height = 300, 350
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        
        self.edit_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        
        ttk.Label(self.edit_window, text="Work Time (minutes):").pack(pady=5)
        self.work_time_entry = tk.Entry(self.edit_window)
        self.work_time_entry.pack(pady=5)
        self.work_time_entry.insert(0, str(work_time // 60))
        
        ttk.Label(self.edit_window, text="Short Break Time (minutes):").pack(pady=5)
        self.short_break_time_entry = tk.Entry(self.edit_window)
        self.short_break_time_entry.pack(pady=5)
        self.short_break_time_entry.insert(0, str(short_break_time// 60))
        
        ttk.Label(self.edit_window, text="Long Break Time (minutes):").pack(pady=5)
        self.long_break_time_entry = tk.Entry(self.edit_window)
        self.long_break_time_entry.pack(pady=5)
        self.long_break_time_entry.insert(0, str(long_break_time // 60))

        ttk.Label(self.edit_window, text="Task Name:").pack(pady=5)
        self.task_entry = tk.Entry(self.edit_window)
        self.task_entry.pack(pady=5)
        self.task_entry.insert(0, task_name)
        
        ttk.Button(self.edit_window, text="Save", command=self.save_timer_settings).pack(pady=20)

    def save_timer_settings(self):
        global WORK_TIME, SHORT_BREAK_TIME, LONG_BREAK_TIME
        try:
            WORK_TIME = int(self.work_time_entry.get()) * 60
            SHORT_BREAK_TIME = int(self.short_break_time_entry.get()) * 60
            LONG_BREAK_TIME = int(self.long_break_time_entry.get()) * 60
            task_name = self.task_entry.get()
            self.work_time = WORK_TIME
            self.short_break_time = SHORT_BREAK_TIME
            self.long_break_time = LONG_BREAK_TIME
            update_task(task_name, WORK_TIME, SHORT_BREAK_TIME, LONG_BREAK_TIME)
            self.load_tasks
            self.update_timer_label()
            self.edit_window.destroy()
            messagebox.showinfo("Task Updated", "Tasks successfully updated!")
        except ValueError:
            messagebox.showwarning("Invalid input", "Please enter valid integer values for the times.")
    
    def update_timer_label(self):
        minutes, seconds = divmod(self.work_time, 60)
        self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
    
    
    def on_task_select(self, event):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.edit_button.config(state=tk.NORMAL)
        except IndexError:
            self.edit_button.config(state=tk.DISABLED)
    
    def claim_reward(self, idx):
        messagebox.showinfo("Achievement Claimed", f"You have claimed your reward for task {idx + 1}!")
        self.reward_buttons[idx].config(state=tk.DISABLED)  # Disable the button again after claiming reward
        self.show_achievement()
        self.toggle_button.config(state=tk.NORMAL)

    def check_task_completion(self):
    # Iterate through missions and mark them as completed if conditions are met
     for index, mission in enumerate(self.missions):
        if mission == "Complete 1 Pomodoro session" and self.pomodoros_completed >= 1:
            self.mark_task_completed(index)
        elif mission == "Complete 3 pomodoro session" and self.pomodoros_completed >= 3:
            self.mark_task_completed(index)
        # Add more conditions for other missions as needed

    def mark_task_completed(self, index):
    # Update the GUI to mark the task as completed
     self.listbox_missions.itemconfig(index, {'bg': 'green', 'fg': 'black'})
     self.reward_buttons[index].configure(state=tk.NORMAL)



    def toggle_lock(self):
        if self.is_locked:
            self.image_label.config(image=self.unlock_photo)
        else:
            self.image_label.config(image=self.lock_photo)
            self.toggle_button.config(text="Unlock")
        self.is_locked = not self.is_locked

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    pomodoro_timer = PomodoroTimer()
    pomodoro_timer.run()
