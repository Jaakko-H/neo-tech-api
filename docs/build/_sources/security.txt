########
Security
########

Upon the project's realisation, there are some related security issues that
could arise.

One of them could be the way the passwords are storaged. If the usernames and
their passwords were stored in a database-system, they should be hashed
properly to be well secure. If Flask-HTTPBasicAuth is used,
the @auth.hash_password decorator should be used for hashing the passwords
upon comparing them. Alternatively, @auth.verify_password could be used
to combine both get_password (as used in this case) and hash_password.

Another issue could be protection from SQL-injections in case the database
is realised with SQL. A user who calls for the method to add a new feedback,
could for example assign an SQL-query into the comment-argument. The source
https://docs.python.org/3/library/sqlite3.html has a suggestion to how this
could be prevented.
