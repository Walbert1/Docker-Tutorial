# Docker To-Do Tutorial

A small to-do application with a FastAPI backend and an Nginx-served frontend. The frontend calls the backend API from your browser.

## Project layout

```text
.
├── BE/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/mysite/main.py
└── FE/
    ├── Dockerfile
    └── static/index.html
```

## Prerequisites

- Docker Desktop (or Docker Engine) running
- A terminal opened in the project root

## Build the images

The final argument to `docker build` is the build context. These commands use each component's directory as its context, so its Dockerfile can copy its own files:

```bash
docker build -t docker-tutorial-backend ./BE
docker build -t docker-tutorial-frontend ./FE
```

`-t` assigns a name (tag) to the built image.

## Start the containers

Start the backend:

```bash
docker run -d --name docker-tutorial-backend -p 8000:8000 docker-tutorial-backend
```

Start the frontend in a second terminal:

```bash
docker run -d --name docker-tutorial-frontend -p 8080:80 docker-tutorial-frontend
```

Here, `-d` runs a container in the background, `--name` gives it a convenient name, and `-p HOST_PORT:CONTAINER_PORT` publishes a container port on your computer.

Open the app at <http://localhost:8080>. The frontend sends API requests to `http://localhost:8000/api/todos`, so keep the backend running and published on port `8000`.

Container names must be unique. If you already have containers with these names, stop and remove those specific containers before creating replacements:

```bash
docker rm -f docker-tutorial-backend docker-tutorial-frontend
```

## Use the API

List all tasks:

```bash
curl http://localhost:8000/api/todos
```

Add a task:

```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"name":"Learn Docker"}'
```

Get a task by its ID (replace `1` with an ID returned by the API):

```bash
curl http://localhost:8000/api/todos/1
```

Delete a task:

```bash
curl -X DELETE http://localhost:8000/api/todos/1
```

The API documentation is available at <http://localhost:8000/docs>, and its health endpoint is <http://localhost:8000/api/health>.

## Inspect and manage containers

Show running containers and their port mappings:

```bash
docker ps
```

Show application logs:

```bash
docker logs docker-tutorial-backend
docker logs docker-tutorial-frontend
```

Stop the containers:

```bash
docker stop docker-tutorial-frontend docker-tutorial-backend
```

Start those stopped containers again:

```bash
docker start docker-tutorial-backend docker-tutorial-frontend
```

## Notes

- Tasks are stored in memory by the backend. They are lost when the backend container is removed or restarted.
- The frontend's API URL is set to `http://localhost:8000`; this setup is intended for local development where the browser and Docker host are the same machine.
