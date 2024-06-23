#
# Application globals and utilities
#
# Indiana Wing CAF
# Jim Olivi 2024

import datetime
# from time import strptime
from tkinter import *
from tkcalendar import Calendar
import pandas as pd


#
# Make sure the program has enough information to proceed.
#

def check_params():
    print('Check CLI commands.')

    if App.start_date is not None:
        # check date formats
        try:
            start_date = datetime.datetime.strptime(str(App.start_date), '%m/%d/%y')
            end_date = datetime.datetime.strptime(str(App.end_date), '%m/%d/%y')
        except ValueError:
            print('invalid dates. Show user calendars.')
            start_date = datetime.datetime.now()
            end_date = start_date
        if start_date > end_date:
            print('Start date is after the end date.')
            start_date = datetime.datetime.now()
            end_date = start_date
    else:
        start_date = datetime.datetime.now()
        end_date = start_date

    root = Tk()

    # Set up the main parent window
    root.geometry("500x300")
    root.title('Required Parameters')

    production_mode = BooleanVar()
    production_mode.set(bool(App.production))
    production_checkbox = Checkbutton(root, text=': Production Mode', variable=production_mode, bg='white')
    production_checkbox.grid(column=1, row=0, pady=(10,10))

    year=start_date.year
    month=start_date.month
    day=start_date.day
    start_calendar = Calendar(root, selectmode='day', year=year, month=month, day=day, firstweekday='sunday')
    cal_start_label = Label(text="Start Date")
    cal_start_label.grid(column=1, row=2)
    start_calendar.grid(column=1, row=3, padx=(4,4))

    year=end_date.year
    month=end_date.month
    day=end_date.day
    end_calendar = Calendar(root, selectmode='day', year=year, month=month, day=day, firstweekday='sunday')
    cal_end_label = Label(text="End Date")
    cal_end_label.grid(column=2, row=2)
    end_calendar.grid(column=2, row=3, padx=(4,4))

    # def on_select(event):
    #     idx = event.widget.curselection()[0]
    #     selection = locations_list[idx]
    #     app.selected_location = selection[1]
    #     root.destroy()
    #
    def on_close():
        print("Exit clicked")
        root.destroy()

    # listbox.bind('<<ListboxSelect>>', on_select)
    root.protocol('WM_DELETE_WINDOW', on_close)

    root.mainloop()
    return False


class App:
    def __init__(self):

        print('App initialization begins')
        self.__production = False
        self.__password = ''
        self.__UserId = ''
        self.__orders_file = ''
        self.__start_date = None
        self.__end_date = None

        aircraft_file_name = 'aircraft.csv'
        try:
            self.aircraft_df = pd.read_csv(aircraft_file_name)
        except FileNotFoundError:
            raise FileNotFoundError('Pandas file not found: ' + aircraft_file_name)
        except:
            raise ReferenceError('Pandas file error: ' + aircraft_file_name)
        else:
            print('CAFRides utility successfully initialized.')

    def get_aircraft(self, aircraft):
        hh_designator = self.aircraft_df.loc[self.aircraft_df['Aircraft'] == aircraft]['HH_Designation'].values[0]
        return hh_designator

    @property
    def production(self):
        if self.__production:
            return True
        else:
            return False

    @property
    def UserId(self):
        return self.__UserId

    @property
    def password(self):
        return self.__password

    @property
    def orders_file(self):
        return self.__orders_file

    @property
    def start_date(self):
        return self.start_date

    @property
    def end_date(self):
        return self.end_date

    @start_date.setter
    def start_date(self, date):
        self.start_date = datetime.strptime(date, '%m/%d/%Y')

    @end_date.setter
    def end_date(self, date):
        self.end_date = datetime.strptime(date, '%m/%d/%Y')

    @password.setter
    def password(self, p):
        self.__password = p

    @production.setter
    def production(self, value):
        self.__production = value

    @UserId.setter
    def UserId(self, value):
        self.__UserId = value

    @orders_file.setter
    def orders_file(self,filename):
        self.__orders_file = filename

# selected_location = None
# access_token = os.environ['ACCESS_TOKEN']
#
# selected_start_date = None
# selected_end_date = None


