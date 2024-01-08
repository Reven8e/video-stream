import psycopg2

from abc import ABC, abstractmethod
import os


class DatabaseInterface(ABC):
    """
    Abstract base class for database interfaces.
    """
    @abstractmethod
    def execute_query(self, query, params=None):
        """
        Executes the given query on the database.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to be passed to the query.

        Returns:
            None
        """
        pass

    @abstractmethod
    def commit(self):
        """
        Commits the changes made to the database.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Closes the database connection.
        """
        pass


class PostgresDatabase(DatabaseInterface):
    """
    A class representing a Postgres database.

    Attributes:
        connection (psycopg2.extensions.connection): The connection to the Postgres database.

    Methods:
        __init__(): Initializes the PostgresDatabase object.
        execute_query(query, params=None, fetch='all' or 'one' or None): Executes a query on the database.
        commit(): Commits the changes made to the database.
        close(): Closes the connection to the database.
    """
    def __init__(self):
        """
        Initializes a new instance of the DBInterfaces class.
        Establishes a connection to the PostgreSQL database using the environment variables for host, user, and password.
        """
        self.connection = psycopg2.connect(
            host=os.environ['PSQL_HOST'],
            user=os.environ['PSQL_USER'],
            password=os.environ['PSQL_PASSWORD']
        )

    def execute_query(self, query, params=None, fetch='all'):
        """
        Executes a query on the Postgres database.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): The parameters to be passed to the query (default: None).
            fetch (str, optional): Specifies whether to fetch 'all' rows, 'one' last row, or None and return True. (default: 'all').

        Returns:
            list or tuple or bool: The result of the query execution.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch == 'all':
                return cursor.fetchall()
            elif fetch == 'one':
                return cursor.fetchone()
            elif fetch is None:
                return True

    def commit(self):
        """
        Commits the changes made to the Postgres database.
        """
        self.connection.commit()

    def close(self):
        """
        Closes the connection to the Postgres database.
        """
        self.connection.close()
