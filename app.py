import os
from flask import Flask, request, redirect, url_for,render_template, jsonify, make_response, abort, send_file,flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from extract import extract
import glob
import utils
import numpy as np
from ph_scan import PhScan
from phrag_map import phrag_map
from utils import cluster_ph, write_tif
import sys
import zipfile
import gdal
import matplotlib.pyplot as plt
import pandas as pd
import time
import shutil
import pickle

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def reset():
    files = os.listdir("tmp")
    to_be_removed = [x for x in files if("zip" in x)|("TIF" in x)]
    if len(to_be_removed)>0:
        for f in to_be_removed:
            os.remove(os.path.join("tmp",f))

    inputs = os.listdir(os.path.join("data","delivery","000"))
    if len(inputs)>0:
        for folder in inputs:
            shutil.rmtree(os.path.join("data","delivery","000",folder))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    reset()           

    error=None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error = 'No selected file'
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
        if request.form['action'] == 'Process':
            return redirect(url_for('loading_file',
                                    filename=filename.split(".")[0],
                                    route="done"))
        elif request.form['action'] == 'Visualize':
            return redirect(url_for('visualize_file',
                                    filename=filename.split(".")[0]))

    return render_template("index.html", error=error)

@app.route('/visualize_file/<filename>')
def visualize_file(filename):
    extract(os.path.join(app.config['UPLOAD_FOLDER'], filename+".zip"), "tmp")
    return redirect(url_for('loading_file', filename=filename+".TIF", route="visualize"))

@app.route('/process/<route>/<filename>')
def loading_file(filename,route):
    return render_template("process.html", filename=filename, route=route)

@app.route('/done/<filename>')
def process_file(filename):
    extract(os.path.join(app.config['UPLOAD_FOLDER'], filename+".zip"),
    os.path.join("data","delivery","000"))
    files = utils.get_tif_list()
    fname = files[0]

    scan = PhScan(fname)
    print "Generating phragmites estimate..."
    bgrn  = scan.norm
    phrag = phrag_map(bgrn)
    print "Generating the clusters..." 
    clust = cluster_ph(scan, n_clusters=5, n_jobs=10, frac=0.05)


    ffile = os.path.join("tmp", fname.split(os.sep)[-1].replace(".TIF", "_proc.TIF"))


    if not os.path.isfile(ffile):
        print("Writing processed maps to GeoTIFF {0}...".format(ffile))

        write_tif(ffile, scan, phrag, clust)


    print "done"
    return render_template("process_done.html", filename=ffile.split(os.sep)[-1])

@app.route('/download/<filename>')
def download(filename):
    # fzip = filename.replace(".TIF",".zip")
    # with zipfile.ZipFile("tmp/"+fzip, 'w') as myzip:
    #     myzip.write("tmp/"+filename)
    return send_file(open("tmp/"+filename, 'rb'), 
		attachment_filename=os.path.basename(filename),
		mimetype='image/tiff')

@app.route('/image/<path:filename>')
def image(filename):
	'''Used to render an image. Can do some processing here.'''
	return send_file(open("tmp/"+filename, 'rb'), 
		mimetype='image/jpeg')

@app.route('/visualize/<filename>')
def visualize(filename):
    print filename
    fout = filename.replace(".TIF",".jpg")

    rast = gdal.Open("tmp/"+filename)

    width = rast.RasterXSize
    height = rast.RasterYSize
    gt = rast.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5] 
    maxx = gt[0] + width*gt[1] + height*gt[2]
    maxy = gt[3]

    coords = [[maxy,miny],[minx,maxx]] 
    with open(filename.replace(".TIF","_ll.txt"), "wb") as fp:
        pickle.dump(coords, fp)
    print "coord saved"

    img  = rast.ReadAsArray()
    rgb = img[:3,].transpose(1, 2, 0)[..., ::-1].copy()
    rgb /= rgb.max()
    grayw = utils.grayworld(rgb)
    fac = 4
    rgb  = (3.0 * grayw).clip(0, 1)[::fac, ::fac]
    plt.imsave(os.path.join("tmp",fout),rgb)

    phrag = np.dstack([1-img[5,]]+[np.zeros(img[5,].shape)+255]*2)
    phrag = phrag[::fac, ::fac]
    plt.imsave("tmp/"+fout.replace(".jpg","_phrag.png"), phrag)

    df = pd.DataFrame(img[4,][::fac, ::fac])
    ndvishp = img[4,][::fac, ::fac].shape
    with open(filename.replace(".TIF","_shp.txt"), "wb") as fp:
        pickle.dump(ndvishp, fp)
    print "shape saved"

    range_ = [-2,0,.3,.6,1]
    vals = [[0,0,0],[206, 0, 17],[255, 238, 0],[22,224,0]]
    dict_ndvi = {k:v for k,v in zip(range(4),vals)}
    df = df.apply(lambda x: pd.cut(x,range_).cat.codes)
    x = df.apply(lambda x:[dict_ndvi[y] for y in x], axis=1)
    s1=np.vstack(np.array(x.apply(lambda y:[elem[0] for elem in y])))
    s2=np.vstack(np.array(x.apply(lambda y:[elem[1] for elem in y])))
    s3=np.vstack(np.array(x.apply(lambda y:[elem[2] for elem in y])))
    ndvi = np.dstack([s1,s2,s3])
    plt.imsave(os.path.join("tmp",fout.replace(".jpg","_ndvi.png")),ndvi)

    plt.imsave("tmp/"+fout.replace(".jpg","_cluster.png"),img[6][::fac, ::fac], cmap="Accent")
    
    
    print "finish reading file"
    print fout

    time.sleep(10)
    return redirect(url_for('view', filename=fout))
# , coords=coords,ndvi=ndvi.tolist(), ndvishp=ndvi.shape)

@app.route('/view/<filename>')
def view(filename):
    print filename
    with open(filename.replace(".jpg","_ll.txt"), "rb") as fp:
        coords = pickle.load(fp)
    with open(filename.replace(".jpg","_shp.txt"), "rb") as fp:
        ndvishp = pickle.load(fp)
    phrag_fname = filename.replace(".jpg","_phrag.png")
    cluster_fname = filename.replace(".jpg","_cluster.png")
    ndvi_fname = filename.replace(".jpg","_ndvi.png")
    print phrag_fname, cluster_fname, ndvi_fname

    return render_template('visualize.html', \
    title='File: {}'.format(filename.split(".")[0]),\
    filename=filename,\
    phrag=phrag_fname,\
    cluster=cluster_fname,\
    coords=coords,\
    ndvishp=ndvishp,\
    ndvi=ndvi_fname)


if __name__ == '__main__':
	app.run(debug=True, port=5000) # , threaded=True