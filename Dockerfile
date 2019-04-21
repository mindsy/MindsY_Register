FROM mindsy/flask:latest
COPY ./ ./src
WORKDIR ./src
RUN pip install -r requirements.txt
CMD python app.py
EXPOSE 5000
