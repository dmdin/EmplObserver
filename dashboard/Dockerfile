FROM node:18-alpine3.18 AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app
COPY . .


FROM base as prod-deps
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile


FROM base AS build
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build


FROM base

RUN apk add graphicsmagick
RUN apk add --no-cache sed
RUN sed -i 's/node:x:1000:1000/node:x:1001:1001/g' /etc/passwd && \
    sed -i 's/node:x:1000:node/node:x:1001:node/g' /etc/group && \
    chown -R node:node /home/node

COPY --from=prod-deps /app/node_modules /app/node_modules
COPY --from=build /app/build /app

RUN npx prisma generate
EXPOSE 3000
CMD ["node", "./index.js"]