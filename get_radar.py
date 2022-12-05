import shutil
import boto3
import botocore
from botocore.client import Config
from datetime import datetime
import os

#
# Start by defining some basic information about this configuration
# As per coding standards define locations for everything
#

BASE_DIR = './radar/'

#
# Define the radar names to archive
#

site_names = ['KENX','KBOX']

#
# Determine if this a clockqueue run or a archive
# rum
#

now = input("Use current data or get archive [c/a]? ")

#
# Archive run get the date/time for the get call
#

if now == "a":

    #
    # Get the date/time string
    #

    a = input("Enter the date/time string yyyy-mm-dd-hh ")

    year = a[0:4]        # year
    month = a[5:7]       # month
    day = a[8:10]        # day
    hour = a[11:13]      # hour 

else:
    
   #
   # Clockqueue run get and decode the time for this run
   #

   date = str(datetime.utcnow())
   
   year = date[0:4]
   month = date[5:7]
   day = date[8:10]
   hour = date[11:13]

#
# Insure that I have some place to store the data
#

for site in site_names:
    dest = BASE_DIR+"/"+site+"/"+year+month+day+"/"+hour
    if not os.path.exists(dest):
        os.makedirs(dest)

#
# Open up the link 
#

s3 = boto3.resource('s3', config=Config(signature_version=botocore.UNSIGNED,
                                        user_agent_extra='Resource'))

bucket = s3.Bucket('noaa-nexrad-level2')

#
# Build the site independent part of the Prefix string
#

string = year + "/" + month + "/" + day + "/"

for site in site_names:
    prefix = string + site + "/" + site + year + month + day + "_" + hour
    for obj in bucket.objects.filter(Prefix=prefix):
        with open(obj.key.split('/')[-1],'wb') as outfile:
            shutil.copyfileobj(obj.get()['Body'],outfile)
            dest = BASE_DIR+"/"+site+"/"+year+month+day+"/"+hour+"/"

            #
            # Because the outfile isn't a string and contains alot
            # of cruft we don't need
            #

            temp = str(outfile)
            src = temp[26:49]
            
            #
            # If I already downloaded the file remove the outfile
            # if not copy the file
            #
            
            if os.path.isfile(dest+src) and os.access(dest+src, os.R_OK):

                if os.path.isfile(dest+src) and os.access(dest+src, os.R_OK):
                    print("File exists and is readable")
  
            else:
                if os.path.isdir(dest):
                    shutil.move(src,dest)
