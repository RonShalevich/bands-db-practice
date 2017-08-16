from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from band_setup import Base, Band
from werkzeug.utils import secure_filename
import os
import urlparse


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pfd', 'png', 'jpg',
                                        'jpeg', 'gif'])
engine = create_engine('sqlite:///bands.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/bands/')
def allBands():
    bands = session.query(Band).all()
    return render_template('bands.html', bands=bands)


@app.route('/band/<int:band_id>/')
def showBand(band_id):
    band = session.query(Band).filter_by(id=band_id).one()

    return render_template('showband.html', band=band)


@app.route('/band/photo/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.file:
        filename = photos.save(request.files['photo'])
        rec = photo(filename=filename, user=g.user.id)
        rec.store()
        lash("Photo saved.")
        return redirect(url_for('showBand', id=rec.id))
    return render_template('upload.html')


@app.route('/bands/new', methods=['GET', 'POST'])
def createBand():
    if request.method == 'POST':
        url_video = request.form['video']
        video = url_video.replace('watch?v=', 'embed/')

        url_music = request.form['track']
        update_url = url_music.find('/track/')
        track = url_music[:update_url] + '/embed' + url_music[update_url:]

        url_album = request.form['album']
        album = url_album + '?mt=1&app=music'

        newBand = Band(name=request.form['name'], bio=request.form['bio'],
                       music=request.form['music'],
                       pic=request.form['pic'],
                       track=track,
                       album=album,
                       video=video,
                       email=request.form['email'],
                       website=request.form['website'],
                       social=request.form['social'],
                       home=request.form['home'])

        session.add(newBand)
        session.commit()
        return redirect(url_for('allBands'))
    else:
        return render_template('newband.html')


@app.route('/bands/<int:band_id>/edit', methods=['GET', 'POST'])
def editBand(band_id):
    editedBand = session.query(Band).filter_by(id=band_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBand.name = request.form['name']
        if request.form['bio']:
            editBand.bio = request.form['bio']
        if request.form['music']:
            editedBand.music = request.form['music']
        if request.form['video']:
            url = request.form['video']
            url_data = urlparse.urlparse(url)
            query = urlparse.parse_qs(url_data.query)
            editedBand.video = query["v"][0]
        if request.form['pic']:
            editedBand.pic = request.form['pic']
        if request.form['album']:
            url_album = request.form['album']
            album = url_album + '?mt=1&app=music'
        if request.form['track']:
            url = request.form['track']
            update_url = url.find('/track/')
            editedBand.track = url[:update_url] + '/embed' + url[update_url:]
        session.add(editedBand)
        session.commit()
        return redirect(url_for('showBand', band_id=band_id))
    else:
        return render_template('editband.html', band_id=band_id,
                               band=editedBand)


@app.route('/band/<int:band_id>/delete', methods=['GET', 'POST'])
def deleteBand(band_id):
    bandToDelete = session.query(Band).filter_by(id=band_id).one()
    if request.method == 'POST':
        session.delete(bandToDelete)
        session.commit()
        return redirect(url_for('allBands'))
    else:
        return render_template('deleteBand.html', band=bandToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
