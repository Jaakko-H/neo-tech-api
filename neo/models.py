"""
Models for NeoTech API.

"""


class Feedback(object):
    """
    Feedback for a product.

    """

    def __init__(self, feedback_id, rating, time, comment=None):
        """
        Initialise a feedback.

        Args:
            feedback_id (int): Identifies this feedback.
            rating (int): Rating given by the user (a number between 1 and 5).
            time (date): The time the feedback is created.

        Keyword Args:
            comment (string): An optional comment written by the user.

        """
        self.feedback_id = feedback_id
        self.rating = rating
        self.time = time
        self.comment = comment


class Product(object):
    """
    Product for sale.

    """

    def __init__(self, product_id, name):
        """
        Initialise a product. Initialise its feedbacks-list.

        Args:
            product_id (string): Identifies this product.
            name (name): Product name.

        """
        self.product_id = product_id
        self.name = name
        self.feedbacks = []

    def add_feedback(self, feedback):
        """
        Create a new feedback for this product.

        Args:
            feedback (Feedback): The feedback-object to be appended to this
                product's feedbacks-list.

        """
        self.feedbacks.append(feedback)
