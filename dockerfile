# The vm we are wroking with
FROM python:3.8

# Change the home directory and working directory to the /root folder
ENV HOME /root
WORKDIR /root

# Running a shell command to download the neccesary dependancies for the pymongo
RUN python -m pip install pymongo
RUN apt install python3-django

# Copy all the contents from this working directory into the VM's working directory
COPY . .

# The VM will be accessible on port 8080
EXPOSE 8015

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python3 -u main.py