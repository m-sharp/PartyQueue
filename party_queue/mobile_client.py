# GMusicApi Ref: http://unofficial-google-music-api.readthedocs.io/en/latest/usage.html

from gmusicapi import Mobileclient

from .controllers import ConfigFileController


class MobileClientWrapper:

    def __init__(self):
        self.client = Mobileclient()
        self.config = ConfigFileController()
        login = self.client.login(self.config.username, self.config.password, Mobileclient.FROM_MAC_ADDRESS)
        if not login:
            raise Exception('LoginFailure', 'MobileClientWrapper')

    def __del__(self):
        self.client.logout()

    def is_authenticated(self):
        """
        :return: Authentication Status of Mobileclient
        """
        return self.client.is_authenticated()

    def get_locale(self):
        """
        :return: Locale of Mobileclient
        """
        return self.client.locale

    def get_subscribed_status(self):
        """
        :return: subscription status of account logged into Mobileclient
        """
        del self.client.is_subscribed  # ToDo: Wtf?
        return self.client.is_subscribed

    def get_all_playlists(self):
        """
        Prefer GetAllPlaylistContent
        :return: list of all playlists as dictionaries
        """
        playlists = self.client.get_all_playlists()
        return playlists

    def get_all_playlist_content(self):
        """
        :return: list of all Playlist content as dictionaries.
        """
        return self.client.get_all_user_playlist_contents()

    def get_shared_playlist_content(self, share_token):
        """
        Returns content of a shared Playlist given a shareToken

        :param share_token: either the shareToken associated with the Playlist, or the playlist share Url
        :return: PlaylistEntry with it's Track included. Not sure on how useful this will be
        """
        return self.client.get_shared_playlist_contents(share_token)

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

    def reorder_playlist_entry(self, entry, entry_to_follow, entry_to_precede):
        """
        Reorders entry before entryToFollow and after entryToPrecede

        :param entry: entry to reorder
        :param entry_to_follow: entry to follow reorded entry
        :param entry_to_precede: entry to procede reorded entry
        """
        self.client.reorder_playlist_entry(entry, to_follow_entry=entry_to_follow, to_precede_entry=entry_to_precede)

    def remove_entries_from_playlist(self, entry_ids):
        """
        Removes given EntryID(s).

        :param entry_ids: id(s) of Playlist Entries to remove
        :return: list of Playlist Entry ids removed
        """
        return self.client.remove_entries_from_playlist(entry_ids)

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
