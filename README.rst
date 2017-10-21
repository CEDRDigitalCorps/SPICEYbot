Social Precision Insight of Crowdsourced EmergencY - SPICEY
===========================================================

Setup
-----

Create a virtual environment for the project.

.. code-block:: bash

  $ virtualenv spicey_env -p <path to Python 3 on your machine>

To find out the path to Python 3, run these commands:

.. code-block:: bash

  $ python3 -v
  $ python -v # if the python3 command doesn't return anything

You might have to install Python 3 if you haven't already.

Once you have the virtual environment made, activate it.

.. code-block:: bash

  $ source spicey_env/bin/activate

Install the requirements in the activated virtual environment.

.. code-block:: bash

   $ pip install -r requirements.txt

Remember to reactivate the virtual environment any time you work on the project in the future.

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
