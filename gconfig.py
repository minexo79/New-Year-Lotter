import configparser

class GConfig:

    def __init__(self, _path: str) -> None:
        self.redEnvCount = 3
        self.minClick = 50
        self.maxClick = 100
        self.path = _path
        self.config = configparser.ConfigParser()

    def read(self):
        self.config.sections()
        self.config.read(self.path)

        self.redEnvCount = self.config.getint('DEFAULT', 'redEnvCount')
        self.minClick = self.config.getint('DEFAULT', 'minClick')
        self.maxClick = self.config.getint('DEFAULT', 'maxClick')

    def write(self):
        self.config['DEFAULT'] = {
            'redEnvCount': self.redEnvCount,
            'minClick': self.minClick,
            'maxClick': self.maxClick
        }

        with open(self.path, 'w') as configfile:
            self.config.write(configfile)