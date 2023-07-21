TAG=${1:-latest}

docker run --rm -it \
    -p 5000:5000 \
    -v /etc/localtime:/etc/localtime:ro \
    -e OPENAI_KEY=YOUR_KEY_HERE \
    -v "$PWD":"/opt/chatpaper" \
     chatpaper:$TAG \
     conda run --no-capture-output --name chatpaper python3 app.py -d -vv