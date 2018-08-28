FROM postgres:10
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
COPY ./docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/
