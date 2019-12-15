FROM python:3.8-buster
COPY ./ /app 
RUN pip install /app/requirements.txt 
CMD [python,/app/src/main.py]
