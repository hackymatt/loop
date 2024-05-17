FROM node:18-alpine as BUILD_IMAGE

WORKDIR /usr/src/app/frontend

COPY package.json package-lock.json ./

# install dependencies
RUN npm install

COPY . .

ARG API_URL=http://dev.loop.edu.pl/api
ENV NEXT_PUBLIC_API_URL=$API_URL

ARG BASE_URL=http://dev.loop.edu.pl
ENV NEXT_PUBLIC_BASE_URL=$BASE_URL

ARG GOOGLE_CLIENT_ID=617166587683-r77p1ri68pjhff6fd9032ak42qjq0v7j.apps.googleusercontent.com
ENV NEXT_PUBLIC_GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID

ARG FACEBOOK_CLIENT_ID=1576703186506729
ENV NEXT_PUBLIC_FACEBOOK_CLIENT_ID=$FACEBOOK_CLIENT_ID

ARG GITHUB_CLIENT_ID=802861860d8aee939ba2
ENV NEXT_PUBLIC_GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID

ARG GITHUB_REPO=https://github.com/loopedupl/
ENV NEXT_PUBLIC_GITHUB_REPO=$GITHUB_REPO

# build
RUN npm run build

# remove dev dependencies
RUN npm prune --production

FROM node:18-alpine

WORKDIR /usr/src/app/frontend

# copy from build image
COPY --from=BUILD_IMAGE /usr/src/app/frontend/package.json ./package.json
COPY --from=BUILD_IMAGE /usr/src/app/frontend/node_modules ./node_modules
COPY --from=BUILD_IMAGE /usr/src/app/frontend/next.config.js next.config.js
COPY --from=BUILD_IMAGE /usr/src/app/frontend/.next ./.next
COPY --from=BUILD_IMAGE /usr/src/app/frontend/public ./public

EXPOSE 3000
CMD ["npm", "start"]