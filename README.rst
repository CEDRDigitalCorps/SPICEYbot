Social Precision Insight of Crowdsourced EmergencY - SPICEY
===========================================================

Setup
-----

.. code-block:: bash

   $ pip install -r requirements.txt


Configuration
-------------

Twitter and Slack credentials are needed, create a ``settings.ini`` file with the following contents;

.. code-block:: bash

   [settings]
   TWITTER_KEY=<your-twitter-key>
   TWITTER_SECRET=<your-twitter-secret>
   TWITTER_ACCESS_TOKEN=<your access token>
   TWITTER_ACCESS_TOKEN_SECRET=<your access secret>
   SLACK_TOKEN=<your-slack-token>
   SLACK_CHANNEL=<channel name or id>
   DATABASE_NAME=<db-table>
   DATABASE_HOST=
   DATABASE_TABLE=<db-table>
   DATABASE_USER=<db-user>
   DATABASE_PASSWORD=
   GEOLOCATION_BB=<x1,y1,x2,y2>
   PRECLASSIFIED_FILE=<train.csv>

Replacing the ``<*>`` strings with relevant keys, secrets, and tokens

To get a Twitter Key go to https://apps.twitter.com/ and create an app.  Use the
KEY and SECRET provided.  When SPICEY first tries to connect, it will open a browser
window to authorize the application.  Once authorized SPICIE will print your TOKEN
and TOKEN_SECRET.  Save this and put them in the settings.ini

To get a SLACK_TOKEN goto https://api.slack.com/apps and add a new app.
Running
-------

  Run python spicey.py
  After about a minute tweets will be posted to the channel.  Tag correct tweets
  with :+1: and incorrect tweets with :-1:.  The bot will come back through and retrain
  base on the recommendation.

