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

if __name__ == "__main__":
    import conf
    print(conf.STATIC_TYPE_INTERVENTION)
    [print(x) for x in readXmlFile(conf.STATIC_TYPE_INTERVENTION)]
    print("\n\n\n")
    print(conf.STATIC_MEDECIN)
    [print(x) for x in readXmlFile(conf.STATIC_MEDECIN)]
