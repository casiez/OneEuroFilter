# Docker image

Docker image to test the implementations of the 1€ filter.

## Create the image

```
docker build -t oneeurofilter .
```

## Run

In the parent folder:
```
docker run -i -t -d --name=oneeurofilter_con --mount type=bind,source=.,target=/mnt/1euro oneeurofilter
```

## Connect

```
docker exec -it oneeurofilter_con /bin/bash
cd /mnt/1euro
make
```