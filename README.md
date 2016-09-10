# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

# DB Helper Tools #
* db_extract.py  - for viewing DB entries
* db_helper.py   - helper function module
* test_db.py     - unit test for helper function module
* db_tables.py   - table column definitions
* delete_dbs.bat - batch script for deleting all .db files in the directory
* gen_info.py    - scenario convert tool info ini generator
* gen_query.py   - sql file generator


### How do I get set up? ###

####1. Copy DB files in the path:####
* 3G_VER_INFO.db 
> rename VER_INFO.db from 3G DB folder to 3G_VER_INFO.db
* VER_INFO.db
* cp_combo_name.db
* cp_end_name.db
* cp_macro_name.db
* cp_para_name.db
* cp_para_atr.db
* cp_str_ptr.db

####2. Syntax####

* python db_extract.py <macro no> \[detail level\]
    show basic: `python db_extract.py 1247
    show basic: `python db_extract.py 1247 0
    show detailed: `python db_extract.py 1247 1


### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

### To Follow ###
* Add docopt implementation
* Dynamic DB Location
* How to run tests