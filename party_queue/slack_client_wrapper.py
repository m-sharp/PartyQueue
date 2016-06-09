from slackclient import SlackClient

from .controllers import ConfigFileController, PartyQueueController, SearchController, TrackController


class SlackClientWrapper:

    def __init__(self):
        self.config = ConfigFileController()
        self.token = self.config.get_slack_token()
        self.client = SlackClient(self.token)
        self.queue = PartyQueueController()
        self.track_controller = TrackController()
        self.search_controller = SearchController()

    def start_real_time_messaging(self):
        """
        Starts Real Time Messaging
        """
        if self.client.rtm_connect():
            print('PartyQueue up and listening! Ctrl+C to break.')
            try:
                while True:
                    last_read = self.client.rtm_read()
                    if last_read:
                        has_type = 'type' in last_read[0]
                        if has_type and last_read[0]['type'] == 'message':
                            self.handle_message(last_read[0])
            except KeyboardInterrupt:
                pass

    def handle_message(self, last_read_message):
        """
        Handles a slack message

        :param last_read_message: dict of last read message
        """
        parsed_text = last_read_message['text']
        origin_channel = last_read_message['channel']
        slack_user_id = last_read_message['user']
        if parsed_text and 'partyqueue' in parsed_text:
            if 'getqueue' in parsed_text.lower():
                self.get_party_queue_contents(origin_channel)
            elif 'searchartist' in parsed_text.lower():
                self.search_songs_for_text(
                    origin_channel, self.get_query_from_message(parsed_text.lower(), 'searchartist'), 'Artist'
                )
            elif 'searchsong' in parsed_text.lower():
                self.search_songs_for_text(
                    origin_channel, self.get_query_from_message(parsed_text.lower(), 'searchsong'), 'Song'
                )
            elif 'addsong' in parsed_text.lower():
                self.add_song_by_name_and_title(
                    origin_channel, self.get_query_from_message(parsed_text.lower(), 'addsong'), slack_user_id
                )
            else:
                self.client.rtm_send_message(origin_channel, 'I don\'t understand your stupid request.')

    def get_party_queue_contents(self, origin):
        """
        Posts PartyQueue Entries to chat

        :param origin: channel where request originated
        """
        text = '*Songs in PartyQueue:*\n*-------------------------*\n'
        count = 1
        for track in self.queue.get_songs_from_party_queue():
            text = text + str(count) + '. ' + track.Artist + '|' + track.Title + '\n'
            count = count + 1
        self.client.rtm_send_message(origin, text)

    def search_songs_for_text(self, origin, query, type_):
        """
        Posts results of search made on given query to chat

        :param origin: channel where request originated
        :param query: search query
        :param type_: either song search or artist search
        """
        text = '*' + type_ + ' Search Results for \'' + query + '\'*\n*-------------------------*\n'
        count = 1
        filtered_song_data = self.search_controller.get_search_results(query, type_)
        for track in filtered_song_data:
            self.track_controller.add_track_to_repo(track)
            text = text + str(count) + '. ' + track.Artist + '|' + track.Title + '\n'
            count = count + 1
        self.client.rtm_send_message(origin, text)

    @staticmethod
    def get_query_from_message(message, command):
        """
        Pulls out actual query from message string

        :param message: the message string
        :param command: the PartyQueue command string used in the message

        :return: ?
        """
        starting_index = message.index(command)
        message_length = len(message)
        command_length = len(command)
        extracted_query = message[starting_index+command_length+1:message_length]
        return extracted_query

    def add_song_by_name_and_title(self, origin, artist_song_string, slack_user_id):
        """
        Adds a Song to the PartyQueue and Posts a notification

        :param origin: channel where request originated
        :param artist_song_string: Name of the song to add
        :param slack_user_id: ID of the slack user who requested the song
        """
        split_list = artist_song_string.split('|')
        track = self.track_controller.get_track_by_artist_and_name(split_list[0], split_list[1].rstrip())
        if track is None:
            text = '*Could not find song ' + split_list[1] + ', try searching for it!*'
        else:
            self.queue.add_to_play_list(track.StoreId, slack_user_id)
            text = '*' + 'Added ' + split_list[1] + ' to PartyQueue!*\n*-------------------------*'
        self.client.rtm_send_message(origin, text)
