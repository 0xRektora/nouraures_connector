"""
    File that includes utility for Nouraures Connector
"""



class Singleton():
    """
        Class that'll apply the Singleton design pattern to the passed
    """
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]

def readXmlFile(csvPath):
    import conf, csv, logging
    """
        Take a path into the param and convert the xml file into a python object
    """
    logger = conf._init_logger(logger=conf.LOGGER_UTILS)
    logger = logging.getLogger(conf.LOGGER_UTILS)
    try:
        obj = []
        path = conf.FULL_PATH+csvPath

        with open(path, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                obj.append(row)
        logger.info(f"[+] Successfully loaded {path}")

        if csvPath == conf.STATIC_MEDECIN:
            [obj.remove(obj[x]) for x in range(0, 4, 1)]
            obj = list(filter(lambda x: x != [";;;"], obj))
            obj = list(map(lambda x: x[0].split(";"), obj))

        if csvPath == conf.STATIC_TYPE_INTERVENTION:
            obj.remove(obj[0])
            obj = list(filter(lambda x: x != [";;;"], obj))
            obj = list(map(lambda x: x[0].split(";"), obj))

        return obj
    except:
        logger.critical(f"[+] Can't open the file {path} [+]")

def getFile(static_path):
    """Return the choosen object,
    if it exist unpickle the object else read csv, pickle and return the object.

    Arguments:
        file {str} -- file name => conf.STATIC_MEDECIN / conf.STATIC_TYPE_INTERVENTION
    """
    import pickle, os, conf, logging

    logger = conf._init_logger(logger=conf.LOGGER_UTILS)
    logger = logging.getLogger(conf.LOGGER_UTILS)
    try:
        pickle_format = ".pickle"
        path_csv = conf.FULL_PATH + static_path # Full path to the csv file
        path_pickle = conf.FULL_PATH + str(static_path).split(".")[0] + pickle_format # Full path to the pickle file

        # If the pickle file exist, load it and return it
        if(os.path.exists(path_pickle)):
            logger.info(f"[+] Unpickling {path_pickle} [+]")
            with open(path_pickle, "rb") as f:
                return pickle.load(f)
        # If not, load the data of the xml file, pickle it and return the obj
        else:
            logger.info(f"[+] Load and pickling {static_path} [+]")
            mObj = readXmlFile(static_path)
            with open(path_pickle, "wb") as f:
                pickle.dump(mObj, f)

            return mObj

    except Exception as e:
        logger.critical(f"[+] Can't find the file {static_path} [+]")
        logger.critical(e)

def constructHl7Orm(hlseven, patient, examen, medecin, type_intervention, RPPS, CODE_PRESC, dicom_mod):
    """
        Function that take in param the orm object for patient and examen
        return a fully constructed hl7 object
    """
    import conf
    # Construct the PID segment
    # ID_PATIENT^^^LOGICIEL_GAP
    hlseven.pid.pid_3 = str(patient[0]) + "^^^" + "NourauresConnector"
    # NOM_PATIENT^PRENOM_PATIENT
    hlseven.pid.pid_5 = str(patient[2] + "^" + patient[1])
    hlseven.pid.pid_7 = str(patient[4].strftime(
        conf.DT_FORMAT))  # DOB : YYYYMMDD
    # M : MALE / F : FEMALE / O : OTHER / U : UKNOWN
    hlseven.pid.pid_8 = "M" if str(patient[3]).lower() == "homme" else "F"

    # Construct the PV1 segment
    hlseven.pv1.pv1_2 = "O"  # O : OUTPUT
    hlseven.pv1.pv1_3 = "EXTERNE"  # EXTERNE
    # TODO IMPLEMENT
    # CODE_RADIOLOGGUE^^^^^^^^^^^^^RPPS
    hlseven.pv1.pv1_8 = str(RPPS) + "^^^^^^^^^^^^^RPPS"
    # DATE_ADMISSION : YYYYMMDDHHMMSS
    hlseven.pv1.pv1_44 = str(examen[2].strftime(conf.DT_FORMAT))

    # Construct the ORC segment
    hlseven.orc.orc_1 = "NW"  # Order Control NW
    hlseven.orc.orc_3 = str(examen[0])  # Filler Order Number NUMERO_EXAMEN
    hlseven.orc.orc_7 = "^^^" + \
        str(examen[2].strftime(conf.DT_FORMAT))  # ^^^DATE_ADMISSION
    # DATE_ADMISSION : YYYYMMDDHHMMSS
    hlseven.orc.orc_9 = str(examen[2].strftime(conf.DT_FORMAT))
    # TODO IMPLEMENT
    hlseven.orc.orc12 = str(CODE_PRESC) + "^" + str(medecin[1][1]) + "^" + str(medecin[1][1]) + \
        "^^^^^^^^^^" + \
        str(CODE_PRESC)  # CODE_PRESCRIPTEUR^NOM^PRENOM^^^^^^^^^^RPPS

    # Construct the OBR segment
    # CODE_EXAMEN^TITRE_EXAMEN
    hlseven.obr.obr_4 = str(
        type_intervention[0]) + "^" + str(type_intervention[1])
    """
    MODALITE :
        - CR : RADIO
        - CT : SCANNER
        - MR : IRM
        - XA : ANGIO
        - ES : ENDOSCOPIE
        - US : ECHOGRAPHIE
        - PX : PANORAMIQUE
    """
    hlseven.obr.obr_24 = dicom_mod  # Diagnostic Serv Sect ID, MODALITE
    hlseven.obr.obr_27 = "^^^" + \
        str(examen[2].strftime(conf.DT_FORMAT))  # ^^^DATE_ADMISSION

    return hlseven


if __name__ == "__main__":
    import conf
    print(conf.STATIC_TYPE_INTERVENTION)
    [print(x) for x in readXmlFile(conf.STATIC_TYPE_INTERVENTION)]
    print("\n\n\n")
    print(conf.STATIC_MEDECIN)
    [print(x) for x in readXmlFile(conf.STATIC_MEDECIN)]
