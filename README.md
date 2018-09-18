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

# Installation

To install this web tool, make sure to have [python2.7](https://conda.io/miniconda.html) and pip installed.

This web tool requires GDAL, therefore please install GDAL dependencies prior to installation.

After all installed, download and extract (or git clone) this repo to the desired destination. Open command prompt (or Anaconda prompt), go inside the folder by typing `cd focr` and install all the requirements by typing `pip install -r requirements.txt`.

Once everything installed, type `python app.py`, open browser, and go to the localhost address shown e.g http://127.0.0.1:5000/

### Credit

Thanks to Greg Dobler of NYU CUSP and his team for the image processing scripts used in this project. Link [here](https://github.com/gdobler/carve)
