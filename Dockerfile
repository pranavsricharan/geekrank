FROM ubuntu:18.04
EXPOSE 5000
RUN apt-get update && apt-get install -y python3 gcc python3-pip
WORKDIR /app
COPY execution-service .
RUN pip3 install -r requirements.txt
RUN echo "gunicorn -b 0:5000 -w 3 -t 120 app:app" > startup.sh
ENTRYPOINT ["bash", "startup.sh"]
