import tweepy
import webbrowser
import csv
from logic_proc import logic_proc

class TwitterIngest():
    def __init__(self, consumer_key, consumer_secret, preclassified_file=None, \
        geolocation_bounding_box=None, receiver_class=None, access_token=None, access_token_secret=None):
        print 'Starting CrowdRescue Twitter Autodiscovery Search Assistant and Bot a.k.a. SPICEY...'
        print 'Starting API...'
        self.api = None
        self.preclassified_file = None
        self.geolocation_bounding_box = None
        consumer_key = consumer_key
        consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        try:
            self.authenticate(
                consumer_key, #consumer_key
                consumer_secret) #consumer_secret
            print 'Success! Authenticated as User ' + self.api.me().name
        except Exception as e:
            print "Authentication Failed. " + str(e) + " Exiting..."
            raise
        print 'API connection established. Establishing Search and Starting scrapers...'
        self.stream_scraper = TwitterStreamScraper(receiver_class, self.api, restart=self._restart)
        self.scrapper       = None
        if preclassified_file != None:
           self.set_target(preclassified_file,geolocation_bounding_box)

    def authenticate(self, consumer_key, consumer_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        if self.access_token is None:
            # Get Access Token
            try:
                redirect_url = auth.get_authorization_url()
                print redirect_url
            except tweepy.TweepError:
                print 'Error! Failed to get request token.'
                quit()
            try:
                print "Please go to this URL and permission the application."
                webbrowser.open(redirect_url)   
                verifier = raw_input('Verifier Code:')
                auth.get_access_token(verifier)
                print "Verification successful. Access Token: " + str(auth.access_token)
                print "Access Token Secret: " + str(auth.access_token_secret)
            except tweepy.TweepError:
                print 'Error! Failed to get access token.'
        else:
            print "Found stored Access Token. Authenticating..."
            auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)
        print 'Testing API connection...'
        print self.api.get_status('906653703402250242').text
        print "Building Twitter Search Query..."
        

    def _restart(self):
        """
        Start streaming tweets
        """
        self.set_target(self.preclassified_file, self.geolocation_bounding_box)


    def set_target(self, preclassified_file, geolocation_bounding_box):
        self.preclassified_file = preclassified_file
        self.geolocation_bounding_box = geolocation_bounding_box
        user_list, hashtag_list, phrase_list = self.build_query(
            preclassified_file, geolocation_bounding_box)

        # need to restart and the query target has changed
        self.start_monitoring(geolocation_bounding_box, user_list, hashtag_list, phrase_list)

    def build_query(self, preclassified_file, geolocation_bounding_box):
        if preclassified_file is None:
            return  [],[],[]
        preclassified_tweets = []
        #Get the text of all tweets from the preclassified file.
        with open (preclassified_file, 'rb') as csvfile:
            csv_reader = csv.DictReader(csvfile, fieldnames=['text','pos'])
            for tweet in csv_reader:
                preclassified_tweets.append(tweet)
        #Find all hashtags within the tweets in the file
        user_list = self.discover_users(preclassified_tweets)
        hashtag_list = self.discover_hashtags(preclassified_tweets)
        phrase_list = self.discover_phrases(preclassified_tweets)
        return user_list, hashtag_list, phrase_list

    def discover_users(self, tweets):
        result = []
        for t in tweets:
            user = t.get('user',None)
            if user!=None:
                result.append(user)
        return result

    def discover_hashtags(self, tweets):
        discovered_hashtags = []
        for t in tweets:
            discovered_hashtags.extend(self.extract_hashtags(t))
        return list(set(discovered_hashtags))

    def extract_hashtags(self,tweet):
        text = tweet['text'].encode('utf8')
        if tweet['pos'] == 'neg':
            return []
        # only hash tags
        # and skip '#' since its not a hash tag
        # and skip just numbers, as its probably part of an address
        raw_tags = [part for part in text.split() if part.startswith('#') \
            and len(part)>1 \
            and unicode(part[1:],'utf8').isnumeric()==False ]
        return list(set(part.replace(',', '').replace('.', '')  for part in raw_tags))
            

    def discover_phrases(self, tweets):
        return []

    def start_monitoring(self, geolocation_bounding_box, user_list, hashtag_list, phrase_list):

        print "Starting twitter thread"
        print(hashtag_list + phrase_list)

        if self.scrapper != None:
           self.scraper.disconnect()

        # need to make a new scrapper, as calling 'filter'
        # starts up a thread, and there is NO WAY (currently) to
        # wait for it to exit.
        # Instead, call 'disconnect' on the old thread and let it
        # get GC'd, while a new thread is started below
        
        # make new object
        self.scraper = tweepy.Stream(
           auth=self.api.auth,
           listener=self.stream_scraper)

        # start the new thread
        self.scraper.filter(
            follow=user_list,
            track=hashtag_list + phrase_list,
            locations=geolocation_bounding_box,
            async=True)

class TwitterStreamScraper(tweepy.StreamListener):
    def __init__(self, receiver_class, api, restart=None):
        tweepy.StreamListener.__init__(self,api)
        self.receiver_class = receiver_class
        self.restart = restart
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False
    def on_status(self, status):
        if not status.text[0:2] == "RT":
            self.receiver_class.add_new_message(status, 'twitter')

    def on_exception(self, ex):
        import traceback
        traceback.print_exc()
        if self.restart != None:
            self.restart()

if __name__ == '__main__':
    twitter_connection = TwitterInterface()
