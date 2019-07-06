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
        self.logger = conf._init_logger(logger=conf.LOGGER_ORM, filehandler=conf.LOG_INFO)
        self.logger.info("[+] Initilizing Orm [+]")


        self.engine = sqlalchemy.create_engine(
            f"mysql+mysqldb://{conf.DB_USER}:{conf.DB_PASSWORD}@{conf.DB_ADRESS}/{conf.DB_NAME}")
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.metadata.reflect(only=["examens", "sections", "patients", "medecins", "types_intervention"])
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
        self.types_interventions = sqlalchemy.Table("types_intervention", self.metadata)
        self.logger.info("[+] Orm initialized [+]\n\n")

    def check_table(self,):
        import datetime
        """
            Create a new table if it doest exist
        """
        self.logger.info("\t[+] Checking table hl7_connections if it exist [+]")
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
            self.logger.info("\t[-] Creating table hl7_connections [-]")
            self.metadata.create_all()
            self.logger.info("\t[+] hl7_connections successfully created [+]")

    def insertHl7Connection(self, msg):
        """
            Insert the string :msg: to the db
        """
        self.hl7_connections.insert().values(message=msg).execute()


    def get_sections(self,):
        """
            Returns all the sections rows
        """
        self.logger.info("\t[+] get_sections [+]")
        try:
            return self.sections.select().execute()
        except Exception as e:
            self.logger.critical("\t[-] Exception occured [-]")
            self.logger.critical("\t" + str(e))
            self.logger.critical("\t[-] Exception occured [-]")

    def get_examen(self, id_examen):
        """
            Return the examen row of the id_examen passed
        """

        self.logger.info("\t[+] get_examen [+]")
        self.logger.info(f"\t[+] id_examen {id_examen} [+]")
        try:
            return self.examens.select().where(self.examens.columns.id_examen == id_examen).execute()
        except Exception as e:
            self.logger.critical("\t[-] Exception occured [-]")
            self.logger.critical("\t" + str(e))
            self.logger.critical("\t[-] Exception occured [-]")

    def get_types_intervention(self, id_examen):
            """
                Return the type_interventions row of the id_examen passed
            """

            self.logger.info("\t[+] get_type_intervention [+]")
            self.logger.info(f"\t[+] id_examen {id_examen} [+]")
            try:
                # Select the row and retrieve the id
                id_type_intervention = list(self.examens.select().where(self.examens.columns.id_examen == id_examen).execute())[0][5]

                if(id_type_intervention):
                    return self.types_interventions.select().where(self.types_interventions.columns.id_type_intervention == id_type_intervention).execute()
                else:
                    self.logger.warning(f"\t [-] types_intervention not found {id_type_intervention} [-]")
                    return False
            except Exception as e:
                self.logger.critical("\t[-] Exception occured [-]")
                self.logger.critical("\t" + str(e))
                self.logger.critical("\t[-] Exception occured [-]")

    def get_medecin(self, id_examen):
            """
                Return the type_interventions row of the id_examen passed
            """

            self.logger.info("\t[+] get_type_intervention [+]")
            self.logger.info(f"\t[+] id_examen {id_examen} [+]")
            try:
                # Select the row and retrieve the id
                row = list(self.examens.select().where(self.examens.columns.id_examen == id_examen).execute())[0]
                id_medecin_interv = row[7]
                id_medecin_presc = row[13]

                if(id_medecin_interv or id_medecin_presc):
                    return (self.medecins.select().where(self.medecins.columns.id_medecin == id_medecin_interv).execute(),
                    self.medecins.select().where(self.medecins.columns.id_medecin == id_medecin_presc).execute())
                else:
                    self.logger.warning(f"\t [-] types_intervention not found interv : {id_medecin_presc}, presc: {id_medecin_presc} [-]")
                    return False
            except Exception as e:
                self.logger.critical("\t[-] Exception occured [-]")
                self.logger.critical("\t" + str(e))
                self.logger.critical("\t[-] Exception occured [-]")


    def get_patient(self, id_examen):
        """
            Return the patient row of the id_patient passed
        """

        self.logger.info("\t[+] get_patient [+]")
        self.logger.info(f"\t[+] id_examen {id_examen} [+]")

        try:
            # Select the row and retrieve the id
            id_patient = list(self.examens.select().where(self.examens.columns.id_examen == id_examen).execute())[0][1]

            if(id_patient):
                return self.patients.select().where(self.patients.columns.id_patient == id_patient).execute()
            else:
                self.logger.warning(f"\t [-] Patient not found {id_patient} [-]")
                return False

        except Exception as e:
            self.logger.critical("\t[-] Exception occured [-]")
            self.logger.critical("\t" + str(e))
            self.logger.critical("\t[-] Exception occured [-]")



if __name__ == "__main__":
    import conf
    logger = conf._init_logger(logger=conf.LOGGER_ORM, filehandler=False)
    m = Orm()
    m.insertHl7Connection("test")
