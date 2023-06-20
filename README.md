# python-qgis-scripts
Repository which contains a set of scripts which can be used in the QGIS Python API to load maps and layers using different OGC webservices and API standards

For this small project, we aim to have scripts for at least the following services:

* WMS
* WMTS
* WFS
* OGC API - Features 
* OGC API - Maps* 
* OGC API - Tiles* 

*Look at the possibilities of these standards and whether they are directly supported by the python API

## How to use the script (temp)
From the python console in QGIS, just execute: `exec(open(r"path-to-repo/python-qgis-scripts/qgis-scripts.py".encode('utf-8')).read())` 

This will run the script and add a group to the current QGIS project with different layers.