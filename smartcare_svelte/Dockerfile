FROM node:20-alpine

WORKDIR /smartcare_svelte

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["node", "build"]