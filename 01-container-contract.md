# Container Contract

The container must expose one stable process, listen on `0.0.0.0`, and provide
separate liveness and readiness routes. Liveness answers whether the process can
serve HTTP. Readiness answers whether its configuration is usable; it should not
perform a paid generation call.

![Docker architecture showing clients, the Docker host, images, containers, and a registry](assets/docker-architecture.png)

*Source: [Docker architecture](https://commons.wikimedia.org/wiki/File:Docker-architecture.png), Wikimedia Commons; CC BY-SA 4.0, by dc.*

## Practice

Build and run the image, then inspect all three API routes:

```bash
docker compose up --build
```

Keep Compose running and use another terminal for the requests:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain container readiness briefly."}'
```

Change the Docker command so it binds only to `127.0.0.1`. Explain why the host
can no longer reach it through the published port, then restore the command.

## Reference Answer

A process bound to container loopback accepts traffic only from inside that
container. Binding to `0.0.0.0` allows the container network interface to
receive traffic forwarded through the published port or cloud load balancer.
