FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (including dev dependencies for development)
RUN npm install

# Copy application code
COPY . .

EXPOSE 3000

# Run in development mode
CMD ["npm", "run", "dev"]
