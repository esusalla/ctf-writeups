- inspecting the source for the webpage reveals comments that include an endpoint that takes an `id` parameter, `/portfolio?id=`
- navigating to the endpoint and testing it for SQL injection reveals it's a SELECT query with an injection vulnerability at the end
- ending up enumerating the databases and exfiltrating data that wasn't needed
```
# list databases
1 union select 1,schema_name,1 from information_schema.schemata

# list table names from specific DB
1 union select 1,table_name,1 from information_schema.tables where table_schema = 'freelancer'

# list columns in from specific table
1 union select 1,column_name,1 from information_schema.columns where table_name = 'safeadmin'

# retrieve specific columns from specific table
1 union select 1,username,password from safeadmin
```
- intended method was to use `load_file` for LFI
```
# retrieve known file
1 union select 1,2,load_file('/etc/passwd')
```
- response headers reveal the server is using Apache, can read the config file at `/etc/apache2/apache2.conf`
- the Apache config reveals the root web directory is located at `/var/www/html`
- easy to read JavaScript and CSS files from here, but PHP files are unable to be read without first base64 encoding
```
# retrieve known file and base64 encode
1 union select 1,2,to_base64(load_file('/var/www/html/portfolio.php'))
```
- retrieving the source code for `portfolio.php` reveals the existence of `/var/www/html/administrat/include/config.php`
- reading the config reveals the `db_user` password that's not used
- navigating to `http://<host>:<port>/administrat` shows a login page
- we can confirm the `safeadm` user exists, but am not able to crack their password in order to login (both from the previously mentioned database enumeration)
- inspecting the HTML source for the `/administrat` homepage shows that it makes a POST request to `/administrat/index.php`
- pulling this file and reading it shows that it redirects to `/administrat/panel.php` after logging in
- the flag is embedded in the admin panel and can be read by retrieving the panel file

#### Tags: SQL injection (SELECT statement), LFI
