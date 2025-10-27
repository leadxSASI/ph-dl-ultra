import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

class PornhubDownloaderGUI:
    def __init__(self, config, download_func):
        self.config = config
        self.download = download_func
        self.root = tk.Tk()
        self.root.title("PH-DL-ULTRA")
        self.root.geometry("600x500")
        self.root.configure(bg="#1a1a1a")
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        # URL
        ttk.Label(self.root, text="Pornhub URL:", foreground="white", background="#1a1a1a").pack(pady=10)
        self.url_entry = ttk.Entry(self.root, width=70)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, "https://www.pornhub.com/view_video.php?viewkey=")

        # Quality
        ttk.Label(self.root, text="Quality:", foreground="white", background="#1a1a1a").pack(pady=(20,5))
        self.quality_var = tk.StringVar(value=self.config["quality"])
        quality_combo = ttk.Combobox(self.root, textvariable=self.quality_var, state="readonly")
        from utils.quality import get_quality_options
        quality_combo['values'] = list(get_quality_options().keys())
        quality_combo.set("1080p")
        quality_combo.pack()

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Download", command=self.start_download).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Login", command=self.login).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Config", command=self.open_config).grid(row=0, column=2, padx=10)

        # Log
        self.log = tk.Text(self.root, height=10, bg="#000", fg="#0f0", font=("Consolas", 10))
        self.log.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    def log_msg(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url.startswith("http"):
            messagebox.showerror("Error", "Invalid URL")
            return
        quality_key = self.quality_var.get()
        from utils.quality import get_quality_options
        quality = get_quality_options()[quality_key]

        threading.Thread(target=self._download_thread, args=(url, quality), daemon=True).start()

    def _download_thread(self, url, quality):
        self.log_msg(f"Starting: {url}")
        success, msg = self.download(url, quality, gui_mode=True)
        self.log_msg(msg)
        if success:
            messagebox.showinfo("Done", "Download complete!")

    def login(self):
        from utils.login import export_cookies
        threading.Thread(target=lambda: [
            self.log_msg("Exporting cookies..."),
            export_cookies(self.config["browser"], "~/.config/ph-dl-ultra/cookies.txt"),
            self.log_msg("Login cookies updated!")
        ], daemon=True).start()

    def open_config(self):
        import webbrowser
        webbrowser.open(str(Path.home() / ".config" / "ph-dl-ultra" / "config.yaml"))

    def run(self):
        self.root.mainloop()
