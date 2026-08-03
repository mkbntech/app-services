# --- build stage ---
FROM golang:1.22-alpine AS build
WORKDIR /src
COPY go.mod go.sum ./
COPY main.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/recommendation-service .

# --- runtime stage ---
FROM gcr.io/distroless/static-debian12
COPY --from=build /out/recommendation-service /recommendation-service
ENV PORT=8002
EXPOSE 8002
USER 65532:65532
ENTRYPOINT ["/recommendation-service"]
