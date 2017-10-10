from twitter_ingest import twitter_ingest
from logic_proc import logic_proc
from decouple import config

class Spicey:

    def __init__(self):
        twitter_api_consumer_key = config("TWITTER_KEY", default="")
        twitter_api_consumer_secret = config("TWITTER_SECRET", default="")
        access_token = config("TWITTER_ACCESS_TOKEN", default=None)
        access_token_secret = config(
            "TWITTER_ACCESS_TOKEN_SECRET",
            default=None
        )
        slack_token = config("SLACK_TOKEN", default="")
        preclassified_file = config("PRECLASSIFIED_FILE", default=None)
        channel = config("SLACK_CHANNEL", default="")
        geolocation_bounding_box = config("GEOLOCATION_BB", default="")

        self.logic_processing= logic_proc.LogicProc(preclassified_file, channel, slack_token)

        self.twitter_interface = twitter_ingest.TwitterIngest(twitter_api_consumer_key,
                                            twitter_api_consumer_secret, preclassified_file,
                                            geolocation_bounding_box, 
                                            self.logic_processing,
                                            access_token=access_token,
                                            access_token_secret=access_token_secret
                   )
    def set_target(self, preclassified_file, bounding_box):
        self.twitter_interface.set_target(preclassified_file, bounding_box)

    def prepare_run(self):
        """Call before run_bot
        """
        pass

    def run_bot(self):
        """
        Main loop for bot. does not return
        """
        try:
            self.logic_processing.run_loop()
        finally:
            quit()

if __name__ == '__main__':
    spicey = Spicey()
    puerto_rico_bb = [17.7307, -68.1109, 18.6664,-65.0914]
    spicey.set_target('preclassified_pr.csv', 
                       puerto_rico_bb)
    spicey.prepare_run()
    spicey.run_bot()


#map tool
#gives longitude then latitude
#-68.1109,17.7307,-65.0914,18.6664
#gives bottom left, then top right