#!/bin/bash

# Build image from Dockerfile
docker build -t nabilanavabIlovepdf .

# Run container from the built image
docker run -it --rm nabilanavabIlovepdf
