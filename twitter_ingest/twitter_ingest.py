import tweepy

from logic_proc import logic_proc


class TwitterIngest():
    def __init__(self, consumer_key, consumer_secret, bot_mode=False, access_token=None, access_token_secret=None):
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
        if bot_mode:
            self.stream_scraper = TwitterStreamScraper()
            self.scraper = tweepy.Stream(
               auth=self.api.auth,
               listener=self.stream_scraper)
            self.start_scrapers()
        self.logic = logic_proc.LogicProc(self.api)

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

    def start_scrapers(self):
        self.search_filters()

    def search_filters(self):
        # Hashtag Gathering
        hashtag_list = self.hashtags_to_monitor()
        # Geographic Gathering
        florida_bounding_box = self.geobounds_to_monitor()
        # Phrases
        ngram_list = self.ngrams_to_monitor()

        track_list = hashtag_list.extend(ngram_list)
        self.scraper.filter(
            track=track_list,
            locations=florida_bounding_box,
            async=True)

    def hashtags_to_monitor(self):
        hashtags = ["#irmasos",
                    "#irmapetrescue",
                    "#marcoisland",
                    "#irmarescue",
                    "#IRMASOS",
                    "#sosIrma",
                    "#FLKeys",
                    "#floridakeys",
                    "#florida",
                    "#needrescue",
                    "#needhelp",
                    "#needwaterrescue",
                    "#IRMAhelp",
                    "#IrmaRescue",
                    "#irmapets",
                    "#irmapetrescue",
                    "#irmapetsos",
                    "#IRMA",
                    "#IRMA2017",
                    "#IRMAFlorida",
                    "#hurricaneIRMA",
                    "#huricaneIRMA",
                    "#hurricanIRMA",
                    "#hurrcaneIRMA",
                    "#hurracaneIRMA",
                    "#hurricaneirma2017",
                    "#irmahurricane2017",
                    "#IRMAhurricane",
                    "#IRMAhuricane",
                    "#IRMAhurrcane",
                    "#IRMAhurracane",
                    "#hurricane",
                    "#huricane",
                    "#hurican",
                    "#hurracane",
                    "#tornado",
                    "#flood",
                    "#flooded"]
        return hashtags

    def geobounds_to_monitor(self):
        # Partial Florida, focused on southern.
        geo_bounding_box = [-83.54, 24.27, -79.74, 29.13]
        return geo_bounding_box

    def ngrams_to_monitor(self):
        ngrams = []  # Add the Harvey dataset n-grams after testing.
        return ngrams

    def bayesian_search(self, query):
        return self.logic.bayesian_search(query)


class TwitterStreamScraper(tweepy.StreamListener):
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

    def on_status(self, status):
        if not status.text[0:2] == "RT":
            self.logic.add_new_message(status, 'twitter')


if __name__ == '__main__':
    twitter_connection = TwitterInterface()
