rixb-webpy
==========

rixb powered by web.py

##a test

    $ wget https://github.com/RicterZ/rixb-webpy/archive/master.zip
    $ unzip master.zip && rm master.zip
    $ mv rixb-webpy-master rixb
    $ cd rixb/lib
    $ vi local-settings.py

then, set some parameters.

    database_type = 'mysql'
    MySQL_host = 'localhost'
    MySQL_user = 'root'
    MySQL_pass = 'xxx'
    MySQL_DB = 'rixb'
    
or 

    database_type = 'sqlite'
    sqlite_path = 'rixbdb.db'

and `esc :wq` to save it.
then,

    $ cd ..
    $ python init_db.py
    $ python main.py

and in the browser access `http://127.0.0.1:8080/`

