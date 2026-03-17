# Use an official Node runtime as a parent image
FROM node:20-slim AS build

# Set work directory
WORKDIR /app

# Copy package files
COPY frontend-react/package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY frontend-react/ .

# Build the app
RUN npm run build

# Stage 2: Serve with Nginx for production performance
FROM nginx:alpine

# Copy build files from stage 1
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config if needed, or use default
# EXPOSE 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
