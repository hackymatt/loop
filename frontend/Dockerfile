FROM node:18-alpine as BUILD_IMAGE

WORKDIR /usr/src/app/frontend

COPY package.json package-lock.json ./

# install dependencies
RUN npm install

COPY . .

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