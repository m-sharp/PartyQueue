import json

from .mobile_client import MobileClientWrapper
from .models import Track
from .repos import PlaylistRepository
from .repos import TrackRepository


class ConfigFileController:

    def __init__(self):
        self.config_dict = {}
        with open('config.json', 'r') as f:
            data = f.read()
        self.config_dict = json.loads(data)

    @property
    def username(self):
        return self.config_dict['PlayUsername']

    @property
    def password(self):
        return self.config_dict['PlayPassword']

    @property
    def slack_token(self):
        return self.config_dict['SlackToken']


class PartyQueueController:

    PLAYLIST_NAME = 'PartyQueue'

    def __init__(self):
        self.playlist_controller = PlaylistController()
        self.track_controller = TrackController()
        self.party_queue_playlist = self.get_party_queue()
        self.playlist_extended_objects = list()
        self.tracks = self.get_songs_from_party_queue()

    def get_party_queue(self):
        party_queue = self.playlist_controller.get_playlist_by_name(self.PLAYLIST_NAME)
        if party_queue is None:
            return self.create_party_queue()
        return party_queue

    def get_songs_from_party_queue(self):
        tracks = list()
        for entry in self.party_queue_playlist.Entries:
            track = self.track_controller.get_track(entry.TrackId)
            tracks.append(track)
        return tracks

    def create_party_queue(self):
        """
        Starts the Party Queue by creating it
        :return:
        """
        return self.playlist_controller.make_new_playlist(self.PLAYLIST_NAME, 'See you in Slack!', True)

    def close_party_queue(self):
        self.playlist_controller.delete_playlist(self.party_queue_playlist.Id)

    def get_share_url(self):
        return 'https://play.google.com/music/playlist/' + self.party_queue_playlist.ShareToken

    def add_to_play_list(self, track_id, requested_by):
        self.playlist_controller.add_track_to_playlist(self.party_queue_playlist.Id, track_id)
        self.populate_extended_properties(track_id, requested_by)
        self.playlist_controller.refresh_repo()
        self.party_queue_playlist = self.get_party_queue()

    @staticmethod
    def assemble_extended_properties(track_id, requested_by):
        return {'TrackId': track_id, 'RequestedBy': requested_by}

    def populate_extended_properties(self, track_id, requested_by):
        self.playlist_extended_objects.append(self.assemble_extended_properties(track_id, requested_by))

    def remove_from_play_list(self, track_id):
        for entry in self.party_queue_playlist.Entries:
            if entry.TrackId == track_id:
                self.playlist_controller.remove_playlist_entry(entry.Id)
        self.playlist_extended_objects.remove(self.get_extended_object(track_id))

    def get_extended_object(self, track_id):
        for extendedObject in self.playlist_extended_objects:
            if extendedObject['TrackId'] == track_id:
                return extendedObject

    # TODO: Figure out how to fairly sort
    # def SortPartyQueue(self):
    #    for idx, playListEntry in enumerate(self.PartyQueuePlaylistDO.Entries):
    #        if idx == 0:
    #            continue
    #        elif idx == playListEntry[-1]:
    #            break
    #        extendedObject = self.GetExtendedObject(playListEntry.TrackId)
    #        totalForUser = self.GetTotalEntriesForUser(extendedObject['RequestedBy'])
    #        if totalForUser == len(self.PartyQueuePlaylistDO.Entries):
    #            break
    #        elif totalForUser == 1:
    #            continue

    #        nextExtendedObject = self.GetExtendedObject(self.PartyQueuePlaylistsDO[idx+1].TrackId)
    #        previousExtendedObject = self.GetExtendedObject(self.PartyQueuePlaylistsDO[idx-1].TrackId)
    #   if extendedObject['RequestedBy'] == nextExtendedObject['RequestedBy'] == previousExtendedObject['RequestedBy']:

    # def GetTotalEntriesForUser(self, userId):
    #    entriesForUser = 0
    #    for extendedObject in self.PlaylistExtendedObjectList:
    #        if extendedObject['RequestedBy'] == userId:
    #            entriesForUser = entriesForUser + 1
    #    return entriesForUser


