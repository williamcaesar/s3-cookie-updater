FROM alpine:3.9
MAINTAINER William Caesar
RUN apk add --no-cache python3 && pip3 install minio
WORKDIR .
COPY compare.py /home/compare.py
COPY run.py /home/run.py
COPY run.sh /home/run.sh
COPY updater.py /home/updater.py
COPY credentials.json /home/credentials.json
RUN chmod +x /home/run.sh
VOLUME /home/cookies/
CMD sh /home/run.sh

