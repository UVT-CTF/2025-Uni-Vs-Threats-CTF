#!/bin/bash
docker build -t go_4_it . && docker run -p 40048:40048 go_4_it:latest
