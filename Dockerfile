FROM python:3.8
WORKDIR /app
COPY . /app
COPY ./db/init.sql /docker-entrypoint-initdb.d/
RUN pip install scrapy scrapy_playwright psycopg2-binary
RUN playwright install
RUN playwright install-deps
EXPOSE 8080
CMD [ "python", "scraper/main.py" ]