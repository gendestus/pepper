FROM laudio/pyodbc:3.0.0

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]