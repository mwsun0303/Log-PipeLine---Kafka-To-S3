DOCKER_FILE="Dockerfile"
CONTAINER_NAME="kafka_to_s3"
IMAGE_NAME="${CONTAINER_NAME}_image"

echo "[INFO] -------------------------- "
echo "[INFO] Old Container Remove "
echo "[INFO] -------------------------- "
    docker ps -a --filter "name=$CONTAINER_NAME" --format "{{.ID}}" | xargs -r docker rm -f
    echo "[INFO] Old Container Remove Check"
        docker ps -a

echo "[INFO] -------------------------- "
echo "[INFO] $CONTAINER_NAME Build Start "
echo "[INFO] -------------------------- "
    docker build -t $IMAGE_NAME -f $DOCKER_FILE .

echo "[INFO] -------------------------- "
echo "[INFO] $CONTAINER_NAME Docker Container Run "
echo "[INFO] -------------------------- "
    CONTAINER_ID=$(docker run -d -v $MOUNT_PATH:$MOUNT_PATH --name $CONTAINER_NAME $IMAGE_NAME)
    echo "[INFO] Container started with ID: $CONTAINER_ID"

echo "[INFO] -------------------------- "
echo "[INFO] Container Log 10sec"
echo "[INFO] -------------------------- "
    timeout 10 docker logs -f $CONTAINER_ID

echo "[INFO] -------------------------- "
echo "[INFO] Deploy Success"
echo "[INFO] -------------------------- "