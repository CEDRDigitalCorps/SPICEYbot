# from slack_interface import slack_interface
# from twitter_ingest import twitter_ingest
# from database import message
from slack_interface import slack_interface
import os
from textblob.classifiers import NaiveBayesClassifier
import time
from threading import Timer
from database_interface import database_interface
import infinite_timer
import time

class LogicProc:
    def __init__(self, preclassified_file, channel, slack_token):

        if os.path.isfile(preclassified_file)==False:
            print('"' + preclassified_file + '" does not exist!')

        with open(preclassified_file,'r') as train_set:
            self.spam_classifier = NaiveBayesClassifier(train_set, format=None)
        self.slack_client = slack_interface.SlackInterface(slack_token)
        self.message_queue = []
        self.last_message_ts = None
        self.channel = channel
        #self.db_interface = database_interface.DatabaseInterface()

        self.update_classifer_from_slack(self.channel)

        self.check_twitter_msgs = infinite_timer.InfiniteTimer(5.0, self.proc_messages)
        self.check_slack_msgs = infinite_timer.InfiniteTimer(60.0, self.update_classifer_from_slack, self.channel)
        self.check_twitter_msgs.start()
        self.check_slack_msgs.start()


    def add_new_message(self, msg, source):
        """
        Callback from Twitter when there is a new message
        @param msg     The Twitter message, with all its attributes
        @param source  Where the message came from.  Right now should only be 'twitter'
        """
        self.message_queue.append({'source': source, 'message': msg})

    def proc_messages(self):
        for msg in self.message_queue:
            if msg['source'] == 'twitter':
                message = msg['message']
                if self.quality_filter(message.text) == True:
                    self.post_to_slack(message, self.channel)
                    self.store_message(message, True)
                else:
                    self.store_message(message, False)
            self.message_queue.remove(msg)

    def run_loop(self):
        """
         Not sure what this was originally intended to do..
         now it runs proc_messages once a second
        """
        while True:
           # sleep between polling queue
           time.sleep(1)

    def quality_filter(self, message_text):
        # -filter useless hashtag announcements "Prayers for Irma! Use #IrmaSoS"
        # -filter outside the geobounds
        # -filter duplicates
        # -bayesian filter
        result = self.spam_classifier.classify(message_text)
        if result == 'neg':
            return False
        else:
            return True

    def post_to_slack(self, msg, channel):
        self.slack_client.post_message(msg.text, channel)

    def update_classifer_from_slack(self, channel):
        slack_msgs = self.slack_client.get_slack_reactions(channel, self.last_message_ts)
        if len(slack_msgs)>0:
            self.last_message_ts = slack_msgs[-1]['ts']
        bayesian_update_data = []
        for m in slack_msgs:
            user_feedback = self.is_slack_reaction_pos(m['reactions'])
            text = m['text']
            if user_feedback == None:
                pass
            elif user_feedback == True:
                bayesian_update_data.append((text, 'pos'))
            elif user_feedback == False:
                bayesian_update_data.append((text, 'neg'))
        # update for better results
        print 'updating...'
        self.spam_classifier.update(bayesian_update_data)
        print 'done...'

    def is_slack_reaction_pos(self,reactions):
        for t in reactions:
           name = t['name']
           if name == '-1':
               return False
           if name == '+1':
               return True
        return None


    def store_message(self, message, filter_classification):
        pass

    def bayesian_search(self, query):
        results = self.api.search(query)
        filtered_results = [r for r in results if self.is_spam(r.text) == 0]
        return filtered_results
