TAG=$1

docker tag chatpaper:latest panda1024/chatpaper:${TAG}
docker push panda1024/chatpaper:${TAG}