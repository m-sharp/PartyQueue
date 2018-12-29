import click
import json

from .slack_client_wrapper import PartyQueueBot


context = dict(
    auto_envvar_prefix='PARTY_QUEUE',
    help_option_names=['-h', '--help']
)


class Config:

    def __init__(self, user_name: str, password: str, slack_token: str, slack_client_id: str, slack_client_secret: str):
        self.user_name = user_name
        if not self.user_name:
            raise SyntaxError('Missing argument: user_name')
        self.password = password
        if not self.password:
            raise SyntaxError('Missing argument: password')
        self.slack_token = slack_token
        if not self.slack_token:
            raise SyntaxError('Missing argument: slack_token')
        self.slack_client_id = slack_client_id
        if not self.slack_client_id:
            raise SyntaxError('Missing argument: slack_client_id')
        self.slack_client_secret = slack_client_secret
        if not self.slack_client_secret:
            raise SyntaxError('Missing argument: slack_client_secret')


def _config_file(ctx, param, value):
    if value:
        with open(value, 'r') as f:
            data = f.read()
            return Config(**json.loads(data))
    return None


@click.command(context_settings=context)
@click.option('-u', '--user-name', help='Google Play Username')
@click.option('-p', '--password', help='Google Play Password', hide_input=True)
@click.option('-t', '--slack-token', help='Slack App Token', hide_input=True)
@click.option('-id', '--slack-client-id', help='Slack App Client Id', hide_input=True)
@click.option('-s', '--slack-client-secret', help='Slack App Client Secret', hide_input=True)
@click.option('--config-file', type=click.Path(exists=True, dir_okay=False), callback=_config_file, is_eager=True,
              help='JSON file specifying values for the command line options')
def party_queue(user_name, password, slack_token, slack_client_id, slack_client_secret, config_file):
    print('Loading...')
    config_file = config_file or Config(user_name, password, slack_token, slack_client_id, slack_client_secret)
    sc = PartyQueueBot(config_file)
    sc.start_real_time_messaging()
