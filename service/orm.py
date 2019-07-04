import sqlalchemy
import logging
import conf


class Orm():
    """
        Orm Class to connect with the DB
    """

    def __init__(self,):
        """
            Init the connetcion with the database
        """
        self.engine = sqlalchemy.create_engine(
            f"mysql+mysqldb://{conf.DB_USER}:{conf.DB_PASSWORD}@{conf.DB_ADRESS}/{conf.DB_NAME}")
        self.metadata = sqlalchemy.MetaData(bind=self.engine, reflect=True)
        self.conn = self.engine.connect()
        """
            Load the ORM of different table into the class
        """
        self.check_table()
        self.examens = sqlalchemy.Table("examens", self.metadata)
        self.examens = sqlalchemy.Table("examens", self.metadata)

    def check_table(self,):
        if not self.engine.has_table("hl7_connections"):
            import datetime
            sqlalchemy.Table("users", self.metadata,
                            sqlalchemy.Column("id", sqlalchemy.Integer, sqlalchemy.Sequence(
                                "user_id_seq"), primary_key=True),
                            sqlalchemy.Column(
                                "message", sqlalchemy.String(255)),
                            sqlalchemy.Column(
                                "sent_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
                            keep_existing=True
                            )


if __name__ == "__main__":
    import conf
    conf.logging_state()
    m = Orm()
    logging.debug("[+] Orm initialized [+]")
    logging.debug(next(iter(m.examens.select().limit(10).execute())))
