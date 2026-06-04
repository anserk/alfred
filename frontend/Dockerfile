FROM node:24-slim


# Install pnpm globally
RUN npm install -g pnpm

WORKDIR /app

# Copy package files
COPY package*.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Expose Vite port
EXPOSE 5173

# Start dev server
CMD ["pnpm", "run", "dev", "--", "--host", "0.0.0.0"]