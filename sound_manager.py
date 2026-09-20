import pygame
import os


class SoundManager:
    """游戏音效管理器"""

    def __init__(self, game):
        self.game = game
        self.sounds = {}
        self.music_playing = False

        self._sounds_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'sounds')

        self._setup_channels()
        self._load_sounds()

    def _setup_channels(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)

    def _load_sounds(self):
        sound_files = {
            'shoot': 'shoot.wav',
            'explode': 'explode.wav',
            'hit': 'hit.wav',
            'levelup': 'levelup.wav',
            'gameover': 'gameover.wav',
            'start': 'start.wav',
        }

        for key, filename in sound_files.items():
            path = os.path.join(self._sounds_dir, filename)
            if os.path.exists(path):
                try:
                    self.sounds[key] = pygame.mixer.Sound(path)
                except pygame.error:
                    pass

    def play(self, name, volume=1.0):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
            self.sounds[name].play()

    def play_music(self, filename, loops=-1, volume=0.4):
        path = os.path.join(self._sounds_dir, filename)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops=loops)
                self.music_playing = True
            except pygame.error:
                self.music_playing = False

    def stop_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def pause_music(self):
        if self.music_playing:
            pygame.mixer.music.pause()

    def resume_music(self):
        if self.music_playing:
            pygame.mixer.music.unpause()