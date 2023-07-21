TAG=${1:-latest}

docker build -t chatpaper:$TAG  -f ./docker/Dockerfile .