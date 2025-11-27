import pygame
import os
from ffpyplayer.player import MediaPlayer
from ffpyplayer.tools import set_loglevel
from pymediainfo import MediaInfo
from errno import ENOENT


class Video:
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(ENOENT, os.strerror(ENOENT), path)
        set_loglevel("quiet")

        self.path = path
        self.name = os.path.splitext(os.path.basename(path))[0]

        self._video = MediaPlayer(path, ff_opts={'paused': False, 'autoexit': True})
        self._frame_num = 0

        info = MediaInfo.parse(path).video_tracks[0]

        self.frame_rate = float(info.frame_rate)
        self.frame_count = int(info.frame_count)
        self.frame_delay = 1 / self.frame_rate
        self.duration = info.duration / 1000
        self.original_size = (info.width, info.height)
        self.current_size = self.original_size

        self.active = True
        self.frame_surf = pygame.Surface(self.current_size)
        self.frame_surf.fill((0, 0, 0))

        self.alt_resize = pygame.transform.smoothscale

    def close(self):
        self._video.close_player()
        self.active = False

    def restart(self):
        self._video.seek(0, relative=False)
        self._frame_num = 0
        self.frame_surf = pygame.Surface(self.current_size)
        self.frame_surf.fill((0, 0, 0))
        self.active = True

    def set_size(self, size: tuple):
        self.current_size = size
        if self.frame_surf:
            self.frame_surf = pygame.transform.scale(self.frame_surf, size)

    def get_paused(self) -> bool:
        return self._video.get_pause()

    def pause(self):
        self._video.set_pause(True)

    def resume(self):
        self._video.set_pause(False)

    def get_pos(self) -> float:
        return self._video.get_pts()

    def toggle_pause(self):
        self._video.toggle_pause()

    def _update(self):
        # 프레임 가져오기
        frame, val = self._video.get_frame()

        if val == 'eof':
            self.active = False
            return False

        if frame is None:
            return False

        # 이미지 데이터 추출
        img, t = frame
        if img is None:
            return False

        # pygame surface로 변환
        size = img.get_size()
        img_bytes = img.to_bytearray()[0]

        try:
            surf = pygame.image.frombuffer(img_bytes, size, "RGB")

            # 크기 조정
            if size != self.current_size:
                surf = self.alt_resize(surf, self.current_size)

            self.frame_surf = surf
            self._frame_num += 1
            return True

        except Exception as e:
            print(f"프레임 변환 에러: {e}")
            return False

    def seek(self, seek_time: int):
        vid_time = self._video.get_pts()
        if vid_time + seek_time < self.duration and self.active:
            self._video.seek(seek_time)
            while vid_time + seek_time < self._frame_num * self.frame_delay:
                self._frame_num -= 1

    def draw(self, surf: pygame.Surface, pos: tuple, force_draw: bool = True) -> bool:
        if not self.active:
            return False

        if self._update() or force_draw:
            surf.blit(self.frame_surf, pos)
            return True

        return False