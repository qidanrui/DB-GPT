import re
from typing import Optional, Any
from sqlalchemy import text

from pilot.connections.rdbms.base import RDBMSDatabase


class ClickhouseConnect(RDBMSDatabase):
    """Connect Clickhouse Database fetch MetaData
    Args:
    Usage:
    """

    db_type: str = "clickhouse"
    driver: str = "clickhouse"
    db_dialect: str = "clickhouse"

    @classmethod
    def from_uri_db(
            cls,
            host: str,
            port: int,
            user: str,
            pwd: str,
            db_name: str,
            engine_args: Optional[dict] = None,
            **kwargs: Any,
    ) -> RDBMSDatabase:
        db_url: str = (
                cls.driver
                + "://"
                + user
                + ":"
                + pwd
                + "@"
                + host
                + ":"
                + str(port)
                + "/"
                + db_name
        )
        return cls.from_uri(db_url, engine_args, **kwargs)

    def get_indexes(self, table_name):
        """Get table indexes about specified table."""
        return """"""

    def get_show_create_table(self, table_name):
        """Get table show create table about specified table."""
        session = self._db_sessions()
        cursor = session.execute(text(f"SHOW CREATE TABLE  {table_name}"))
        ans = cursor.fetchall()
        ans = ans[0][0]
        ans = re.sub(r"\s*ENGINE\s*=\s*MergeTree\s*", " ", ans, flags=re.IGNORECASE)
        ans = re.sub(
            r"\s*DEFAULT\s*CHARSET\s*=\s*\w+\s*", " ", ans, flags=re.IGNORECASE
        )
        ans = re.sub(r"\s*SETTINGS\s*\s*\w+\s*", " ", ans, flags=re.IGNORECASE)
        return ans

    def get_fields(self, table_name):
        """Get column fields about specified table."""
        session = self._db_sessions()
        cursor = session.execute(
            text(
                f"SELECT name, type, default_expression, is_in_primary_key, comment  from system.columns where table='{table_name}'".format(
                    table_name
                )
            )
        )
        fields = cursor.fetchall()
        return [(field[0], field[1], field[2], field[3], field[4]) for field in fields]

    def get_users(self):
        return []

    def get_grants(self):
        return []

    def get_collation(self):
        """Get collation."""
        return "UTF-8"

    def get_charset(self):
        return "UTF-8"

    def get_database_list(self):
        return []

    def get_database_names(self):
        return []

    def get_table_comments(self, db_name):
        session = self._db_sessions()
        cursor = session.execute(
            text(
                f"""SELECT table, comment FROM system.tables WHERE database = '{db_name}'""".format(
                    db_name
                )
            )
        )
        table_comments = cursor.fetchall()
        return [
            (table_comment[0], table_comment[1]) for table_comment in table_comments
        ]
