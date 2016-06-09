from .mobile_client import MobileClientWrapper
from .models import Playlist


class PlaylistRepository:

    def __init__(self):
        self.client = MobileClientWrapper()
        self.playlists = list()
        self.refresh()

    def refresh(self):
        """
        Clears and then populates Playlists List with Playlist's
        """
        del self.playlists[:]
        for playList in self.client.get_all_playlist_content():
            self.playlists.append(Playlist(playList))


class TrackRepository:

    def __init__(self):
        self.client = MobileClientWrapper()
        self.tracks = list()

    def refresh(self):
        """
        Clears the Repo
        """
        del self.tracks[:]

    def add_to_repo(self, track):
        self.tracks.append(track)
