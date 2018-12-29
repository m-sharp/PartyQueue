# GMusicApi Ref: http://unofficial-google-music-api.readthedocs.io/en/latest/usage.html
from gmusicapi import Mobileclient


class MobileClientWrapper:

    def __init__(self, config):
        self.client = Mobileclient(debug_logging=False)
        login = self.client.login(config.user_name, config.password, Mobileclient.FROM_MAC_ADDRESS)
        if not login:
            raise ConnectionError('MobileClientWrapper - Login Error Please Check Google Play Username and Password')

    def logout(self):
        self.client.logout()

    def get_all_playlist_content(self):
        """
        :return: list of all Playlist content as dictionaries.
        """
        return self.client.get_all_user_playlist_contents()

    def create_playlist(self, new_playlist_name, description_text, public_bool):
        """
        Creates a Playlist with given information and returns its id

        :param new_playlist_name: name to give new PlayList
        :param description_text: description text of new Playlist
        :param public_bool: True/False value to specify public sharing on new Playlist
        :return: playlist id
        """
        return self.client.create_playlist(new_playlist_name, description=description_text, public=public_bool)

    def delete_playlist(self, play_list_id):
        """
        Delete a Playlist with given Id

        :param play_list_id: playlist ID
        """
        self.client.delete_playlist(play_list_id)

    def add_songs_to_playlist(self, play_list_id, song_ids):
        """
        Adds given song(s) to given Playlist.

        :param play_list_id: id of the target Playlist
        :param song_ids: id(s) of the target Song to add
        :return: list of Playlist Entry ids added
        """
        return self.client.add_songs_to_playlist(play_list_id, song_ids)

    def get_track_info(self, store_track_id):
        """
        Returns information on a store track

        :param store_track_id: target TrackId
        """
        return self.client.get_track_info(store_track_id)

    def search(self, search_query):
        """
        Searches based on searchQuery
        :param search_query: query to run through music library

        :return: dictionary of hits
        """
        return self.client.search(search_query, max_results=10)
