from collections import namedtuple, Counter
from itertools import islice
from dateutil.parser import parse
import datetime

def date(value):
    '''
    This function is used to format the column with date in it.
    It will take a string in the form 10/5/2016 and return datetime.date(2016, 10, 5)
    '''
    return parse(value).date()   

def gen_info(file):
    '''
    this generator reads values from the 'personal_info.csv' file
    '''
    with open(file, encoding='utf8', errors='ignore') as f:
        # the first line is the header; this is used to
        # create the names for elements in the namedtuple
        header = next(f).strip().split(',')
        header = [x.replace(" ", "") for x in header]
        # data type for each column in the file
        data_type = [str, str, str, str, str]
        Info = namedtuple('Info', header )
        for line in f:
            line = line.strip().split(',')
            data = (type(field) for type, field in zip(data_type, line))
            yield Info(*data)

info = gen_info('personal_info.csv')

for i in islice(info, 0,2):
    print(f'{i}\n')


def gen_employ(file):
    '''
    this generator reads values from the 'employment.csv' file
    '''
    with open(file, encoding='utf8', errors='ignore') as f:
        # the first line is the header; this is used to
        # create the names for elements in the namedtuple
        header = next(f).strip().split(',')
        header = [x.replace(" ", "") for x in header]
        # data type for each column in the file
        data_type = [str, str, str, str]
        Employ = namedtuple('Employ', header )
        for line in f:
            line = line.strip().split(',')
            data = (type(field) for type, field in zip(data_type, line))
            yield Employ(*data)

employ = gen_employ('employment.csv')

for i in islice(employ, 0,2):
    print(f'{i}\n')


def gen_update(file):
    '''
    this generator reads values from the 'update_status.csv' file
    '''
    with open(file, encoding='utf8', errors='ignore') as f:
        # the first line is the header; this is used to
        # create the names for elements in the namedtuple
        header = next(f).strip().split(',')
        header = [x.replace(" ", "") for x in header]
        # data type for each column in the file
        data_type = [str, date, date]
        Update = namedtuple('Update', header )
        for line in f:
            line = line.strip().split(',')
            data = (type(field) for type, field in zip(data_type, line))
            yield Update(*data)

update = gen_update('update_status.csv')

for i in islice(update, 0,2):
    print(f'{i}\n')

def gen_vehicle(file):
    '''
    this generator reads values from the 'vehicles.csv' file
    '''
    with open(file, encoding='utf8', errors='ignore') as f:
        # the first line is the header; this is used to
        # create the names for elements in the namedtuple
        header = next(f).strip().split(',')
        header = [x.replace(" ", "") for x in header]
        # data type for each column in the file
        data_type = [str, str, str, int]
        Vehicle = namedtuple('Vehicle', header )
        for line in f:
            line = line.strip().split(',')
            data = (type(field) for type, field in zip(data_type, line))
            yield Vehicle(*data)

vehicle = gen_vehicle('vehicles.csv')

for i in islice(vehicle, 0,2):
    print(f'{i}\n')

def gen_record():
    '''
    This generator attempts to combine all data from the four files.
    First, the generators are initialized
    '''
    info = gen_info('personal_info.csv')
    employ = gen_employ('employment.csv')
    update = gen_update('update_status.csv')
    vehicle = gen_vehicle('vehicles.csv')

    # The four generators are zipped together
    for i, e, u, v in zip(info, employ, update, vehicle):
        Record = namedtuple('Record', 'ssn first_name last_name \
            gender language employer department employee_id last_updated created \
                vehicle_make vehicle_model model_year' )
        data = (*i, e.employer, e.department, e.employee_id, \
                    u.last_updated, u.created, \
                        v.vehicle_make, v.vehicle_model, v.model_year)
        yield Record(*data)

record = gen_record()

for i in islice(record, 0,2):
    print(f'{i}\n')

def stale_record():
    '''
    This generator yields only data if the record has been updated
    after 3/1/2018.
    '''
    record = gen_record()
    for r in record:
        if r.last_updated > datetime.date(2018, 1, 3):
            yield r

st_rec = stale_record()

for i in islice(st_rec, 0,2):
    print(f'{i}\n')


def car_gender():
    '''
    This function prints the most common car model used by males and females.
    after 3/1/2018.
    '''
    record = gen_record()
    male_cnt = Counter() # this counter keeps track of car models for males
    female_cnt = Counter() # this counter keeps track of car models for females
    for r in record:
        if r.gender == 'Male':
           male_cnt.update([r.vehicle_model])
        elif r.gender == 'Female':
           female_cnt.update([r.vehicle_model])
    print(f'Most Common Car for Male is {male_cnt.most_common(1)[0][0]} with a count of {male_cnt.most_common(1)[0][1]}')
    print(f'Most Common Car for Female is {female_cnt.most_common(1)[0][0]} with a count of {female_cnt.most_common(1)[0][1]}')

car_gender()