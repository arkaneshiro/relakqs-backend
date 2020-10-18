# relakqs-backend
backend for relakqs

Check out relakqs here: [relakqs](https://relakqs.herokuapp.com)

Frontend for relakqs here: [relakqs](https://github.com/arkaneshiro/relakqs)

## Documentation Links
- [Feature List](https://github.com/arkaneshiro/relakqs/blob/master/Documentation/feature-list.md)
- [MVP](https://github.com/arkaneshiro/relakqs/blob/master/Documentation/mvp.md)
- [Front End Routes](https://github.com/arkaneshiro/relakqs/blob/master/Documentation/frontEndRoutes.md)
- [Back End Routes](https://github.com/arkaneshiro/relakqs/blob/master/Documentation/backEndRoutes.md)
- [Models](https://github.com/arkaneshiro/relakqs/blob/master/Documentation/models.md)

## Instructions to run locally
- clone repo
- run command "npm install"

- create database with some user, name, and password, enter appropriate info into .env file
- run command 'pipenv shell', then 'python seeder.py' to seed database
- make sure "socket.run(app, debug=True)" is uncommented in relakqs.py
- while still in the pipenv shell, run command 'python relakqs.py' to start server
