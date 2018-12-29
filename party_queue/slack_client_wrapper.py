from slackclient import SlackClient

from .controllers import PartyQueueController, SearchController, TrackController
from .mobile_client import MobileClientWrapper


class PartyQueueBot:

    def __init__(self, config):
        self.client = SlackClient(
            token=config.slack_token, client_id=config.slack_client_id, client_secret=config.slack_client_secret
        )
        self.bot_user_id = self._get_user_id()
        self.bot_mention = '<@{id_}>'.format(id_=self.bot_user_id)
        self.mobile_client = MobileClientWrapper(config)
        self.queue = PartyQueueController(self.mobile_client)
        self.track_controller = TrackController(self.mobile_client)
        self.search_controller = SearchController(self.mobile_client)

    def _get_user_id(self):
        users = self.client.api_call('users.list')
        return [user for user in users['members'] if user['name'] == 'party_queue'][0]['id']

    def start_real_time_messaging(self):
        """
        Starts Real Time Messaging
        """
        if self.client.rtm_connect():
            print('PartyQueue up and listening! Ctrl+C to break.')

            try:
                while True:
                    last_read = self.client.rtm_read()
                    if not last_read:
                        continue
                    last_read = last_read[0]
                    last_read.setdefault('type', '')
                    last_read.setdefault('text', '')
                    if last_read['type'] == 'message' and self.bot_mention in last_read['text']:
                        self.handle_message(last_read)
            except KeyboardInterrupt:
                print('Cleaning up and logging out...')
                self.queue.close_party_queue()
                self.mobile_client.logout()

    def handle_message(self, last_read_message):
        """
        Handles a slack message

        :param last_read_message: dict of last read message
        """
        parsed_text = last_read_message['text']
        origin = last_read_message['channel']
        sender_user_id = last_read_message['user']
        if 'queue' in parsed_text.lower():
            self.get_queue_contents(origin)
        elif 'search' in parsed_text.lower():
            self.search_songs(origin, self.get_query(parsed_text.lower(), 'search'))
        elif 'add' in parsed_text.lower():
            self.add_song_by_name_and_title(origin, self.get_query(parsed_text.lower(), 'add'), sender_user_id)
        else:
            self.client.rtm_send_message(origin, 'I don\'t understand your stupid request.')

    @staticmethod
    def get_query(message, command):
        """
        Pulls out actual query from message string

        :param message: the message string
        :param command: the PartyQueue command string used in the message

        :return: query string
        """
        return message[message.index(command)+len(command)+1:]

    def get_queue_contents(self, origin):
        """
        Posts PartyQueue Entries to chat

        :param origin: channel where request originated
        """
        queue_tracks = self.queue.get_party_queue_tracks()
        if len(queue_tracks):
            text = '*Songs in the PartyQueue ({share}):*' \
                   '\n*-------------------------*\n'.format(share=self.queue.share_url())
            for index, track in enumerate(queue_tracks, start=1):
                text += '{count}. {artist} | {title}\n'.format(count=index, artist=track.artist, title=track.title)
        else:
            text = 'No Songs Currently in the Queue ({share})'.format(share=self.queue.share_url())
        self.client.rtm_send_message(origin, text)

    def search_songs(self, origin, query):
        """
        Posts results of search made on given query to chat

        :param origin: channel where request originated
        :param query: search query
        """
        text = '*Search Results for \'{query}\'*\n*-------------------------*\n'.format(**locals())
        for index, track in enumerate(self.search_controller.get_search_results(query), start=1):
            self.track_controller.add_track_to_repo(track)
            track_text = '{count}. {artist} | {title}\n'.format(count=index, artist=track.artist, title=track.title)
            text += track_text
        self.client.rtm_send_message(origin, text)

    def add_song_by_name_and_title(self, origin, artist_song_string, slack_user_id):
        """
        Adds a Song to the PartyQueue and Posts a notification

        :param origin: channel where request originated
        :param artist_song_string: Name of the song to add
        :param slack_user_id: ID of the slack user who requested the song
        """
        split_list = artist_song_string.split('|')
        artist = split_list[0].strip()
        track_name = split_list[1].strip()
        track = self.track_controller.get_track_by_artist_and_name(artist, track_name)
        if track is None:
            text = '*Could not find song {title}, try searching for it first*'.format(title=track_name.title())
        else:
            self.queue.add_to_play_list(track.store_id, slack_user_id)
            text = '*Added {title} to the Party Queue*'.format(title=track.title)
        self.client.rtm_send_message(origin, text)
