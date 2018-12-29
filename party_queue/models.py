class Playlist:

    def __init__(self, **kwargs):
        self.access_controlled = kwargs.get('accessControlled')
        self.creation_timestamp = kwargs.get('creationTimestamp')
        self.deleted = kwargs.get('deleted')
        self.entries = [PlaylistEntry(**entry) for entry in kwargs.get('tracks') or []]
        self.id_ = kwargs.get('id')
        self.kind = kwargs.get('kind')
        self.last_modified_timestamp = kwargs.get('lastModifiedTimestamp')
        self.name = kwargs.get('name')
        self.owner_name = kwargs.get('ownerName')
        self.owner_profile_photo_url = kwargs.get('ownerProfilePhotoUrl')
        self.recent_timestamp = kwargs.get('recentTimestamp')
        self.share_token = kwargs.get('shareToken')
        self.type = kwargs.get('type')


class PlaylistEntry:

    def __init__(self, **kwargs):
        self.absolute_position = kwargs.get('absolutePosition')
        self.creation_timestamp = kwargs.get('creationTimestamp')
        self.deleted = kwargs.get('deleted')
        self.id_ = kwargs.get('id')
        self.kind = kwargs.get('kind')
        self.last_modified_timestamp = kwargs.get('lastModifiedTimestamp')
        self.play_list_id = kwargs.get('playListId')
        self.source = kwargs.get('source')
        self.track_id = kwargs.get('trackId')  # trackId = nid/storeId in Track


class Track:

    def __init__(self, **kwargs):
        self.album = kwargs.get('album')
        self.album_art_url = kwargs.get('albumArtRef')[0]['url']
        self.album_artist = kwargs.get('albumArtist')
        self.album_id = kwargs.get('albumId')
        self.artist = kwargs.get('artist')
        self.artist_id = kwargs.get('artistId')[0]
        self.beats_per_minute = kwargs.get('beatsPerMinute')
        self.client_id = kwargs.get('clientId')
        self.comment = kwargs.get('comment')
        self.composer = kwargs.get('composer')
        self.creation_timestamp = kwargs.get('creationTimestamp')
        self.deleted = kwargs.get('deleted')
        self.disc_number = kwargs.get('discNumber')
        self.duration_millis = kwargs.get('durationMillis')
        self.estimated_size = kwargs.get('estimatedSize')
        self.genre = kwargs.get('genre')
        self.id_ = kwargs.get('id')
        self.kind = kwargs.get('kind')
        self.last_modified_timestamp = kwargs.get('lastModifiedTimestamp')
        self.nid = kwargs.get('nid')
        self.play_count = kwargs.get('playCount')
        self.rating = kwargs.get('rating')
        self.recent_timestamp = kwargs.get('recentTimestamp')
        self.store_id = kwargs.get('storeId')
        self.title = kwargs.get('title')
        self.total_disc_count = kwargs.get('totalDiscCount')
        self.total_track_count = kwargs.get('totalTrackCount')
        self.track_number = kwargs.get('trackNumber')
        self.year = kwargs.get('year')
