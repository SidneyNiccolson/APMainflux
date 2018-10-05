import unittest

from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User

# create flaskgroup instance to extend the normal Flask CLIE commands
app = create_app()
cli = FlaskGroup(create_app=create_app)

# register a command to test services
@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

# register a command to recreate the db from the command line
@cli.command()
def recreatedb():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()