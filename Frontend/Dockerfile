FROM node:18-alpine

WORKDIR /app

# Install dependencies (use npm ci when package-lock present)
COPY package.json package-lock.json* ./
RUN if [ -f package-lock.json ]; then npm ci --silent --no-audit --prefer-offline || npm install --silent; else npm install --silent; fi

# Copy source
COPY . .

EXPOSE 5173

ENV HOST 0.0.0.0

CMD ["npm", "run", "dev"]
