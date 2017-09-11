# from slack_interface import slack_interface
# from twitter_ingest import twitter_ingest
# from database import message
from slack_interface import slack_interface
import os
from textblob.classifiers import NaiveBayesClassifier
import time
from database_interface import database_interface

TRAINING_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../train.csv")
)


class LogicProc:
    def __init__(self, twitter_api, bot_mode=False):
        self.bot_mode = bot_mode
        self.twitter_api = twitter_api
        print("Using training file: {}".format(TRAINING_FILE))
        with open(TRAINING_FILE) as train_set:
            self.spam_classifier = NaiveBayesClassifier(train_set, format=None)
        self.slack_client = slack_interface.SlackInterface()
        self.message_queue = []
        self.db_interface = database_interface.DatabaseInterface()
        self.run_loop()

    def run_loop(self):
        while True:
            if self.message_queue != []:
                self.proc_messages
            else:
                time.sleep(3)

    def add_new_message(self, msg, source):
        self.message_queue.append({'source': source, 'message': msg})

    def proc_messages(self):
        for msg in self.message_queue:
            if msg['source'] == 'twitter':
                if self.is_spam(msg['message'].text) is False:
                    self.post_to_slack(msg)
                    self.store_message([msg['message'], False])
                else:
                    self.store_message([msg['message'], True])
            self.message_queue.remove(msg)

    def is_spam(self, message_text):
        if self.spam_classifier.classify(message_text) == 'neg':
            return False
        else:
            return True

    def bayesian_search(self, query):
        results = self.api.search(query)
        filtered_results = [r for r in results if self.is_spam(r.text) == 0]
        return filtered_results

    def post_to_slack(self, msg):
        if self.bot_mode is True:
            self.slack_client.api_call(
                "chat.postMessage",
                channel="@altuspresssec",
                text=msg
            )

    def poll_slack_reactions(self):
        pass

    def store_messages(self, message):
        self.db_interface.add(message)
    def retrieve_message(self, msg):
        pass
    def message_exists(self, msg):
        pass

    def discover_search_terms(self, bounding_box, hashtags):
        '''Find new relevant search terms based on incoming messages.

        Given a geographical area and a list of hashtags, return a dictionary of lists
        of new hashtags, specific locations within the geographical area, and n-grams
        which represent significant events occuring within the geographical areas or related
        to the list of input hashtags.'''
        pass
    def find_active_locations(self, bounding_box):
        '''Find areas within the bounding box which have a high volume of tweets.'''
        pass

# 1. search for potential sos
#     -search most common hashtags and n-grams
#     -alert hashtag specific
# 2. Filter / Detect
#     -filter useless hashtag announcements "Prayers for Irma! Use #IrmaSoS"
#     -filter outside the geobounds
#     -filter duplicates
#     -bayesian filter
# 3. Relay
#     -Write sos to file
#     -Post to Slack
