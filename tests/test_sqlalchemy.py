from sqlalchemy import text

from app.database.engine import engine


def test_sqlalchemy_connection():

    with engine.connect() as connection:

        result = connection.execute(text("SELECT 1"))

        assert result.scalar_one() == 1