import psycopg2
from itemadapter import ItemAdapter

class PostgresPipeline:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("POSTGRES_HOST"),
            database=crawler.settings.get("POSTGRES_DATABASE"),
            user=crawler.settings.get("POSTGRES_USER"),
            password=crawler.settings.get("POSTGRES_PASSWORD"),
            port=crawler.settings.get("POSTGRES_PORT"),
        )

    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
        )
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS flats(
            id serial PRIMARY KEY, 
            title text,
            image_url text
        )
        """)

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute("insert into flats (title, image_url) values (%s, %s)", 
            (item["title"], item["image_url"]))
        self.connection.commit()

        return item

   

