***********
NeoTech API
***********

This project contains the RESTful API for the company NeoTech.

.. _environment-setup:

Environment Setup:
==================


Python
------

It is highly recommended to run everything in an up-to-date virtualenv.
The project requires python3 to run properly. The environment can be set up
using:

.. code-block:: sh

    $ RND=$RANDOM
    $ virtualenv /tmp/venv$RND --python=python3
    $ source /tmp/venv$RND/bin/activate

In order to run the project, requirements need to be installed. This can be
done by typing:

.. code-block:: sh

    $ pip install -r requirements.txt

Running
=======

Configurations related to running the project can be found from defaults.cfg.

The API can be run simply with:

.. code-block:: sh

    $ python api.py

Documentation
=============

Build the HTML documentation using:

.. code-block:: sh

    $ tox -e sphinx
