FROM python:3.8-buster
COPY ./ /app 
RUN pip install -r /app/requirements.txt 
ENV PYTHONPATH=/app/
EXPOSE 5000
ENTRYPOINT  ["python","/app/routes/rest.py"]
