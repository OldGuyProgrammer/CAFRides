#
# Application globals and utilities
#
# Indiana Wing CAF
# Jim Olivi 2024

import pandas as pd

class App:
    def __init__(self):
        aircraft_file_name = 'aircraft.json'
        try:
            self.aircraft_df = pd.read_json(aircraft_file_name, orient='index')
        except FileNotFoundError:
            raise FileNotFoundError('Pandas file not found: ' + aircraft_file_name)
        except:
            raise ReferenceError('Pandas file error: ' + aircraft_file_name)
        else:
            pass