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

# ARG REACT_APP_BACKEND_IP

# ENV REACT_APP_BACKEND_IP $REACT_APP_BACKEND_IP

# Building production package.
RUN yarn build

# production environment
FROM nginx:stable-alpine3.17 as production
ENV NODE_ENV production

# Copying built package to nginx
COPY --from=build /app/build /usr/share/nginx/html

COPY run.sh /config/run.sh

RUN chmod +x /config/run.sh

# Copying nginx.conf file to nginx conf default path.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposing port needed for application
EXPOSE 80

ENTRYPOINT ["/bin/sh", "/config/run.sh"]

