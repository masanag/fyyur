from extensions import db
from enums import GenreEnum, StateEnum
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects import postgresql
from datetime import datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String())

    shows = db.relationship('Show', backref='venue', lazy=True)
    genres_enum = ENUM(*[genre.name for genre in GenreEnum], name='genres_enum')
    genres = db.Column(postgresql.ARRAY(genres_enum), nullable=False)
    state = db.Column(ENUM(*[state.name for state in StateEnum], name='state_enum'), nullable=False)

    @property
    def upcoming_shows(self):
      return [show for show in self.shows if show.start_time > datetime.utcnow()]

    @property
    def past_shows(self):
      return [show for show in self.shows if show.start_time < datetime.utcnow()]

    @property
    def upcoming_shows_count(self):
      return len(self.upcoming_shows)

    @property
    def past_shows_count(self):
      return len(self.past_shows)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='artist', lazy=True)
    genres_enum = ENUM(*[genre.name for genre in GenreEnum], name='genres_enum')
    genres = db.Column(postgresql.ARRAY(genres_enum), nullable=False)
    state = db.Column(ENUM(*[state.name for state in StateEnum], name='state_enum'), nullable=False)

    @property
    def upcoming_shows(self):
      return [show for show in self.shows if show.start_time > datetime.utcnow()]

    @property
    def past_shows(self):
      return [show for show in self.shows if show.start_time < datetime.utcnow()]

    @property
    def upcoming_shows_count(self):
      return len(self.upcoming_shows)

    @property
    def past_shows_count(self):
      return len(self.past_shows)

class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
