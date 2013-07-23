######
#
#   CODE IS DEPRECIATED. PARSE_TWEET IS NOT TWITTER API 1.1 COMPLIANT AND ENVIRONMENT SETTINGS HAVE CHANGED IN 10.1
#
# By: cdweidem@usc.edu
# App: Use Twitter's API to query geolocated tweets and then store them in a geodatabase
# Input: Lat, long, search string, and search radius
# output: database with tweets, locations, user, etc.
# Thanks to sixohsix, geospatialpython, and rnz0 for their examples, code, and help.
#
#   !!!!!!!!!!WARNING!!!!!!!!!!!
#
#   Twitter API 1 has been depreciated. This code no longer works. Code will be updated.
#
#   !!!!!!!!!!WARNING!!!!!!!!!!!
#
######

import arcpy
import urllib2
import json

#set some defaults for the search
query = arcpy.GetParameterAsText(0)
searchlat = arcpy.GetParameterAsText(1)
searchlong = arcpy.GetParameterAsText(2)
radius = arcpy.GetParameterAsText(3)

#set up environment. Change workspace if you wish to store these elsewhere
Twitter = "Twitter.gdb"
Tweets = "Tweets"
WGS84 = os.path.join(installDir,r"Coordinate Systems/Geographic Coordinate Systems/World/WGS 1984.prj")
arcpy.env.workspace = "C:/" 

 
def db_set():

    FIELDS = [
        ['tweet_id', 'TEXT','NON_NULLABLE','REQUIRED'],
        ['text','TEXT','NON_NULLABLE','REQUIRED'],
        ['created_at','TEXT','NON_NULLABLE','REQUIRED'],
        ['query','TEXT','NON_NULLABLE','REQUIRED'],
        ['lat','FLOAT','NON_NULLABLE','REQUIRED'],
        ['lon','FLOAT','NON_NULLABLE','REQUIRED'],
        ['from_user','TEXT','NON_NULLABLE','REQUIRED'],
        ['from_user_name','TEXT','NON_NULLABLE','REQUIRED'],
        ['city','TEXT','NON_NULLABLE','NON_REQUIRED']
    ]

    try:
        arcpy.CreateFileGDB_management(arcpy.env.workspace, Twitter)
    except:
        pass
    try:
       arcpy.Createfeatureureclass_management(Twitter,Tweets,"POINT","#","DISABLED","DISABLED",WGS84)
    except:
        pass
    for field_name, field_type, NULLABLE, REQUIRED in FIELDS:
        try:
            arcpy.AddField_management("Twitter.gdb/Tweets",field_name, field_type, "#", "#", "#", "#", NULLABLE, REQUIRED,"#")
        except:
            pass
   
def parse_tweets(query, searchlat, searchlong, radius):
    url = "http://search.twitter.com/search.json?q="+query+"&include_entities=true&geocode="+searchlat+","+ searchlong + "," + radius
    tweet_data_json = urllib2.urlopen(url).read()
    tweet_data = json.loads(tweet_data_json)
 
    results = []
    for tweet in tweet_data['results']:
        results.append([
            tweet['id'],                # 0
            tweet['text'],              # 1    
            tweet['created_at'],        # 2
            query,                      # 3
            tweet['latitude']           # 4
            tweet['longitude']          # 5 
            tweet['from_user'],         # 6
            tweet['from_user_name']     # 7
        ])
 
    return results
 
 
def write_tweets():
  
    insert_cursor = arcpy.Insertinsert_cursorsor("Twitter.gdb/Tweets")
    Arcpy_Array = arcpy.Array()
    point = arcpy.Point()

    for tweet in parse_tweets(query, str(searchlat), str(searchlong)):
        
        feature = insert_cursor.newRow()
        point.ID = long(tweet[0])
        point.Y = tweet[4]
        point.X = tweet[5]
        
        feature.setValue('tweet_id', str(tweet[0]))
        feature.setValue('text', tweet[1])
        feature.setValue('created_at', tweet[2])
        feature.setValue('query', tweet[3])
        feature.setValue('lat', tweet[4])
        feature.setValue('lon', tweet[5])
        feature.setValue('from_user', tweet[6])
        feature.setValue('from_user_name', tweet[7])
        feature.setValue('city', city_name)
        Arcpy_Array.add(point)
        feature.shape = Arcpy_Array[0]
        insert_cursor.insertRow(feature)
        Arcpy_Array.removeAll()
        
    del insert_cursor
        
if __name__ == "__main__":
    db_set()
    write_tweets()
