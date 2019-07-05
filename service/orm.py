import sqlalchemy
import logging
import conf


class Orm(Singleton):
    """
        Orm Class to connect with the DB
    """

    def __init__(self,):
        """
            Init the connetcion with the database
        """
        logging.debug("[+] Initilizing Orm [+]")

        # If the

        self.engine = sqlalchemy.create_engine(
            f"mysql+mysqldb://{conf.DB_USER}:{conf.DB_PASSWORD}@{conf.DB_ADRESS}/{conf.DB_NAME}")
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.metadata.reflect(only=["examens", "sections", "users"])
        self.conn = self.engine.connect()
        """
            Load the ORM of different table into the class
        """
        self.check_table()
        self.hl7_connections = sqlalchemy.Table("hl7_connections", self.metadata)
        self.examens = sqlalchemy.Table("examens", self.metadata)
        self.sections = sqlalchemy.Table("sections", self.metadata)
        self.patients = sqlalchemy.Table("patients", self.metadata)
        self.medecins = sqlalchemy.Table("medecins", self.metadata)
        logging.debug("[+] Orm initialized [+]")

    def check_table(self,):
        import datetime
        """
            Create a new table if it doest exist
        """
        logging.debug("\t[+] Checking table hl7_connections if it exist [+]")
        sqlalchemy.Table("hl7_connections", self.metadata,
                        sqlalchemy.Column(
                            "id", sqlalchemy.Integer, primary_key=True),
                        sqlalchemy.Column(
                            "message", sqlalchemy.String(255),),
                        sqlalchemy.Column(
                            "sent_at", sqlalchemy.DateTime, default=datetime.datetime.now),
                        keep_existing=True
                        )

        if not self.engine.has_table("hl7_connections"):
            logging.debug("\t[-] Creating table hl7_connections [-]")
            self.metadata.create_all()
            logging.debug("\t[+] hl7_connections successfully created [+]")



if __name__ == "__main__":
    import conf
    conf.logging_state()
    m = Orm()
    m.hl7_connections.insert().values(message="test").execute()
    logging.debug(next(m.users.select().limit(10).execute()))

