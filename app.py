#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
# TODO: Python標準ライブラリ、サードパーティのライブラリ、そして自作のモジュールという順番でインポートする
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_moment import Moment
from extensions import db, migrate
from models import Venue, Artist, Show
import logging
from logging import Formatter, FileHandler
from forms import *
from enums import *
from collections import defaultdict

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db.init_app(app)
migrate.init_app(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = Venue.query.order_by(Venue.state, Venue.city).all()
  grouped_venues = defaultdict(list)
  for venue in venues:
    key = (venue.city, venue.state)
    grouped_venues[key].append({
      "id": venue.id,
      "name": venue.name,
    })

  data = []
  for (city, state), venues_list in grouped_venues.items():
    data.append({
      "city": city,
      "state": state,
      "venues": venues_list
    })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term')
  venues = db.session.query(Venue).filter(Venue.name.like(f'%{search_term}%')).all()
  return render_template('pages/search_venues.html', results=venues, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.get(venue_id)
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: enable CSRF protection
  form = VenueForm(request.form, meta={'csrf': False})

  # on successful db insert, flash success
  if form.validate_on_submit():
    try:
      new_venue = Venue(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        address = form.address.data,
        phone = form.phone.data,
        image_link = form.image_link.data,
        genres = form.genres.data,
        facebook_link = form.facebook_link.data,
        website = form.website_link.data,
        seeking_talent = form.seeking_talent.data,
        seeking_description = form.seeking_description.data,
      )
      db.session.add(new_venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
      flash('An error occurred. Venue ' + form.name.data + ' could not be created.', 'danger')
      db.session.rollback()
    finally:
      db.session.close()
      return redirect(url_for('venues'))

  else:
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    for field, error in form.errors.items():
      flash(f"An error occurred. Venue {getattr(form, field).label.text} could not be listed. {error}", 'danger')
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: enable CSRF protection
  form = VenueForm(request.form, meta={'csrf': False})
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.image_link.data = venue.image_link
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: enable CSRF protection
  form = VenueForm(request.form, meta={'csrf': False})
  venue = Venue.query.get(venue_id)
  if not venue:
    flash("Venue not found!", "error")
    return redirect(url_for('index'))
  if form.validate():
    try:
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.image_link = form.image_link.data
      venue.genres = form.genres.data
      venue.facebook_link = form.facebook_link.data
      venue.website = form.website_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully updated!')

    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Venue ' + form.name.data + ' could not be updated.', 'danger')
    finally:
      db.session.close()
      return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    for field, error in form.errors.items():
      flash(f"An error occurred. Venue {getattr(form, field).label.text} could not be updated. {error}", 'danger')
    return render_template('forms/edit_venue.html', venue=venue, form=form)

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term')
  artists = db.session.query(Artist).filter(Artist.name.like(f'%{search_term}%')).all()

  return render_template('pages/search_artists.html', results=artists, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  artist = Artist.query.get(artist_id)
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: improve csrf
  # TODO: request.formが必要かどうか調べる
  form = ArtistForm(request.form, meta={'csrf': False})
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.phone.data = artist.phone
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  form.genres.data = artist.genres
  form.state.data = artist.state
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: enable CSRF protection
  form = ArtistForm(request.form, meta={'csrf': False})
  artist = Artist.query.get(artist_id)
  if not artist:
    flash("Artist not found!", "error")
    return redirect(url_for('index'))
  if form.validate():
    try:
      artist.name = form.name.data
      artist.city = form.city.data
      artist.phone = form.phone.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.website = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      artist.genres = form.genres.data
      artist.state = form.state.data
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully updated!')

    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Artist ' + form.name.data + ' could not be updated.', 'danger')
    finally:
      db.session.close()
      return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    for field, error in form.errors.items():
      flash(f"An error occurred. Artist {getattr(form, field).label.text} could not be updated. {error}", 'danger')
      return render_template('forms/edit_artist.html',artist=artist ,form=form)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  form = ArtistForm(request.form, meta={'csrf': False})

  # on successful db insert, flash success
  if form.validate_on_submit():
    try:
      new_artist = Artist(
        name = form.name.data,
        city = form.city.data,
        phone = form.phone.data,
        image_link = form.image_link.data,
        facebook_link = form.facebook_link.data,
        website = form.website_link.data,
        seeking_venue = form.seeking_venue.data,
        seeking_description = form.seeking_description.data,
        genres = form.genres.data,
        state = form.state.data
      )
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
      flash('An error occurred. Venue ' + form.name.data + ' could not be created.', 'danger')
      db.session.rollback()
      flash('An error occurred. Artist ' + form.name.data + ' could not be created.', 'danger')
    finally:
      db.session.close()
    return redirect(url_for('artists'))
  else:
    for field, error in form.errors.items():
      flash(f"Error in {getattr(form, field).label.text}: {error}")
    return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  shows = Show.query.all()
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  form = ShowForm(request.form, meta={'csrf': False})
  if form.validate_on_submit():
    try:
      new_show = Show(
        artist_id = form.data['artist_id'],
        venue_id = form.data['venue_id'],
        start_time = form.data['start_time']
      )
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
    except Exception as e:
      flash('An error occurred. Show could not be created.', 'danger')
      db.session.rollback()
    finally:
      db.session.close()
    return redirect(url_for('shows'))
  else:
    for field, error in form.errors.items():
      flash(f"Error in {getattr(form, field).label.text}: {error}")
    return render_template('forms/new_show.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
