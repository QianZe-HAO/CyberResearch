FROM ghcr.io/astral-sh/uv:alpine
WORKDIR /app

COPY . .

# Install dependencies
RUN uv sync

# Run the application
CMD ["uv", "run", "main.py"]