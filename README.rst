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


Running
-------

  Run python spicey.py
  After about a minute tweets will be posted to the channel.  Tag correct tweets 
  with :+1: and incorrect tweets with :-1:.  The bot will come back through and retrain 
  base on the recommendation.

Deployment
----------

The run the deployment code script on server;

.. code-block:: bash

   $ /var/www/assistsearch/app/scripts/update.sh
