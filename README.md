# Friends of Chicago River: web tool

This is a web tool built with python Flask to **process** and **visualize** satellite images.

## 1. Process

To process a raster data, a folder of a TIF file with its attribute files has to be zipped. Select this zip and click "Process" button. The script will then:

1. calculates NDVI (vegetative health)
2. detect phragmites
3. clustering vegetation

After it is done, user can download the processed TIF file (contains all information above) and visualize the TIF. 

![process and visualize th file](https://github.com/nmonarizqa/focr/blob/master/demo/demo1.gif?raw=true)

## 2. Visualize

This can be accessed right after process 1 done, or by uploading a zip file containing a single processed TIF file. 
The visualization tool will display four images in four different tabs:

1. Phragmites (blue --> detected phragmites)
2. Cluster (different color --> different cluster)
3. Vegetative health (red --> poor, yellow --> fair, green --> good)
4. Original (original pictures)

Click anywhere on the image to display the latitude and longtiude on the top right location box.

![process and visualize th file](https://github.com/nmonarizqa/focr/blob/master/demo/demo2.gif?raw=true)

## Using the tool

You can access the web version at [https://focrproject.cuspuo.org](https://focrproject.cuspuo.org) or run / install it locally following the below instructions.

### Installation

#### Running using docker:

> Make sure you are running docker v17.0 or higher.

1. Open terminal and type `docker run -p 5000:5000 mohitsharma44/focr`

2. Go to your browser and visit `http://localhost:5000`

#### Installing locally:

To install this web tool, make sure to have [python2.7+](https://www.python.org/) and pip (or pip3) installed.

This web tool requires GDAL, therefore please install GDAL dependencies prior to installation. This web tool
has been tested with gdal v2.2.2 and with v2.3.1

Debian/ Ubuntu Users can install gdal2 by adding unstable version of gis PPA
``` shell
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt install libgdal20
# based on whether you are using python(2) or python3
sudo apt install python-gdal # or python3-gdal
```

Mac Users can install using brew
``` shell
brew tap osgeo/osgeo4mac && brew tap --repair
brew install gdal2
```

After all installed, download and extract (or git clone) this repo to the desired destination.
Install all the requirements by typing `sudo pip install -r requirements.txt` or `sudo pip3 install -r requirements.txt`.

Once everything installed, type `python app.py` or `python3 app.py`, open browser, and go to the
http://localhost:5000

### Credit

Thanks to Greg Dobler of NYU CUSP and his team for the image processing scripts used in this project. Link [here](https://github.com/gdobler/carve)
