This docker-compose configuration to be used **only** for development purpose.

**NOTE:** Unless otherwise stated, all files and commands are with respective to the `dev` directory.

## List of services

### frontend-http-server

This container is a RESTful API web server linked to its database.
It provides the endpoints for regular users to interact with the library.

### frontend-grpc-server
This container is a gRPC server linked to the same database as the `frontend-http-server`. It provides the endpoints for the admin to update/delete books
from the library.

### frontend-postgresqldb

This container is a PostgreSQL DB shared by the `frontend-http-server` and `frontend-grpc-server`. DB data is kept in a volume, persistent across containers restarts.

### admin-http-server
This container is a RESTful API web server that allows the admin to perform
CRUD operations on the `frontend` service.

## Starting the services

```sh
docker compose up --build
```

## Environment variables

### frontend-grpc-server
### frontend-http-server

- `POSTGRES_URI`: PostgreSQL DSN string
- `DEBUG`: Whether to be verbose in log output.
- `MAX_PAGE_SIZE`: Maximum number of items to return from a request/query (default: 20)
- `GRPC_SERVER_PORT`: Port to run the gRPC server.

### admin-http-server
- `DEBUG`: Whether to be verbose in log output.
