from slackclient import SlackClient
import os

class SlackInterface:
    def __init__(self):
        slack_token = os.environ['SLACK_TOKEN']
        self.sc = SlackClient(slack_token)

    def post_to_slack(self, msg):
        self.sc.api_call(
          "chat.postMessage",
          channel="@altuspresssec",
          text=msg
        )

    def poll_slack_reactions(self):
        new_reacts_thing = {}
        messages = sc.api_call(
          "search.all",
          query="from:TweetBot"
        )['messages']['matches']
        for i in messages:
            reacts = sc.api_call(
              "reactions.get",
              full="true",
              channel="C70127ZL1",
              timestamp=i['ts']
            )['message'].get('reactions', [])
            new_reacts_thing[i['ts']] = []
            for a in reacts:
                new_reacts_thing[i['ts']].append({a['name']: a['count']})
        return new_reacts_thing
