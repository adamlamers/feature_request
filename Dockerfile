FROM ubuntu:latest
MAINTAINER Adam Lamers "adamlamers@gmail.com"
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev virtualenv
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
