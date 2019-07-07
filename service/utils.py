import csv

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

def readXmlFile(xmlPath):
    import conf
    """
        Take a path into the param and convert the xml file into a python object
    """
    try:
        logger = conf._init_logger()
        obj = []
        path = conf.FULL_PATH+xmlPath

        with open(path, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                obj.append(row)
        logger.info(f"[+] Successfully loaded {path}")

        if xmlPath == conf.STATIC_MEDECIN:
            [obj.remove(obj[x]) for x in range(0, 4, 1)]
            obj = list(filter(lambda x: x != [";;;"], obj))
            obj = list(map(lambda x: x[0].split(";"), obj))

        if xmlPath == conf.STATIC_TYPE_INTERVENTION:
            obj.remove(obj[0])
            obj = list(filter(lambda x: x != [";;;"], obj))
            obj = list(map(lambda x: x[0].split(";"), obj))

        return obj
    except:
        logger.critical(f"[+] Can't open the file {path} [+]")

if __name__ == "__main__":
    import conf
    print(conf.STATIC_TYPE_INTERVENTION)
    [print(x) for x in readXmlFile(conf.STATIC_TYPE_INTERVENTION)]
    print("\n\n\n")
    print(conf.STATIC_MEDECIN)
    [print(x) for x in readXmlFile(conf.STATIC_MEDECIN)]
