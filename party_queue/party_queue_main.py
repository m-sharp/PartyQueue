from .controllers import PartyQueueController
from .slack_client_wrapper import SlackClientWrapper


print('Loading...')
sc = SlackClientWrapper()
pq = PartyQueueController()
sc.start_real_time_messaging()
pq.close_party_queue()
