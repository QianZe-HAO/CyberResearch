FROM ghcr.io/astral-sh/uv:alpine
WORKDIR /app

COPY . .

# Install dependencies
RUN uv sync

# Install playwright and dependencies
RUN playwright install-deps
RUN playwright install chromium

# Run the application
CMD ["streamlit", "run", "main.py"]
