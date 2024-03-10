"""Database manager."""
from peewee import PostgresqlDatabase


class DatabaseManager:
    """Database manager.

    this class manage connection to database.
    """
    def __init__(self, database_name, user, password, host, port):
        """Connect to database.

        :param database_name: database name
        :param user: user name
        :param password: password
        :param host: host name
        :param port: port number
        """
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        # Connect
        self.db = self.connect_to_database()

    def connect_to_database(self):
        """Connect to database."""
        database_connection = PostgresqlDatabase(
            self.database_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        database_connection.connect()
        return database_connection

    def close_connection(self):
        """close connection."""
        self.db.close()

    def create_tables(self, models):
        """Create tables."""
        self.db.create_tables(models)
