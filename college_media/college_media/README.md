"# College_media" 
python -m venv myenv
myenv\Scripts\activate

requirements:
1) Sending mail when the student login the website for the first time

1-Add studen single,multi
2-post accept and reject


about docker
pip install -r requirements.txt
__________________________
star the docker
->docker-compose up -d
check for running 
-> docker ps 
accessing resis
->docker exec -it college_media-redis-1 redis-cli
->PING

torun the project
-> daphne -b 127.0.0.1 -p 8000 college_media.asgi:application