class PlaylistController:

    def __init__(self):
        self.client = MobileClientWrapper()
        self.playlist_repo = PlaylistRepository()

    def refresh_repo(self):
        self.playlist_repo.refresh()

    def get_playlist_by_name(self, play_list_name):
        """
        Searches Playlist Repository for a Playlist with target name

        :param play_list_name: name of target Playlist
        :return:
        """
        for playListDO in self.playlist_repo.playlists:
            if playListDO.Name == play_list_name:
                return playListDO
        return None

    def get_playlist_by_id(self, play_list_id):
        """
        Searches Playlist Repository for a Playlist with target Id

        :param play_list_id: id of target Playlist
        :return:
        """
        for playListDO in self.playlist_repo.playlists:
            if playListDO.Id == play_list_id:
                return playListDO
        return None

    def make_new_playlist(self, new_name, new_description, share):
        """
        Creates a new Playlist

        :param new_name: Name of new Playlist
        :param new_description: Description of new Playlist
        :param share: bool whether to share publically
        :return: new Playlist
        """
        new_playlist_id = self.client.create_playlist(new_name, new_description, share)
        self.refresh_repo()
        return self.get_playlist_by_id(new_playlist_id)

    def delete_playlist(self, id_):
        """
        #Deletes Playlist with target id

        :param id_: id of target Playlist to delete
        :return: true if successful
        """
        deleted_id = self.client.delete_playlist(id_)
        if deleted_id == id_:
            self.refresh_repo()
            return True
        return False

    def add_track_to_playlist(self, target_playlist_id, track_id):
        """
        Adds target Track to target Playlist

        :param target_playlist_id: id of Playlist to add to
        :param track_id: id of Track to add
        :return: true if successful
        """
        list_of_track_ids_added = self.client.add_songs_to_playlist(target_playlist_id, track_id)
        if list_of_track_ids_added[0] == track_id:
            self.refresh_repo()
            return True
        return False

    def reorder_playlist_entry(self, target_playlist_entry_id, play_list_entry_id_after, play_list_entry_id_before):
        """
        Reorders PlaylistEntry with targetPlaylistEntryId after PlaylistEntry with playListEntryIdAfter and before
        PlaylistEntry with playListEntryIdBefore

        :param target_playlist_entry_id:
        :param play_list_entry_id_after:
        :param play_list_entry_id_before:
        :return:
        """
        self.client.reorder_playlist_entry(
            target_playlist_entry_id, play_list_entry_id_after, play_list_entry_id_before
        )
        self.refresh_repo()

    def remove_playlist_entry(self, entry_id):
        """
        Removes target PlaylistEntry from its Playlist

        :param entry_id: Id of target Entry to delete
        :return:
        """
        playlist_entry_ids_removed = self.client.remove_entries_from_playlist(entry_id)
        if playlist_entry_ids_removed[0] == entry_id:
            self.refresh_repo()
            return True
        return False


class SearchController:

    def __init__(self):
        self.client = MobileClientWrapper()

    def get_search_results(self, query, type_):
        results = self.client.search(query)
        list_of_song_search_results = results['song_hits']
        result_list = list()

        for track in list_of_song_search_results:
            result_list.append(Track(track['track']))

        filtered_list = list()
        if type_ in ['Artist']:
            for trackDo in result_list:
                if query.lower() in trackDo.artist.lower():
                    filtered_list.append(trackDo)
        if type_ in ['Song']:
            for trackDo in result_list:
                if query.lower() in trackDo.title.lower():
                    filtered_list.append(trackDo)

        return filtered_list


class TrackController:

    def __init__(self):
        self.client = MobileClientWrapper()
        self.track_repo = TrackRepository()

    def get_track(self, track_id):
        """
        Gets Track for target trackId

        :param track_id: target trackId
        :return:
        """
        track = Track(self.client.get_track_info(track_id))
        self.track_repo.add_to_repo(track)
        return track

    def add_track_to_repo(self, track_do):
        self.track_repo.add_to_repo(track_do)

    def get_track_by_artist_and_name(self, artist_name, track_name):
        for track in self.track_repo.tracks:
            if track.Title.lower() == track_name and track.Artist.lower() == artist_name:
                return track
        return None
