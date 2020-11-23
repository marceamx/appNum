# builder image
FROM golang:1.13-alpine3.11 AS builder
MAINTAINER "El viejo marceamx@gmail.com"

RUN mkdir /build
ADD *.go /build/
WORKDIR /build
RUN GOOS=linux GOARCH=amd64 go build -tags netgo -o app

FROM alpine:latest 

RUN mkdir /app
WORKDIR /app
COPY --from=builder /build/app .

EXPOSE 8080
ENTRYPOINT ["/app/app"]
