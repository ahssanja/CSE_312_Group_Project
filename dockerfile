FROM node:16-slim

ENV HOME /root
WORKDIR /root

COPY package*.json ./

RUN npm install --only=production

COPY . .

EXPOSE 8080

CMD [ "node", "server.js" ]
