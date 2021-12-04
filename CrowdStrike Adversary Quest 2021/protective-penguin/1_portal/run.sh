#!/bin/sh
export FLAG=CS{foobar}
python3 -m http.server --cgi --bind 127.0.0.1
