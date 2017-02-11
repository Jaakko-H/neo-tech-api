########
Database
########


******
Schema
******

.. image:: neo_tech_database.png

***********
Description
***********

In this project, one of the goals was to design a database-layout for
Neotech's software, where Neotech's products could receive feedback.

The image above illustrates a possible database layout for these products
and their feedbacks. As seen in the image, a product consists of an id and
a name. A feedback consists of an id, rating, comment, time and product_id.
In a database-case, the product_id attribute can be used to join feedbacks
into a specific product.

The layout was designed this way, because a feedback should always have a
target. A product may have any number of feedbacks, but a single feedback
is always linked to only one product. Thus, a feedback may not exist if
it's target product stops existing as well (composition).
