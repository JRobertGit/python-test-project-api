FROM python:3.9
WORKDIR /python_test
ADD . /python_test

RUN pip install psycopg2-binary
RUN pip install redis
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 5000
ENTRYPOINT [ "sh", "scripts/dev.sh" ]