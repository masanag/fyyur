from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField, ValidationError
from wtforms.validators import DataRequired, AnyOf, URL, Regexp
from enums import *

def facebook_validator(form, field):
    if 'www.facebook.com/' not in field.data:
        raise ValidationError("URL must contain 'www.facebook.com/'")

class ShowForm(Form):
    artist_id = IntegerField(
        'artist_id',
        validators=[DataRequired()]
    )
    venue_id = IntegerField(
        'venue_id',
        validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=StateEnum.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone',
        validators=[
            DataRequired(),
            Regexp(r'^[0-9\-*$]', message="Phone number can only contain digits and dashes.")
        ]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=GenreEnum.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired(), URL(), facebook_validator]
     )
    website_link = StringField(
        'website_link', validators=[DataRequired(), URL()]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=StateEnum.choices()
    )
    phone = StringField(
        'phone',
        validators=[
            DataRequired(),
            Regexp(r'^[0-9\-]*$', message="Phone number can only contain digits and dashes.")
        ]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=GenreEnum.choices()
     )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired(), URL(), facebook_validator]
     )

    website_link = StringField(
        'website_link', validators=[DataRequired(), URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

