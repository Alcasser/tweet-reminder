FROM python:3.8.3-slim-buster
WORKDIR /reminder-bot/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat screen

RUN pip install --upgrade pip
# Copy requirements file to /reminder-bot/app/pip_requirements.txt
COPY pip_requirements.txt pip_requirements.txt
# And install requirements. Before copying all source code.
RUN pip install -r pip_requirements.txt

COPY . .

COPY scripts/run-app.sh /run-app.sh
RUN chmod +x /run-app.sh

CMD /run-app.sh