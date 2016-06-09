class Playlist:

    def __init__(self, play_list_dict):
        if 'accessControlled' in play_list_dict:
            self.access_controlled = play_list_dict['accessControlled']
        if 'creationTimestamp' in play_list_dict:
            self.creation_timestamp = play_list_dict['creationTimestamp']
        if 'deleted' in play_list_dict:
            self.deleted = play_list_dict['deleted']
        if 'id' in play_list_dict:
            self.id_ = play_list_dict['id']
        if 'kind' in play_list_dict:
            self.kind = play_list_dict['kind']
        if 'lastModifiedTimestamp' in play_list_dict:
            self.last_modified_timestamp = play_list_dict['lastModifiedTimestamp']
        if 'name' in play_list_dict:
            self.name = play_list_dict['name']
        if 'ownerName' in play_list_dict:
            self.owner_name = play_list_dict['ownerName']
        if 'ownerProfilePhotoUrl' in play_list_dict:
            self.owner_profile_photo_url = play_list_dict['ownerProfilePhotoUrl']
        if 'recentTimestamp' in play_list_dict:
            self.recent_timestamp = play_list_dict['recentTimestamp']
        if 'shareToken' in play_list_dict:
            self.share_token = play_list_dict['shareToken']
        if 'type' in play_list_dict:
            self.type = play_list_dict['type']
        if 'tracks' in play_list_dict:
            self.entries = self.build_out_entry_list(play_list_dict['tracks'])

    @staticmethod
    def build_out_entry_list(entry_list):
        entries = list()
        for entry in entry_list:
            entries.append(PlaylistEntry(entry))
        return entries


class PlaylistEntry:

    def __init__(self, entry_dict):
        if 'absolutePosition' in entry_dict:
            self.absolute_position = entry_dict['absolutePosition']
        if 'creationTimestamp' in entry_dict:
            self.creation_timestamp = entry_dict['creationTimestamp']
        if 'deleted' in entry_dict:
            self.deleted = entry_dict['deleted']
        if 'id' in entry_dict:
            self.id_ = entry_dict['id']
        if 'kind' in entry_dict:
            self.kind = entry_dict['kind']
        if 'lastModifiedTimestamp' in entry_dict:
            self.last_modified_timestamp = entry_dict['lastModifiedTimestamp']
        if 'playListId' in entry_dict:
            self.play_list_id = entry_dict['playListId']
        if 'source' in entry_dict:
            self.source = entry_dict['source']
        # trackId = nid/storeId in Track
        if 'trackId' in entry_dict:
            self.track_id = entry_dict['trackId']


class Track:

    def __init__(self, track_dict):
        if 'comment' in track_dict:
            self.comment = track_dict['comment']
        if 'rating' in track_dict:
            self.rating = track_dict['rating']
        if 'albumArtRef' in track_dict:
            self.album_art_url = track_dict['albumArtRef'][0]['url']
        if 'artistId' in track_dict:
            self.artist_id = track_dict['artistId'][0]
        if 'composer' in track_dict:
            self.composer = track_dict['composer']
        if 'year' in track_dict:
            self.year = track_dict['year']
        if 'creationTimestamp' in track_dict:
            self.creation_timestamp = track_dict['creationTimestamp']
        if 'id' in track_dict:
            self.id_ = track_dict['id']
        if 'album' in track_dict:
            self.album = track_dict['album']
        if 'totalDiscCount' in track_dict:
            self.total_disc_count = track_dict['totalDiscCount']
        if 'title' in track_dict:
            self.title = track_dict['title']
        if 'recentTimestamp' in track_dict:
            self.recent_timestamp = track_dict['recentTimestamp']
        if 'albumArtist' in track_dict:
            self.album_artist = track_dict['albumArtist']
        if 'trackNumber' in track_dict:
            self.track_number = track_dict['trackNumber']
        if 'discNumber' in track_dict:
            self.disc_number = track_dict['discNumber']
        if 'deleted' in track_dict:
            self.deleted = track_dict['deleted']
        if 'storeId' in track_dict:
            self.store_id = track_dict['storeId']
        if 'nid' in track_dict:
            self.nid = track_dict['nid']
        if 'totalTrackCount' in track_dict:
            self.total_track_count = track_dict['totalTrackCount']
        if 'estimatedSize' in track_dict:
            self.estimated_size = track_dict['estimatedSize']
        if 'albumId' in track_dict:
            self.album_id = track_dict['albumId']
        if 'beatsPerMinute' in track_dict:
            self.beats_per_minute = track_dict['beatsPerMinute']
        if 'genre' in track_dict:
            self.genre = track_dict['genre']
        if 'playCount' in track_dict:
            self.play_count = track_dict['playCount']
        if 'kind' in track_dict:
            self.kind = track_dict['kind']
        if 'artist' in track_dict:
            self.artist = track_dict['artist']
        if 'lastModifiedTimestamp' in track_dict:
            self.last_modified_timestamp = track_dict['lastModifiedTimestamp']
        if 'clientId' in track_dict:
            self.client_id = track_dict['clientId']
        if 'durationMillis'in track_dict:
            self.duration_millis = track_dict['durationMillis']
