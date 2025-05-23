FROM ubuntu:22.04 as build

# Set non-interactive installation and timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install necessary dependencies for Tauri
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    libssl-dev \
    libgtk-3-dev \
    libwebkit2gtk-4.0-dev \
    libappindicator3-dev \
    librsvg2-dev \
    patchelf \
    # X11 libraries for GUI apps
    libx11-dev \
    libxext-dev \
    libxcb1-dev \
    libxcb-render0-dev \
    libxcb-shape0-dev \
    libxcb-xfixes0-dev \
    # Additional dependencies
    pkg-config \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js v20.x (LTS)
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Tauri CLI
RUN npm install -g @tauri-apps/cli

WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json* ./

# Install npm dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the Tauri application
RUN npm run tauri:build

# Start a new stage for the runtime
FROM ubuntu:22.04 as runtime

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libwebkit2gtk-4.0-37 \
    libappindicator3-1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the built Tauri application from the build stage
COPY --from=build /app/src-tauri/target/release/bundle/deb /app/bundle

# Expose any required ports
EXPOSE 8000

# Set entry point to the Tauri application
CMD ["./bundle/poly-micro-tauri"]
