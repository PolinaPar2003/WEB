import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Resource, abort, reqparse
from flask import jsonify
from . import db_session
from .reviews import Reviews


def abort_if_review_not_found(reviews_id):
    session = db_session.create_session()
    reviews = session.query(Reviews).filter(Reviews.id == reviews_id).first()
    if not reviews:
        abort(404, message=f"Review {reviews_id} not found")


class ReviewsResource(Resource):
    def get(self, reviews_id):
        abort_if_review_not_found(reviews_id)
        session = db_session.create_session()
        review = session.query(Reviews).filter(Reviews.id == reviews_id).first()
        return jsonify({'review': review.to_dict(
            only=('id', 'title', 'content', 'created_date', 'user_id'))})

    def delete(self, reviews_id):
        abort_if_review_not_found(reviews_id)
        session = db_session.create_session()
        review = session.query(Reviews).filter(Reviews.id == reviews_id).first()
        session.delete(review)
        session.commit()
        return jsonify({'success': 'OK'})


class ReviewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        review = session.query(Reviews).all()
        return jsonify({'reviews': [item.to_dict(
            only=('id', 'title', 'content', 'created_date', 'user_id')) for item in review]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        review = Reviews()
        review.id = args.json['id']
        review.title = args.json['title']
        review.content = args.json['content']
        review.user_id = args.json['user_id']
        session.add(review)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)
