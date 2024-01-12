import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.setup_audio()

    def setup_gui(self):
        self.root.title("Music Player")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        bg_image_path = os.path.join(script_dir, "music", "bg_con.png")

        if not os.path.exists(bg_image_path):
            messagebox.showerror("Error", f"Background image not found at {bg_image_path}")
            self.root.destroy()
            return

        self.bg_image = tk.PhotoImage(file=bg_image_path)
        self.bg_label = ttk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        style = ThemedStyle(self.root)
        style.set_theme("arc")

        self.playlist_frame = ttk.Frame(self.root)
        self.playlist_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.control_frame = ttk.Frame(self.root, style="TFrame")
        self.control_frame.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

        self.setup_playlist()
        self.setup_controls()

    def setup_controls(self):
        self.skip_backward_button = ttk.Button(self.control_frame, text="⏪ Skip Backward", command=self.skip_backward)
        self.skip_backward_button.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.play_pause_button = ttk.Button(self.control_frame, text="▶️ Play", command=self.play_pause)
        self.play_pause_button.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="ew")

        self.skip_forward_button = ttk.Button(self.control_frame, text="Skip Forward ⏩", command=self.skip_forward)
        self.skip_forward_button.grid(row=0, column=2, padx=20, pady=(10, 0), sticky="ew")

        self.volume_scale = ttk.Scale(self.control_frame, orient="horizontal", from_=0, to=1, 
                                    variable=tk.DoubleVar(), command=self.set_volume, style="Horizontal.TScale")
        self.volume_scale.grid(row=1, column=0, columnspan=3, padx=30, pady=(20, 10), sticky="ew")

        self.progress_bar = ttk.Progressbar(self.control_frame, orient="horizontal", length=500, mode="determinate")
        self.progress_bar.grid(row=2, column=0, columnspan=3, padx=30, pady=(0, 10), sticky="ew")

        self.elapsed_time = ttk.Label(self.control_frame, text="00:00")
        self.elapsed_time.grid(row=3, column=0, columnspan=3, padx=30, pady=(0, 10), sticky="ew")

        self.import_button = ttk.Button(self.control_frame, text="Import Music", command=self.import_music)
        self.import_button.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="ew")

       
    def setup_playlist(self):
        self.playlist = tk.Listbox(self.playlist_frame, width=70, height=15, selectbackground="#4CAF50", selectforeground="white")
        self.playlist.pack(expand=True, fill='both', pady=(10, 10))
        self.playlist.bind("<Double-Button-1>", self.play_selected)

        scrollbar = ttk.Scrollbar(self.playlist_frame, orient="vertical", command=self.playlist.yview)
        scrollbar.pack(side="right", fill="y")
        self.playlist.config(yscrollcommand=scrollbar.set)

    def setup_audio(self):
        pygame.init()
        pygame.mixer.init()

        self.music_player = pygame.mixer.music

        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        self.current_song = None
        self.paused = False

        self.music_player.set_volume(0.5)

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.get_busy()  

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.get_busy() 

    def play_selected(self, event):
        selected_song = self.playlist.get(self.playlist.curselection())
        self.current_song = selected_song
        pygame.mixer.music.load(self.current_song)
        self.progress_bar["maximum"] = pygame.mixer.Sound(self.current_song).get_length()
        self.update_progressbar()
        pygame.mixer.music.play()
        self.play_pause_button["text"] = "⏸ Pause"

    def play_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.play_pause_button["text"] = "⏸ Pause"
        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.play_pause_button["text"] = "▶️ Play"

    def skip_backward(self):
        selection = self.playlist.curselection()
        if selection:
            prev_song_index = int(selection[0]) - 1
            if prev_song_index >= 0:
                prev_song = self.playlist.get(prev_song_index)
                self.current_song = prev_song
                pygame.mixer.music.load(self.current_song)
                self.progress_bar["maximum"] = pygame.mixer.Sound(self.current_song).get_length()
                self.update_progressbar()
                pygame.mixer.music.play()
                self.play_pause_button["text"] = "⏸ Pause"
            else:
                messagebox.showwarning("Warning", "This is the first song.")
        else:
            messagebox.showerror("Error", "No song is selected.")

    def skip_forward(self):
        selection = self.playlist.curselection()
        if selection:
            next_song_index = int(selection[0]) + 1
            if next_song_index < self.playlist.size():
                next_song = self.playlist.get(next_song_index)
                self.current_song = next_song
                pygame.mixer.music.load(self.current_song)
                self.progress_bar["maximum"] = pygame.mixer.Sound(self.current_song).get_length()
                self.update_progressbar()
                pygame.mixer.music.play()
                self.play_pause_button["text"] = "⏸ Pause"
            else:
                messagebox.showwarning("Warning", "This is the last song.")

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

    def import_music(self):
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            if file_path not in self.playlist.get(0, tk.END):
                self.playlist.insert(tk.END, file_path)

    def update_progressbar(self):
        current_time = pygame.mixer.music.get_pos() / 1000
        self.progress_bar["value"] = current_time
        minutes, seconds = divmod(int(current_time), 60)
        self.elapsed_time.config(text="{:02d}:{:02d}".format(minutes, seconds))
        self.root.after(1000, self.update_progressbar)

if __name__ == "__main__":
    root = tk.Tk()
    MusicPlayer(root)
    root.mainloop()
