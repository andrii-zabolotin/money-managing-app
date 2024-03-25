FROM ubuntu:latest
LABEL authors="fenic"

ENTRYPOINT ["top", "-b"]