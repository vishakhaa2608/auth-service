FROM gcr.io/google_appengine/python

RUN virtualenv -p python3 /venv
ENV PATH /venv/bin:$PATH

ADD requirements.txt /app/requirements.txt
RUN /venv/bin/pip install --upgrade pip && /venv/bin/pip install -r /app/requirements.txt
ADD . /app

CMD python server.py