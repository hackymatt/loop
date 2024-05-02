FROM node:18-alpine as dependencies
WORKDIR /usr/src/app/frontend
COPY package.json package-lock.json ./
RUN yarn install --frozen-lockfile
FROM node:18-alpine as builder
WORKDIR /usr/src/app/frontend
COPY . .
COPY --from=dependencies /usr/src/app/frontend/node_modules ./node_modules
RUN yarn build
FROM node:18-alpine as runner
WORKDIR /usr/src/app/frontend
ENV NODE_ENV production

COPY --from=builder /usr/src/app/frontend/next.config.js ./
COPY --from=builder /usr/src/app/frontend/public ./public
COPY --from=builder /usr/src/app/frontend/.next ./.next
COPY --from=builder /usr/src/app/frontend/node_modules ./node_modules
COPY --from=builder /usr/src/app/frontend/package.json ./package.json
EXPOSE 3000
CMD ["yarn", "start"]