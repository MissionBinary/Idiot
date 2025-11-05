import random
import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

class F3PlayerApp(App):
    def __init__(self, **kwargs):
        super(F3PlayerApp, self).__init__(**kwargs)
        self.sound = None
        self.last_played = ""
        
    def build(self):
        # Create layout
        layout = FloatLayout()
        
        # Create label with instructions
        self.label = Label(
            text='F3 MP3 Player\n\nConnect keyboard and press F3\nto play random audio\n\nTap screen to play',
            font_size='20sp',
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        
        layout.add_widget(self.label)
        
        # Bind keyboard events
        Window.bind(on_keyboard=self.on_keyboard)
        
        # Bind touch events for tap to play
        layout.bind(on_touch_down=self.on_touch)
        
        return layout
    
    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle keyboard events"""
        # F3 key code is 292 on most systems
        if key == 292 or scancode == 292:
            self.play_random_mp3()
            return True
        return False
    
    def on_touch(self, instance, touch):
        """Handle screen tap"""
        self.play_random_mp3()
        return True
    
    def play_random_mp3(self):
        """Play a random MP3 file (1.mp3 or 2.mp3)"""
        # Stop any currently playing audio
        if self.sound:
            self.sound.stop()
        
        # Randomly choose between 1 and 2
        choice = random.randint(1, 2)
        mp3_file = f"{choice}.mp3"
        
        # Get the path to the MP3 file
        # On Android, files should be in the app's directory
        app_dir = os.path.dirname(os.path.abspath(__file__))
        mp3_path = os.path.join(app_dir, mp3_file)
        
        # Try loading from current directory if not found
        if not os.path.exists(mp3_path):
            mp3_path = mp3_file
        
        try:
            # Load and play the sound
            self.sound = SoundLoader.load(mp3_path)
            if self.sound:
                self.sound.play()
                self.last_played = mp3_file
                self.update_label(f"Playing: {mp3_file}")
            else:
                self.update_label(f"Error: Could not load {mp3_file}")
        except Exception as e:
            self.update_label(f"Error: {str(e)}")
    
    def update_label(self, message):
        """Update the label text"""
        self.label.text = f'F3 MP3 Player\n\n{message}\n\nPress F3 or tap screen\nto play random audio'

if __name__ == '__main__':
    F3PlayerApp().run()
