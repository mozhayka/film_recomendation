FROM python:3.9

WORKDIR /app/python

ENV PYTHONPATH /app/python


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD ["python", "/app/python/src/chat/bot.py"]
