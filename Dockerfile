FROM mindsy/flask:latest

RUN mkdir /src

COPY app.py /src/app.py
COPY requirements.txt /src/requirements.txt 

WORKDIR /src

CMD pip install -r requirements.txt
CMD python app.py

EXPOSE 5000
