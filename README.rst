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
   SLACK_TOKEN=<your-slack-token>
   DATABASE_NAME=<db-table>
   DATABASE_HOST=
   DATABASE_TABLE=<db-table>
   DATABASE_USER=<db-user>
   DATABASE_PASSWORD=


Replacing the ``<*>`` strings with relevant keys, secrets, and tokens


Deployment
----------

The run the deployment code script on server;

.. code-block:: bash

   $ /var/www/assistsearch/app/scripts/update.sh
