#
# Application globals and utilities
#
# Indiana Wing CAF
# Jim Olivi 2024

import pandas as pd

class App:
    def __init__(self):
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
