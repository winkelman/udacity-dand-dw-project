
# Data Wrangling and MongoDB

This is the second project for the Data Analyst Nanodegree and accompanies the [Data Wrangling with MongoDB](https://www.udacity.com/course/data-wrangling-with-mongodb--ud032) course from Udacity.  In this project we use data munging techniques to thoroughly audit and clean map data from an area of the world that we are interested. The clean map data is then imported to a NoSQL database and further explored.

The map data is from the open source https://www.openstreetmap.org which often has data quality issues because it is user generated. OpenStreetMap data is stored as XML and Python was used to clean and convert the data to JSON format. The clean JSON file was then imported into MongoDB and queries were run from the command line to explore the data. Finally, a report was compiled to detail problems encountered in the map, give an overview of the cleaned data, and propose other ideas about the dataset.

The map area chosen for the project was the [Guadalajara Metropolitan Area](https://en.wikipedia.org/wiki/Guadalajara_Metropolitan_Area) in the state of Jalisco, Mexico. The OpenStreetMap area can be found [here](http://www.openstreetmap.org/export#map=10/20.6771/-103.3477) and the map's complete dataset can be downloaded through the Overpass API [here](http://overpass-api.de/api/map?bbox=-103.8606,20.3639,-102.8348,20.9884).

The raw .osm XML file can be cleaned and converted to JSON by running `process_data.py`, and the clean JSON file can be imported to MongoDB with `import_mongo.py`
