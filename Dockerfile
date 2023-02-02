
#FROM centos
FROM centos:7.9.2009

WORKDIR /API

ADD main.py /API/


RUN yum -y install wget &&\
    yum install -y centos-release-scl &&\
    yum install -y rh-python38 which  &&\
    cp /opt/rh/rh-python38/root/usr/bin/python3 /usr/bin/python3 &&\
    cp /opt/rh/rh-python38/root/usr/bin/pip3 /usr/bin/pip3

RUN pip3 install fastapi -i https://pypi.douban.com/simple &&\
    pip3 install "uvicorn[standard]" -i https://pypi.douban.com/simple &&\
    pip3 install jwt -i https://pypi.douban.com/simple
