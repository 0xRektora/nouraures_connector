import sqlalchemy
import logging
import conf
from utils import Singleton


class Orm(Singleton):
    """
        Orm Class to connect with the DB
    """

    def __init__(self,):
        """
            Init the connetcion with the database
        """
        logging.info("[+] Initilizing Orm [+]")

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
        logging.info("[+] Orm initialized [+]")

    def check_table(self,):
        import datetime
        """
            Create a new table if it doest exist
        """
        logging.info("\t[+] Checking table hl7_connections if it exist [+]")
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
            logging.info("\t[-] Creating table hl7_connections [-]")
            self.metadata.create_all()
            logging.info("\t[+] hl7_connections successfully created [+]")

    def get_sections(self,):
        """
            Returns all the sections rows
        """
        logging.info("\t[+] get_sections [+]")
        try:
            return self.sections.select().execute()
        except Exception as e:
            logging.critical("\t[-] Exception occured [-]")
            logging.critical("\t" + str(e))
            logging.critical("\t[-] Exception occured [-]")

    def get_examen(self, id_examen):
        """
            Return the examen row of the id_examen passed
        """

        logging.info("\t[+] get_examen [+]")
        logging.info(f"\t[+] id_examen {id_examen} [+]")
        try:
            return self.examens.select().where(self.examens.columns.id_examen == id_examen).execute()
        except Exception as e:
            logging.critical("\t[-] Exception occured [-]")
            logging.critical("\t" + str(e))
            logging.critical("\t[-] Exception occured [-]")

    def get_patient(self, id_examen):
        """
            Return the patient row of the id_patient passed
        """

        logging.info("\t[+] get_patient [+]")
        logging.info(f"\t[+] id_examen {id_examen} [+]")

        try:
            # Select the row and retrieve the id
            id_patient = list(self.examens.select().where(self.examens.columns.id_examen == id_examen).execute())[0][1]

            if(id_patient):
                return self.patients.select().where(self.patients.columns.id_patient == id_patient).execute()
            else:
                logging.warning(f"\t [-] Patient not found {id_patient} [-]")
                return False

        except Exception as e:
            logging.critical("\t[-] Exception occured [-]")
            logging.critical("\t" + str(e))
            logging.critical("\t[-] Exception occured [-]")



if __name__ == "__main__":
    import conf
    conf.logging_state()
    logging.debug("[+] Testing orm.py [+]")
    m = Orm()
    m.hl7_connections.insert().values(message="test").execute()
    logging.debug("[+] Testing orm.py [+]")

