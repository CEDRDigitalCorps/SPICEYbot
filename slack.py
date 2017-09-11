from slackclient import SlackClient
import os

slack_token = os.environ['SLACK_TOKEN']
sc = SlackClient(slack_token)

def get_reacts(msg):
    return sc.api_call(
      "reactions.get",
      full="true",
      channel="C70127ZL1",
      timestamp=msg
    )['message'].get('reactions', [])

def smart():
    messages = sc.api_call(
      "search.all",
      query="from:TweetBot"
    )['messages']['matches']
    for i in messages:
        print(i['text'])
        reacts = get_reacts(i['ts'])
        for a in reacts:
            print("Got "+str(a['count'])+" "+str(a['name'])+"s")


def say(msg):
    print(sc.api_call(
      "chat.postMessage",
      channel="#twitterautosearch",
      text=msg
    ))

smart()
#say("hi")
