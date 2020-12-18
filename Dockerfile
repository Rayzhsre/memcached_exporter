FROM python:3
ADD . /opt
WORKDIR /opt/memcached_exporter
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "/opt/memcached_exporter/main.py" ]