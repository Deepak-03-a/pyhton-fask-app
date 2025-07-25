FROM python:3.10-slim
WORKDIR /app
COPY app.py .
RUN pip install flask psycopg2-binary
EXPOSE 5000
CMD ["python", "app.py"]
