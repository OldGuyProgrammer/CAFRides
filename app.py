#
# Application globals and utilities
#
# Indiana Wing CAF
# Jim Olivi 2024

import datetime
import tkinter.messagebox
from tkinter import *
from tkcalendar import DateEntry
import pandas as pd


#
# Make sure the program has enough information to proceed.
#

def check_date_order(start_date, end_date):
    if start_date > end_date:
        return False
    else:
        return True


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
        if not check_date_order(start_date, end_date):
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

    cal_start_label = Label(text="Start Date")
    cal_start_label.grid(column=1, row=2)
    start_date_picker = DateEntry(root, date_pattern='mm/dd/yy')
    start_date_picker.set_date(start_date)
    start_date_picker.grid(column=1, row=3)

    cal_end_label = Label(text="End Date")
    cal_end_label.grid(column=2, row=2)
    end_date_picker = DateEntry(root, date_pattern='mm/dd/yy')
    end_date_picker.set_date(end_date)
    end_date_picker.grid(column=2, row=3, padx=(4,4))

    # def on_select(event):
    #     idx = event.widget.curselection()[0]
    #     selection = locations_list[idx]
    #     app.selected_location = selection[1]
    #     root.destroy()
    #
    def on_close():
        App.abort = True
        root.destroy()

    # listbox.bind('<<ListboxSelect>>', on_select)
    root.protocol('WM_DELETE_WINDOW', on_close)

    def set_params_button_clicked():
        App.production = production_mode.get()
        start = start_date_picker.get_date()
        end = end_date_picker.get_date()
        if check_date_order(start, end):
            App.start_date = start_date_picker.get_date()
            App.end_date = end_date_picker.get_date()
            root.destroy()
        else:
            msg = 'Start date is after the end date.'
            print(msg)
            tkinter.messagebox.showwarning(title='Date Problem', message='Start date must be before end date.')

    set_params_button = Button(root, text="Save All Parameters and get square data", command=set_params_button_clicked)
    set_params_button.grid(column=2, row=4)

    root.mainloop()


class App:
    def __init__(self):

        print('App initialization begins')
        self.__production = False
        self.__password = ''
        self.__UserId = ''
        self.__orders_file = ''
        self.__start_date = None
        self.__end_date = None
        self.__abort = False

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

    @property
    def abort(self):
        if self.__abort:
            return True
        else:
            return False

    @abort.setter
    def abort(self, flag):
        self.__abort__ = flag

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


