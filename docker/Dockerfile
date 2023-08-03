FROM debian:bookworm-slim

ARG BUILD_DATE

LABEL maintainer="Géry Casiez <gery.casiez@univ-lille.fr>" \
	  description="Docker image for running the 1€ filter tests" \
	  version="1.0" \
	  org.label-schema.build-date=$BUILD_DATE

RUN apt-get update && apt-get install -y \
	sudo \
	python3 \
	python3-pip \
	g++

RUN pip install pandas argparse --break-system-packages
