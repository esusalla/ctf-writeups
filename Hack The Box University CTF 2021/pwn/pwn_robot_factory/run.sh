#!/usr/bin/env sh

docker build -t robot_factory . && docker run -it --rm -p 5000:5000 robot_factory
