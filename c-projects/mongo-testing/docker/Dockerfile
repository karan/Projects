FROM ubuntu:bionic
RUN apt -y update && apt -y upgrade && apt -y install build-essential libmongoc-1.0-0
COPY ../* /usr/local/src
WORKDIR /usr/local/src
RUN ./make
ENTRYPOINT ./main


