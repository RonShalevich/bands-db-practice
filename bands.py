from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from band_setup import Base, Band
import urlparse


app = Flask(__name__)

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


@app.route('/bands/new', methods=['GET', 'POST'])
def createBand():
    if request.method == 'POST':
        url_video = request.form['video']
        url_data = urlparse.urlparse(url_video)
        query = urlparse.parse_qs(url_data.query)
        video = query["v"][0]

        url_music = request.form['track']
        update_url = url_music.find('/track/')
        track = url_music[:update_url] + '/embed' + url_music[update_url:]

        newBand = Band(name=request.form['name'], bio=request.form['bio'],
                       pic=request.form['pic'], music=request.form['music'],
                       track=track, video=video, email=request.form['email'],
                       website=request.form['website'], social=request.form['social'],
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
