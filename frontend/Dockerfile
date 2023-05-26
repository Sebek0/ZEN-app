FROM node:17
LABEL tag="frontend"
COPY . /app
WORKDIR /app
RUN npm install yarn --force && yarn install
RUN yarn build
EXPOSE 80
CMD ["yarn", "preview", "--port", "3000", "--host"]
