import tweepy
from logic_proc import logic_proc
class TwitterIngest():
    def __init__(self, consumer_key, consumer_secret, preclassified_file, \
        geolocation_bounding_box, receiver_class, access_token=None, access_token_secret=None):
        print 'Starting CrowdRescue Twitter Autodiscovery Search Assistant and Bot a.k.a. SPICEY...'
        print 'Starting API...'
        self.api = None
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
        print 'API connection established. Establishing Search and Starting scrapers...'
        self.stream_scraper = TwitterStreamScraper(receiver_class)
        self.scraper = tweepy.Stream(
           auth=self.api.auth,
           listener=self.stream_scraper)
        self.set_target(preclassified_file)

    def authenticate(self, consumer_key, consumer_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        if self.access_token == '':
            # Get Access Token
            try:
                redirect_url = auth.get_authorization_url()
                print redirect_url
            except tweepy.TweepError:
                print 'Error! Failed to get request token.'
                quit()
            verifier = raw_input('Verifier Code:')
            try:
                print "Please go to this URL and permission the application."
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
        selfl.set_target

    def set_target(self, preclassified_file, geolocation_bounding_box,):
        user_list, hashtag_list, phrase_list = self.build_query(
            geolocation_bounding_box, preclassified_file)
        self.start_monitoring(geolocation_bounding_box, user_list, hashtag_list, phrase_list)

    def build_query(self, preclassified_file, geolocation_bounding_box):
        preclassified_tweets = []
        #Get the text of all tweets from the preclassified file.
        with open (preclassified_file, 'rb') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for tweet in csv_reader:
                preclassified_tweets.append(tweet) 
        #Find all hashtags within the tweets in the file
        user_list = self.discover_users(preclassified_tweets)
        hashtag_list = self.discover_hashtags(preclassified_tweets)
        phrase_list = self.discover_phrases(preclassified_tweets)
        return user_list, hashtag_list, phrase_list
        
    def discover_users(self, tweets):
        return t['user'] for t in tweets

    def discover_hashtags(self, tweets):
        discovered_hashtags = []
        for t['text'] in tweets:
            discovered_hastags.extend(self.extract_hashtags(t))
        return list(set(discovered_hastags))

    def extract_hashtags(tweet):
        return list(set(part.replace(',', '').replace('.', '') \
            for part in tweet.split() if part.startswith('#')))

    def discover_phrases(self, tweets):
        return []

    def start_monitoring(self, geolocation_bounding_box, user_list, hashtag_list, phrase_list):
        self.scraper.filter(
            follow=user_list,
            track=hashtag_list.extend(phrase_list),
            locations=geolocation_bounding_box,
            async=True)

class TwitterStreamScraper(tweepy.StreamListener):
    def __init__(self, receiver_class):
        super(tweepy.StreamListener, self).__init__()
        self.receiver_class = receiver_class
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False
    def on_status(self, status):
        if not status.text[0:2] == "RT":
            self.receiver_class.add_new_message(status, 'twitter')


if __name__ == '__main__':
    twitter_connection = TwitterInterface()
