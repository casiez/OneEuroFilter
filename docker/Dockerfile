FROM debian:trixie-slim

ARG BUILD_DATE

LABEL maintainer="Géry Casiez <gery.casiez@univ-lille.fr>" \
	  description="Docker image for running the 1€ filter tests" \
	  version="1.0" \
	  org.label-schema.build-date=$BUILD_DATE

RUN apt-get update && apt-get install -y \
	sudo \
	curl \
	wget \
	python3-full \
	python3-pip \
	g++ \
	openjdk-21-jdk \
	nodejs \
	npm \
	node-typescript \
	cargo \
	rustc \
	mono-mcs \
	mono-runtime

# Version of node provided by Debian is too old, so we install a more recent version using n
RUN npm install -g n
RUN n 26.13.1

RUN python3 -m venv /usr/local/python

ENV PATH="/usr/local/python/bin:$PATH"

RUN pip3 install pandas argparse --break-system-packages
