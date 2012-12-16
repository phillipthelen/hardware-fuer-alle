## Über
Siehe den [Blogpost von @sofakissen](http://raummaschine.de/blog/2012/09/16/bedingungslos-gescheite-hardware-fuer-alle/)

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

1. Clone the Repo

    ```git clone https://github.com/vIiRuS/hardware-fuer-alle.git```

2. install the dependencies

    ```easy_install django django-allauth geopy django-gmapi sorl-thumbnail django-dajaxice django-dajax django-gravatar2```

3. Create the Database

    ```./manage.py syncdb``` _during this step the script will also create an admin user._

4. _(optional)_ populate the project with test data

    ```./manage.py populateTestUsers```

    ```./manage.py populateTestHardware```

5. Run the test server

    ```./manage.py runserver```

_Note: If python2 isn't your default Python version, you have to replace the easy-install command with the approriate command (i.e. easy-install-2.7 )_