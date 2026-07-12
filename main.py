import threading
import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.metrics import dp
import yt_dlp

# Pydroid එකේ crash වෙන එක නවත්වන Logger එක
class MyLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

class DownloaderApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        screen = MDScreen()
        
        # Title
        screen.add_widget(MDLabel(text="Premium Video Downloader Pro", halign="center", pos_hint={"center_x": 0.5, "center_y": 0.88}, font_style="H5", theme_text_color="Primary"))
        
        # URL Input
        self.url_input = MDTextField(hint_text="Paste Video URL Here", pos_hint={"center_x": 0.5, "center_y": 0.75}, size_hint_x=0.8)
        screen.add_widget(self.url_input)
        
        # Quality Selector Label & Spinner
        screen.add_widget(MDLabel(text="Quality:", pos_hint={"center_x": 0.6, "center_y": 0.65}, theme_text_color="Secondary"))
        self.quality_spinner = Spinner(text="720p", values=("1080p", "720p", "480p", "360p"), size_hint=(0.25, 0.05), pos_hint={"center_x": 0.75, "center_y": 0.65}, background_color=(0.9, 0.5, 0, 1))
        screen.add_widget(self.quality_spinner)
        
        # Progress Bar (සිහින් ඉරක් ලෙස)
        self.progress_bar = MDProgressBar(value=0, pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint_x=0.8, size_hint_y=None, height=dp(4))
        screen.add_widget(self.progress_bar)
        
        # Details Label
        self.details_label = MDLabel(text="0.00 MB / 0.00 MB (0%)", halign="center", pos_hint={"center_x": 0.5, "center_y": 0.42}, theme_text_color="Secondary")
        screen.add_widget(self.details_label)
        
        # Download Button
        self.download_btn = MDRaisedButton(text="Download Video", pos_hint={"center_x": 0.5, "center_y": 0.3}, on_release=self.start_download_thread)
        screen.add_widget(self.download_btn)
        
        # Status Label
        self.status_label = MDLabel(text="Ready", halign="center", pos_hint={"center_x": 0.5, "center_y": 0.18}, theme_text_color="Secondary")
        screen.add_widget(self.status_label)
        
        return screen

    def start_download_thread(self, instance):
        self.status_label.text = "Starting..."
        threading.Thread(target=self.download_video).start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            curr_bytes = d.get('downloaded_bytes', 0)
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            curr_mb = curr_bytes / 1048576 
            
            if total_bytes > 0:
                total_mb = total_bytes / 1048576
                percent = (curr_bytes / total_bytes) * 100
                Clock.schedule_once(lambda dt: self.update_ui(percent, curr_mb, total_mb))
            else:
                Clock.schedule_once(lambda dt: self.update_ui_unknown(curr_mb))
                
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.download_finished())

    def update_ui(self, p, curr, tot):
        self.progress_bar.value = p
        self.details_label.text = f"{curr:.2f} MB / {tot:.2f} MB ({p:.1f}%)"
        self.status_label.text = "Downloading... Please wait!"

    def update_ui_unknown(self, curr):
        self.progress_bar.value = 0
        self.details_label.text = f"{curr:.2f} MB / Unknown Size"
        self.status_label.text = "Downloading... Please wait!"

    def download_finished(self):
        self.progress_bar.value = 100
        self.details_label.text = "Download Complete!"
        self.status_label.text = "Success! Video saved to Downloads."

    def download_video(self):
        url = self.url_input.text.strip()
        if not url: return
        
        # Spinner එකෙන් තෝරපු quality එක ලබා ගැනීම
        selected_res = self.quality_spinner.text.replace("p", "")
        
        Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 0))
        Clock.schedule_once(lambda dt: setattr(self.details_label, 'text', "Fetching info..."))
        
        try:
            download_path = '/storage/emulated/0/Download/%(title)s.mp4'
            if not os.path.exists('/storage/emulated/0/Download'):
                download_path = '%(title)s.mp4'
                
            # තෝරපු Quality එකට අනුව Download Format එක හැදීම
            ydl_opts = {
                'format': f'best[height<={selected_res}]/best', 
                'outtmpl': download_path, 
                'logger': MyLogger(),
                'progress_hooks': [self.progress_hook],
                'no_warnings': True,
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f"Error: {str(e)[:40]}"))

if __name__ == "__main__":
    DownloaderApp().run()
