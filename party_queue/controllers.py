import typing as t

from .mobile_client import MobileClientWrapper
from .models import Playlist, Track


class PartyQueueController:

    PLAYLIST_NAME = 'PartyQueue'

    def __init__(self, mobile_client: MobileClientWrapper):
        self.playlist_controller = PlaylistController(mobile_client)
        self.track_controller = TrackController(mobile_client)
        self.__party_queue_playlist = None

    @property
    def party_queue_playlist(self) -> Playlist:
        self.__party_queue_playlist = self.playlist_controller.get_playlist_by_name(self.PLAYLIST_NAME)
        if self.__party_queue_playlist is None:
            return self.playlist_controller.create_playlist(self.PLAYLIST_NAME, 'See you in Slack!', True)
        return self.__party_queue_playlist

    @party_queue_playlist.setter
    def party_queue_playlist(self, val):
        self.__party_queue_playlist = val

    def get_party_queue_tracks(self):
        return [self.track_controller.get_track(entry.track_id) for entry in self.party_queue_playlist.entries]

    def close_party_queue(self):
        self.playlist_controller.delete_playlist(self.party_queue_playlist.id_)

    def share_url(self):
        return 'https://play.google.com/music/playlist/' + self.party_queue_playlist.share_token

    def add_to_play_list(self, track_id, requested_by):
        self.playlist_controller.add_tracks_to_playlist(self.party_queue_playlist.id_, track_id)
        self.party_queue_playlist = None


class PlaylistController:

    def __init__(self, mobile_client: MobileClientWrapper):
        self.client = mobile_client  # type: MobileClientWrapper
        self.playlists = list()  # type: t.List[Playlist]

    def refresh(self):
        self.playlists.clear()
        for playList in self.client.get_all_playlist_content():
            self.playlists.append(Playlist(**playList))

    def get_playlist_by_name(self, play_list_name):
        """
        Searches Playlist Repository for a Playlist with target name

        :param play_list_name: name of target Playlist
        :return:
        """
        for playList in self.playlists:
            if playList.name == play_list_name:
                return playList
        return None

    def get_playlist_by_id(self, play_list_id):
        """
        Searches Playlist Repository for a Playlist with target Id

        :param play_list_id: id of target Playlist
        :return:
        """
        for playList in self.playlists:
            if playList.id_ == play_list_id:
                return playList
        return None

    def create_playlist(self, new_name, new_description, share):
        """
        Creates a new Playlist

        :param new_name: Name of new Playlist
        :param new_description: Description of new Playlist
        :param share: bool whether to share publically
        :return: new Playlist
        """
        new_playlist_id = self.client.create_playlist(new_name, new_description, share)
        self.refresh()
        return self.get_playlist_by_id(new_playlist_id)

    def delete_playlist(self, id_):
        """
        Deletes Playlist with target id

        :param id_: id of target Playlist to delete
        :return: true if successful
        """
        self.client.delete_playlist(id_)
        self.refresh()

    def add_tracks_to_playlist(self, target_playlist_id, *track_ids):
        """
        Adds target Track to target Playlist

        :param target_playlist_id: id of Playlist to add to
        :param track_id: id of Track to add
        :return: true if successful
        """
        self.client.add_songs_to_playlist(target_playlist_id, track_ids)
        self.refresh()


class SearchController:

    def __init__(self, mobile_client: MobileClientWrapper):
        self.client = mobile_client  # type: MobileClientWrapper

    def get_search_results(self, query: str):
        results = self.client.search(query)
        result_list = [Track(**track['track']) for track in results['song_hits']]  # type: t.List[Track]
        # ToDo: real sorting
        filtered_list = list()
        for trackDo in result_list:
            if query.lower() in trackDo.title.lower() or query.lower() in trackDo.artist.lower():
                filtered_list.append(trackDo)
        return filtered_list


class TrackController:

    def __init__(self, mobile_client: MobileClientWrapper):
        self.client = mobile_client  # type: MobileClientWrapper
        self.tracks = list()  # type: t.List[Track]

    def add_to_repo(self, track):
        self.tracks.append(track)

    def get_track(self, track_id):
        track = Track(**self.client.get_track_info(track_id))
        self.add_to_repo(track)
        return track

    def add_track_to_repo(self, track_do):
        self.add_to_repo(track_do)

    def get_track_by_artist_and_name(self, artist_name: str, track_name: str):
        for track in self.tracks:
            if track_name == track.title.lower() and artist_name == track.artist.lower():
                return track
        return None
