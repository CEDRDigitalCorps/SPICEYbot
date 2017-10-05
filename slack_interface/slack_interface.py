from slackclient import SlackClient
import os

class SlackInterface:
    def __init__(self, slack_token):
        self.slack = SlackClient(slack_token)

    def post_message(self, msg, channel):
        self.slack.api_call("chat.postMessage", channel=channel, text=msg)

    def get_slack_reactions(self, channel, last_message_ts=None):
        if last_message_ts == None:
            history = self.slack.api_call("channels.history", channel=channel)
            if 'ok' in history and history['ok'] == False:
                print 'Could not get channel history'
                messages = []
            else:
                messages = history['messages']
        else:
          messages = self.slack.api_call("channels.history", channel=channel, \
            oldest=self.last_message_ts, inclusive=True)['messages']
        for m in messages:
            reactions = self.slack.api_call("reactions.get", full="true", channel=channel, timestamp=m['ts'])
            m['reactions'] = reactions['message']['reactions']
        return messages

