FROM python:3.7

COPY sources/requirements.txt /
RUN ["/usr/local/bin/pip3", "install", "--upgrade", "pip", "-r", "requirements.txt"]

COPY sources /app
WORKDIR /app

EXPOSE 5000

CMD ["./docker-entrypoint.sh"]
