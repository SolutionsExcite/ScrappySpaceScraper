# ScrappySpaceScraper 

Project to get all data from the website stfc.space to utilize in ZeetoSpace upcoming beta launch.  The data from this website, represents all the meta information about everything the star trak fleet command.  This will allow me to attach the beta release of battle logs analysis to give users a more data rich experience.

The project currently only includes the grabbing of data for ships.  All other sections utilize exact same format which means it will be utilizing existing code for slightly different search params.

The way this project gathers data is not through screen scraping.  Scraping a websites requires manually selecting for each data item individually and then transforming into objects.  This is also much more code intensive in single page applications with AJAX requests.  Instead, I am utilizing what the website already provides, cache storage.  Cache storage is utilizing in many single page applications to cache responses from the API to prevent repeatedly getting data.  This data also is provided in a much more usuable structured format.

This app goes to all the pages with data desired, forcing it to load onto the local computers cache storage.  Once that is done, the final step will be for the program to grab the local cache files, filtering out the ones without data, stringing out the non json text, parsing, and piecing back together the relationships by their linked IDs.

In the end, the core operation is get some form of structured data and transform it into the desired structure for permanent storage in the database enabling the ability to run explorative data anyalsis on it utilizing machine learning techniques to see if there are any hidden correlations in the data that are not readily apparant.  If there are none, the data is still useful for known correlations.
 
