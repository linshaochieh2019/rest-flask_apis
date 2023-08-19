# Running app with development server vs. gunicorn

## Background
For local development, we can deploy our app to container using development mode and through volume. It's handy for development because they provide more information and support sync between local codes and codes running within the container.

However, the development server doesn't offer the best performance. Therefore when deploying prodcution app to the cloud, we should use gunicorn. Gunicorn is a server software that stands between browser and our app, and it can efficiently handle the requests. 

## Running app locally
We have to enter the command manually:
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" rest-apis-flask sh -c "flask run --host 0.0.0.0"

We have been using the first half of the command to use volume for development. Now we added the second half to let the local container know that we will be running locally, instead of using the CMD line written in the Dockerfile, as that's already for gunicorn

## Deploying app to the cloud
We have installed gunicorn, and edited the Dockerfile, as such, the cloud will run our app using gunicorn.