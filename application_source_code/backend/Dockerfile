# Setting the base image.
FROM node:slim as build

# Setting node environment 
ENV NODE_ENV production

# Setting application path
WORKDIR /app

# Transferring package dependencies to application folder
COPY package.json .
COPY yarn.lock .

# Installing the application dependencies.
RUN yarn install --production

# Copying other application files 
COPY . .

EXPOSE 5000

CMD npm start

