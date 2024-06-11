#
# Application globals and utilities
#
# Indiana Wing CAF
# Jim Olivi 2024

import pandas as pd


class App:
    def __init__(self):

        self.__production = False
        self.__password = ''
        self.__UserId = ''

        aircraft_file_name = 'aircraft.csv'
        try:
            self.aircraft_df = pd.read_csv(aircraft_file_name)
        except FileNotFoundError:
            raise FileNotFoundError('Pandas file not found: ' + aircraft_file_name)
        except:
            raise ReferenceError('Pandas file error: ' + aircraft_file_name)
        else:
            pass

    def get_aircraft(self, aircraft):
        hh_designator = self.aircraft_df.loc[self.aircraft_df['Aircraft'] == aircraft]['HH_Designation'].values[0]
        return hh_designator

    @property
    def production(self):
        return self.__production

    @property
    def UserId(self):
        return self.__UserId

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, p):
        self.__password = p

    @production.setter
    def production(self, value):
        self.__production = value

    @UserId.setter
    def UserId(self, value):
        self.__UserId = value
# selected_location = None
# access_token = os.environ['ACCESS_TOKEN']
#
# selected_start_date = None
# selected_end_date = None


