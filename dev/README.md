This docker-compose configuration to be used **only** for development purpose.

**NOTE:** Unless otherwise stated, all files and commands are with respective to the `dev` directory.

## Generating the Private and Public Key

**NOTE:** The names `<private_key_filename>` and `<public_key_filename>` are templates for whatever names you choose.

- Generate the private key and save it in `<private_key_filename>`:

  ```sh
  openssl ecparam -name prime256v1 -genkey -noout -out <private_key_filename>
  ```

- Encode the private key as a base64 string:
  ```sh
  base64 -w 0 <private_key_filename>
  ```
- Copy this value and save it as the `JWT_ECDSA_PRIVATE_KEY` variable.

- Generate the public key and save it in `<public_key_filename>`:

  ```sh
  openssl ec -in <private_key_filename> -pubout > <public_key_filename>
  ```

- Encode the public key as a base64 string

  ```sh
  base64 -w 0 <public_key_filename>
  ```

- This value will be used as the `JWT_ECDSA_PUBLIC_KEY` variable in the services that will verify the JWT.

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
- `GOOGLE_CLIENT_ID`: Google client ID for OAuth2 integration
- `GOOGLE_CLIENT_SECRET`: Google client secret for OAuth2 integration
- `JWT_ECDSA_PRIVATE_KEY`: Private key for generating JWT.
- `JWT_ECDSA_PUBLIC_KEY`: Public key for verifying JWT.
- `JWT_EXPIRY_DURATION `: How long JWT should last (default: 3h)

### admin-http-server
- `DEBUG`: Whether to be verbose in log output.
