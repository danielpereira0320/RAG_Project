APP_DIR=$(pwd)
echo "APP_PATH=$APP_DIR" > .env
docker-compose down
docker-compose --env-file .env up -d --build
