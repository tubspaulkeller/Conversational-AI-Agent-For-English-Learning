FROM python:3.8.12 AS BASE


WORKDIR /app

COPY requirements.txt .

#USER root


RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install rasa==3.3.0

COPY . .

CMD ["./bot.py"]



ADD config.yml config.yml
ADD domainDeployment.yml domain.yml
ADD credentials.yml credentials.yml
ADD endpoints.yml endpoints.yml

# By best practices, don't run the code with root user
#USER 1001