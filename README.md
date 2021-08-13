# Session 14 Readme file.


## Link to Colab file

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/payne101/P_14/blob/main/session14.ipynb)


## Question 1

We have to create generators that read a file and yield a row. One such generator is shown below. But first, we need a function to read and format values which are dates.

```python
def date(value):
    '''
    This function is used to format the column with date in it.
    It will take a string in the form 10/5/2016 and return datetime.date(2016, 10, 5)
    '''
    return parse(value).date()
```

Then, we create the generator function that yields one row at-a-time.

```python
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
```

The code can be executed as follows:

```python
info = gen_info('personal_info.csv')

for i in islice(info, 0,2):
    print(f'{i}\n')
```

Here, we used the `islice` function to return a subset (2 here) of the results.

## Question 2

We have to combine from all four generators

```python
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
```

The code can be executed as follows:

```python
record = gen_record()

for i in islice(record, 0,2):
    print(f'{i}\n')
```

## Question 3 

We have to identify stale records in our data i.e. which haven't been updated after 3/1/2017 

```python
def stale_record():
    '''
    This generator yields only data if the record has been updated
    after 3/1/2018.
    '''
    record = gen_record()
    for r in record:
        if r.last_updated > datetime.date(2018, 1, 3):
            yield r
```

## Question 4

We have to idenify most common car model by gender.

```python
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
```