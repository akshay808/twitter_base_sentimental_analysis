from twitter import *

import sys
import csv

latitude = 18.5301802	# geographical centre of search
longitude = 73.8451041	# geographical centre of search
max_range = 1 			# search range in kilometres
num_results = 10		# minimum results to obtain
outfile = "output.csv"



consumer_key = "YqNDEh4hARqQQx696yfNhbnXI"
consumer_secret = "N5twijhTIAeO0kuPIqgtXF3OxmJUb20CDKEVL920LvTFd65GAN"
access_key = "704396968613666816-KnUKpcmHtfDIzcY91WR4U64YVULICgc"
access_secret = "duOjLfto56GqzakEAEnWjTLQgbk6uJDCPsfXgaf6cxims"


# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		        auth = OAuth(access_key,access_secret,consumer_key,consumer_secret))

#-----------------------------------------------------------------------
# open a file to write (mode "w"), and create a CSV writer object
#-----------------------------------------------------------------------
csvfile = file(outfile, "w")
csvwriter = csv.writer(csvfile)

#-----------------------------------------------------------------------
# add headings to our CSV file
#-----------------------------------------------------------------------
row = [ "user", "text", "latitude", "longitude" ]
csvwriter.writerow(row)

#-----------------------------------------------------------------------
# the twitter API only allows us to query up to 100 tweets at a time.
# to search for more, we will break our search up into 10 "pages", each
# of which will include 100 matching tweets.
#-----------------------------------------------------------------------
result_count = 0
last_id = None
while result_count <  num_results:
	#-----------------------------------------------------------------------
	# perform a search based on latitude and longitude
	# twitter API docs: https://dev.twitter.com/docs/api/1/get/search
	#-----------------------------------------------------------------------
	
	query = twitter.search.tweets(q = "", geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count = 100, max_id = last_id)

	for result in query["statuses"]:
		#-----------------------------------------------------------------------
		# only process a result if it has a geolocation
		#-----------------------------------------------------------------------
		
		if result["geo"]:
			user = result["user"]["screen_name"]
			text = result["text"]
			text = text.encode('ascii', 'replace')
			latitude = result["geo"]["coordinates"][0]
			longitude = result["geo"]["coordinates"][1]

			# now write this row to our CSV file
			row = [ user, text, latitude, longitude ]
			csvwriter.writerow(row)
			result_count += 1
			
		last_id = result["id"]

	#-----------------------------------------------------------------------
	# let the user know where we're up to
	#-----------------------------------------------------------------------
	print "got %d results" % result_count

#-----------------------------------------------------------------------
# we're all finished, clean up and go home.
#-----------------------------------------------------------------------
csvfile.close()

print "written to %s" % outfile