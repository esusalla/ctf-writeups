- given the source code for a Flask application that acts like a todo list
- a lot of different routes and functions to inspect, but the important part is that there is an API endpoint at `/api/list/all/` that will list all todos for all users as long as the request passes the `verify_integrity` decorator check
- the `verify_integrity` check only makes sure that the `?secret=<secret>` parameter in the request URL is correct for the `assignee` in the URL
- the `/api/list/all/` endpoint does not have an `assignee`, so passing any valid secret allows you to view all todos and retrieve the flag

#### Tags: Flask, broken auth
