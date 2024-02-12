FROM public.ecr.aws/lambda/python:3.9-x86_64

WORKDIR /build_lambda

COPY requirements.txt /build_lambda

RUN pip install --upgrade pip --no-cache-dir \
    && pip install --no-cache-dir -r requirements.txt --target .\
    && rm -f requirements.txt

COPY /lambda_functions /build_lambda/lambda_functions
COPY lambda_function.py /build_lambda

RUN yum update -y && yum install -y zip \
    && zip -r lambda.zip . \
    && yum remove -y zip \
    && yum clean all
