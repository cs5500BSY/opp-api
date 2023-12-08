
docker rm mycontainer
pip install -r requirements.txt
docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage
