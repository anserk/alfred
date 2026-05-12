FROM node:25-slim


# Install pnpm globally
RUN npm install -g pnpm

WORKDIR /app

# Copy package files
COPY package*.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install

# Copy source code
COPY . .

# Expose Vite port
EXPOSE 5173

# Start dev server
CMD ["pnpm", "run", "dev"]