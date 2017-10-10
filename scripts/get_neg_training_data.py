import csv

query = "Irma -filter:retweets AND -filter:replies"
from twitter_ingest import twitter_ingest
twitter_api_consumer_key = 'lR8ZmpHW7O0DoCLmBBELWL96G'
twitter_api_consumer_secret = 'aOJXxFnWNT5baCL1f6ujvlvNjJ0jUAGlp0mguJFo49zwzdKpRH'
twitter_interface = twitter_ingest.TwitterIngest(twitter_api_consumer_key, 
									twitter_api_consumer_secret)

results = twitter_interface.api.search(query, result_type='recent')
cur_max_id = results[-1].id
print len(results)
with open('neg.csv','wb') as o:
  w = csv.writer(o, delimiter=',')
  for i in range (0, 10):
    search_results = twitter_interface.api.search(query, count=100, result_type='recent', max_id=cur_max_id)
    for r in search_results:       
       w.writerow( [unicode(r.text).encode('utf8'), 'neg']  )
    print(search_results[0].created_at)
    print(search_results[-1].created_at)
    print len(search_results)
    cur_max_id = search_results[-1].id
    results.extend(search_results)
    print len(results)