# syntax=docker/dockerfile:1
LABEL org.opencontainers.image.source=https://github.com/elfkuzco/locallibrary
LABEL org.opencontainers.image.description="Locallibrary Admin Service"
LABEL org.opencontainers.image.licenses=MIT

ARG GO_VERSION=1.21
ARG APP_VERSION="v0.0.0+unknown"
ARG BUILDTIME="1970-01-01T01:00:00+01:00"

FROM golang:${GO_VERSION} AS base
WORKDIR /src
# Install the dependencies
RUN --mount=type=cache,target=/go/pkg/mod/ \
    --mount=type=bind,source=go.sum,target=go.sum \
    --mount=type=bind,source=go.mod,target=go.mod \
    go mod download -x

# Build the server client
FROM base AS build-server
ARG APP_VERSION
ARG BUILDTIME
RUN --mount=type=cache,target=/go/pkg/mod/ \
    --mount=type=bind,target=. \
    GOOS=linux CGO_ENABLED=0 go build \
    -ldflags="-s -X main.buildTime=${BUILDTIME} -X main.version=${APP_VERSION}" \
    -o /bin/server ./cmd/api_server

# Copy the server binary
FROM gcr.io/distroless/static-debian12 AS server
COPY --from=build-server /bin/server /bin/
CMD ["/bin/server"]
