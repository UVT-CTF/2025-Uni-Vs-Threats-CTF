#!/bin/bash

docker build -t query_it . && docker run -p 40049:80 query_it
