from datetime import timedelta, datetime


class ShopDate():
    '''
    Everthing for dates
    '''
    std_format = "%Y-%m-%d"

    def __init__(self, filename: str):
        self._filename = filename
        self._today = self._read()

    @property
    def today(self):
        return self._today

    @today.setter
    def today(self, newdate):
        self._today = newdate

    @property
    def yesterday(self):
        return self.today + timedelta(days=-1)

    @property
    def current_month_range(self):
        '''Get the range of the days of the current month

        Returns:
        tuple -- first day of current month, last day of current month
        '''
        month = self.today.month + 1
        if month > 12:
            month = 1
            end = datetime(self.today.year,
                           month, 1) + timedelta(days=-1)
        return datetime(self.today.year, self.today.month, 1), end.day

    @staticmethod
    def get_range_month(input_date):
        ''' 
        Not used yet
        get the range of the dayes of the input month

        Returns:
        tuple -- first day of current month, last day of month in given day
        '''
        try:
            obj = datetime.strptime(input_date, "%Y-%m")
        except ValueError:
            print("Please check the date and format. Format has to be yyyy-mm")
            exit()
        month = obj.month + 1
        month = month if month <= 12 else 1

        start = datetime(obj.year, obj.month, 1)
        end = datetime(obj.year, month, 1) + timedelta(-1)

        return start, end

    @staticmethod
    def convert_str_to_datetime(datestr: str):
        '''Convert string to datetime object

        Arguments:
        datestr -- string in format [yyyy-mm] or [yyyy-mm-dd]
        '''
        try:
            return datetime.strptime(datestr, ShopDate.std_format)
        except ValueError as err:
            print(err)
            exit()

    @staticmethod
    def convert_datetime_to_str(datedt: datetime):
        '''Convert datetime object to string'''
        return datedt.strftime(ShopDate.std_format)

    def reset_date(self, save=True):
        '''Sets the today atribute to the system date'''
        self.today = datetime.today()
        if save:
            self._write(self.today)

    def shift(self, days: int, save: bool = True):
        '''Shifts the date by a number of days

        Arguments:
        days -- number of days to be shifted
        save -- does it need to be saved to the file, or just shift it for 
                this instance
        Default = True
        '''
        self.today += timedelta(days=days)
        if save:
            self._write(self.today)

    def _read(self):
        '''
        Read the file and set the date to the today atribute
        '''
        try:
            with open(self._filename, 'r') as filehandle:
                today = filehandle.read()
        except FileNotFoundError:
            with open(self._filename, 'w') as filehandle:
                today = datetime.today().strftime(ShopDate.std_format)
                filehandle.write(today)
        return datetime.strptime(today, ShopDate.std_format)

    def _write(self, newdate: datetime):
        '''
        Writes the newdate to the date file
        '''
        with open(self._filename, 'w') as filehandle:
            filehandle.write(newdate.strftime(ShopDate.std_format))
