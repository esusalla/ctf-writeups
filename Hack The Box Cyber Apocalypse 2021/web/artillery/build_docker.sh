#!/bin/bash
docker rm -f web_artillery
docker build -t web_artillery . && \
docker run --name=web_artillery --rm -p1337:8080 -it web_artillery
