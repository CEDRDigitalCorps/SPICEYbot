from slackclient import SlackClient
import os

slack_token = os.environ['SLACK_TOKEN']
sc = SlackClient(slack_token)

def say(msg):
    print(sc.api_call(
      "chat.postMessage",
      channel="@izwick-schachter",
      text=msg
    ))

say("Hi")
