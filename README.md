# luxonis-scraper

## Instructions
Simply cloning the repository and running ``docker-compose up`` should the trick - the result is then available on localhost:8080.

### Some issues
- Sometimes, despite the scraper's database dependency, the scraper runs before the database is set up. If that's the case, just run the ``docker-compose up`` command again.
- I've encountered issues on my Arch Linux machine, where the database "sreality" is not created and the user needs to connect to the database container and create it manually