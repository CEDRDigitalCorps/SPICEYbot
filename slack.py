from slackclient import SlackClient
import os

slack_token = os.environ['SLACK_TOKEN']
sc = SlackClient(slack_token)

def say(msg, chan):
    print(sc.api_call(
      "chat.postMessage",
      channel=chan,
      text=msg
    ))

say("Hi", "#twitterauthsearch)
