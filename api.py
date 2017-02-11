#!/usr/bin/env python3.5

"""
The API module.

"""

# configparser in Python 3, ConfigParser in Python 2
import configparser
from datetime import datetime

from flask import Flask

from flask_httpauth import HTTPBasicAuth

from flask_restful import abort
from flask_restful import Api
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Resource

from neo import models

import timestring
from timestring import TimestringInvalid

# Global variable for counting feedbacks. API-objects get re-initialised after
# REST calls, thus this value cannot be initialised in those classes.
FEEDBACK_COUNT = 0

# Initialise Flask
app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

# Initialise request parser for parsing values from HTTP requests
req_parser = reqparse.RequestParser()
# Always require a rating
req_parser.add_argument(
    'rating', type=int, help='Rating must be a number between 1 and 5.',
    required=True)
req_parser.add_argument(
    'comment', type=str, help='Comment optional for feedback.')
req_parser.add_argument(
    'time_start', type=str,
    help='Example date-form: jan 18th 2017 at 10:00')
req_parser.add_argument(
    'time_end', type=str,
    help='Example date-form: feb 18th 2018 at 16:00')

# XXX: Move this data to a database.
PRODUCTS = {
    '0815': models.Product('0815', 'Foobar-Soundsystem'),
    '1337': models.Product('1337', 'Soundblaster Pro')}

# XXX: Move this data to a database and hash it.
USERS = {
    'neo': 'technician',
    'super': 'admin'
}

# Used with Marshal
feedback_fields = {
    'feedback_id': fields.Integer,
    'rating': fields.Integer,
    'time': fields.DateTime,
    'comment': fields.String
}

# Used with Marshal
product_fields = {
    'product_id': fields.String,
    'name': fields.String,
    'feedbacks': fields.Nested(feedback_fields)
}


def abort_if_product_doesnt_exist(product_id):
    """
    Abort the API call if the requested product does not exist.

    Args:
        product_id (string): The product_id defined in the route.

    """
    if product_id not in PRODUCTS:
        abort(404, message="Product {} doesn't exist".format(product_id))


def abort_if_rating_not_in_range(rating):
    """
    Abort the API call if the given rating is not in the wanted range of 1-5.

    Args:
        rating (int): The rating sent as data in the API call.

    """
    if not rating >= 1 or not rating <= 5:
        abort(400, message='Rating {} not in range of 1-5.'.format(rating))


@auth.get_password
def get_pw(username):
    """
    Check if the given username exists in the USERS-dictionary.

    If a match is found, return its password. Otherwise return None.

    Args:
        username (string): The username included in the API call.

    Returns:
        Password in the USERS-dictionary if successful, None otherwise.

    """
    if username in USERS:
        return USERS.get(username)
    return None


class ProductAPI(Resource):
    """
    REST API for specified product.

    Args:
        resource (flask_restful.Resource): Resource to be added to the API.

    """

    @marshal_with(product_fields)
    def get(self, product_id, **kwargs):
        """
        Get a product's data.

        A local curl call to this method could be for example:

        ``curl http://127.0.0.1:5000/products/<product_id>``

        Args:
            product_id (str): The product_id defined in the route.

        Returns:
            The object specified with the key from the PRODUCTS-dictionary.
            The object is transformed into a JSON-serializable form with
            Marshal.

        """
        abort_if_product_doesnt_exist(product_id)
        return PRODUCTS[product_id]

    @marshal_with(feedback_fields)
    def post(self, product_id, **kwargs):
        """
        Add a new feedback for a product.

        A local curl call to this method could be for example:

        ``curl -d 'rating=5'
        http://localhost:5000/products/<product_id> -X POST``

        Or:

        ``curl -d 'rating=3' -d 'comment=Foo bar.'
        http://localhost:5000/products/<product_id> -X POST``

        Args:
            product_id (str): The product_id defined in the route.

        Returns:
            The successfully created object and The HTTPStatus code.

        """
        abort_if_product_doesnt_exist(product_id)
        # strict=True ensures that an error is thrown if there are undefined
        # arguments
        args = req_parser.parse_args(strict=True)
        rating = args['rating']
        abort_if_rating_not_in_range(rating)

        comment = args['comment']

        time = datetime.now()

        # Increment the global variable that is initialised on module runtime
        # Use the incremented value for feedback_id
        global FEEDBACK_COUNT
        FEEDBACK_COUNT += 1

        # Create a new feedback-object
        feedback = models.Feedback(FEEDBACK_COUNT, rating, time, comment)

        # Append the created feedback to the product's list of feedbacks
        PRODUCTS[product_id].add_feedback(feedback)

        # 201 = Request successful, new resource created
        return feedback, 201


