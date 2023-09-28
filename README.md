# ScrappySpaceScraper
 
This program was created to iterate through pages on stfc.space to load its' data into cache since it utilizes a progressive app framework.

After the cache has been loaded by navigating to pages to scrape, the progressive web api has it stored in the web cache in messy format we will need to grab
our data from.

Once done navigating, the program will process the cache files and extract the required encoded json data.  This will then be saved into a json file
for another app to ETL to database.  Currently it is a separate c# app that runs the ETL of extracted cahce data.

In the future webdrivers will likely be removed for a slimmed down and potentiall faster/more robust approach utilizing curl requests (potentially, needs research).