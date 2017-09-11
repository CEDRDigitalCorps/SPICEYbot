from twitter_ingest import twitter_ingest

class Spicey:

    def __init__(self, bot_mode=False):
        twitter_api_consumer_key = 'lR8ZmpHW7O0DoCLmBBELWL96G'
        twitter_api_consumer_secret = 'aOJXxFnWNT5baCL1f6ujvlvNjJ0jUAGlp0mguJFo49zwzdKpRH'
        self.twitter_interface = twitter_ingest.TwitterIngest(
            twitter_api_consumer_key,
            twitter_api_consumer_secret,
            bot_mode
        )

    def bayesian_search(self, query):
        return self.twitter_interface.bayesian_search(query)

if __name__ == '__main__':
    spicey = Spicey(bot_mode=True)
    test_search = spicey.bayesian_search('#IrmaSOS')
    for t in test_search:
        print t.text