class ProductAdminAPI(Resource):
    """
    REST API for an admin to retrieve more details about a product's feedbacks.

    Args:
        resource (flask_restful.Resource): Resource to be added to the API.

    """

    @auth.login_required
    def get(self, product_id, **kwargs):
        """
        Get the number of feedbacks found with a specific rating.

        Optionally, the number of feedbacks can be filtered to a specific
        time-range. This method is available only via authentication.

        Note that this method requires you to specify -X GET in the curl.
        A local curl call to this method could be for example:

        ``curl -d 'rating=1' -u <username>
        http://localhost:5000/admin/products/<product_id> -X GET``

        Or:

        ``curl -d 'rating=3' -d 'time_start=jan 17th 2017 at 0:51'
        -d 'time_end=jan 18th 2017 at 23:50' -u <username>
        http://localhost:5000/admin/products/<product_id> -X GET``

        Args:
            product_id (str): The product_id defined in the route.

        Returns:
            dict: The number of feedbacks found and the defined time-ranges

        Raises:
            HTTPUnauthorized: If no user is authenticated.

        """
        abort_if_product_doesnt_exist(product_id)

        # strict=True ensures that an error is thrown if there are undefined
        # arguments
        args = req_parser.parse_args(strict=True)
        rating = args['rating']
        abort_if_rating_not_in_range(rating)

        time_start = args['time_start']
        if time_start:
            # If a time-frame start was specified, try to convert it
            # If it fails, abort the call
            try:
                time_start = timestring.Date(time_start)
                print(time_start)
            except TimestringInvalid:
                abort(400, message='Date {} not in correct format.'.format(
                    time_start))

        time_end = args['time_end']
        if time_end:
            # If a time-frame end was specified, try to convert it
            # If it fails, abort the call
            try:
                time_end = timestring.Date(time_end)
                print(time_end)
            except TimestringInvalid:
                abort(400, message='Date {} not in correct format.'.format(
                    time_end))

        # Initialise feedback count
        feedback_count_by_rating = 0

        # Loop through all feedbacks of the product
        for feedback in PRODUCTS[product_id].feedbacks:
            if rating == feedback.rating:
                # If the time-frame has not been specified, count all matches
                if not time_start and not time_end:
                    feedback_count_by_rating += 1
                elif time_start:
                    # If the start of the time-frame has been specified
                    # and this feedback is younger than that
                    if time_start <= feedback.time:
                        # If the end of the time-frame has not been specified
                        # count all matches that are older than time_start
                        if not time_end:
                            feedback_count_by_rating += 1
                        # Otherwise, check if the feedback is older than
                        # the end of the time_frame
                        elif time_end >= feedback.time:
                            feedback_count_by_rating += 1
                elif time_end:
                    # If only the end of the time-frame has been specified,
                    # count feedbacks that are older than it
                    if time_end >= feedback.time:
                        feedback_count_by_rating += 1

        return {'rating {}'.format(rating): feedback_count_by_rating,
                'time_start': args['time_start'],
                'time_end': args['time_end']}

# Setup API routing
api.add_resource(ProductAPI, '/products/<product_id>')
api.add_resource(ProductAdminAPI, '/admin/products/<product_id>')


def main():
    """
    The main method of this application.

    Uses configparser to parse configuration settings from
    defaults.cfg-file. After that runs the flask-app.

    """
    config_parser = configparser.SafeConfigParser()
    config_parser.read('defaults.cfg')
    try:
        debug = config_parser.getboolean('api', 'debug')
    except ValueError:
        debug = False
        print('debug not True or False, default to False')

    app.run(debug=debug)

if __name__ == '__main__':
    main()
