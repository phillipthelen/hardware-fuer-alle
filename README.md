## About

For more information about this project read the [blogpost from @sofakissen](http://raummaschine.de/blog/2012/09/16/bedingungslos-gescheite-hardware-fuer-alle/). _(it's written in german)_

[![Build Status](https://travis-ci.org/vIiRuS/hardware-fuer-alle.png?branch=master)](https://travis-ci.org/vIiRuS/hardware-fuer-alle)

## Dependencies
* Django 1.4
* django-allauth
* geopy
* django-gmapi
* sorl-thumbnail
* django-dajaxice
* django-dajax
* django-gravatar2

## Installation

_We assume in the following you have [Python](http://www.python.org) and [setuptools](http://pypi.python.org/pypi/setuptools) installed. If python2 isn't your default Python version, you have to replace the easy\_install command with the approriate command (i.e. ```easy-install-2.7```)_

### 1. Clone the Repo

```git clone https://github.com/vIiRuS/hardware-fuer-alle.git```

### 2. Install the dependencies

```pip install -r dependencies.txt```

### 3. Create ```hfa/settings.py```

Copy and rename the ```hfa/settings.example.py``` and configure it to your local needs.

### 4. Create the Database

```./manage.py syncdb``` _during this step the script will also create an admin user_

### 5. _(optional)_ Populate the project with test data

```./manage.py populateTestUsers```

```./manage.py populateTestHardware```

### 6. Run the test server

```./manage.py runserver```

### 7. Run the unittests

```./manage.py test main hardware users```
