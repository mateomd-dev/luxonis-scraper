import os
import psycopg2

from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "0.0.0.0"
PORT = 8080

def get_records():
    # Hardcoded
    hostname = '172.18.0.2'
    username = 'admin'
    password = 'admin'
    database = 'sreality'

    connection = None
    try:
        connection = psycopg2.connect(
            user=username,
            password=password,
            host=hostname,
            dbname=database
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM flats")

        return cursor.fetchall()
    except(Exception, psycopg2.Error) as error:
        print("Error: ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Closing the db connection...")

def swag_up():
    style = "<style>"
    style += "h1 {text-align: center;}"
    style += ".offer {display: flex; flex-direction: column; align-items: center; margin: 10px;}"
    style += ".offer img {width: 150px; height: 150px; margin-bottom: 10px;}"
    style += ".offer h2 {font-size: 14px; margin: 0;}"
    style += ".grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); grid-gap: 20px;}"
    style += "</style>"

    return style

class ServerRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        records = get_records()

        response = "<html><head>"
        response = "<meta charset=\"utf-8\">"
        response += swag_up() + "</head><body>"
        response += "<h1>SREALITY - FLATS FOR SALE</h1>"
        response += "<div class=\"grid\">"
        for i, record in enumerate(records):
            title = record[1]
            image_url = record[2]
            response += "<div class=\"offer\"><img src={src}><h2>Flat #{id}</h2><h2>{title}</div>".format(id=i, src=image_url, title=title)
        response += "</div>"
        response += "</body></html>"

        self.wfile.write(response.encode())

server = HTTPServer((HOST, PORT), ServerRequestHandler)
print("Server now running...")
server.serve_forever()

server.server_close()
print("Stopping the server...")
