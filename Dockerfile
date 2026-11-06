FROM python:3.15-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_DEBUG=0
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]
