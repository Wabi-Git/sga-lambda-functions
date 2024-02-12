docker build -t sga-lambda-build --file lambda.Dockerfile .
docker create --name sga-lambda-build sga-lambda-build
docker cp sga-lambda-build:build_lambda/lambda.zip .
docker rm sga-lambda-build
