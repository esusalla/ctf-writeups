# Web

### Jar: actf{you_got_yourself_out_of_a_pickle}
- vulnerable to code injection through unpickling
- flag is stored in variable "flag"
- use "__reduce__" function of pickled class to define what gets run when it's unpickled

### Sea of Quills: actf{and_i_was_doing_fine_but_as_you_came_in_i_watch_my_regex_rewrite_f53d98be5199ab7ff81668df}
- use "cols" query param with UNION SQLi to leak table names
    - "name from sqlite_master union select url"
    - "* from flagtable union select url"
