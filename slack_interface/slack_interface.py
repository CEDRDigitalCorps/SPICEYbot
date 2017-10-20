from slackclient import SlackClient
import os

class SlackInterface:
    def __init__(self, slack_token):
        self.slack = SlackClient(slack_token)
        id = self.slack.api_call('users.identity');

    def get_channel_id(self,name):
        """
        Give the name or id of a channel
        return the id
        """
        channels = self.slack.api_call('conversations.list',types='public_channel, private_channel')
        if channels.get('ok'):
            for c in channels['channels']:
                if c['name'] == name or c['id'] == name:
                    return c['id']
        # for what ever reason, need to do this call separate
        # mpim doesnt list all members
        channels = self.slack.api_call('conversations.list',types='im')
        if channels.get('ok'):
            for c in channels['channels']:
                if c['id'] == name:
                    return c['id']
                user = self.slack.api_call('users.info',user=c['user'])
                if user['ok'] and user['user']['real_name'].lower()==name.lower():
                    return c['id']
        return None

    def post_message(self, msg, channel):
        self.slack.api_call("chat.postMessage", channel=channel, text=msg)

    def get_slack_reactions(self, channel, last_message_ts=None):
        if last_message_ts == None:
            history = self.slack.api_call("conversations.history", channel=channel)
            if 'ok' in history and history['ok'] == False:
                print 'Could not get channel history'
                messages = []
            else:
                messages = history['messages']
        else:
          messages = self.slack.api_call("conversations.history", channel=channel, \
            oldest=last_message_ts, inclusive=True)['messages']
        for m in messages:
              reactions = self.slack.api_call("reactions.get", full="true", channel=channel, timestamp=m['ts'])            
              # only look at messages from bot
              if 'bot_id' in m:
                 m['reactions'] = reactions['message'].get('reactions',[])
              else:
                 m['reactions'] = []
        return messages

