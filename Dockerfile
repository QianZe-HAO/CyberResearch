FROM ghcr.io/astral-sh/uv:trixie-slim
WORKDIR /app

COPY . .

# Install dependencies
RUN uv sync

# Install playwright and dependencies
RUN playwright install-deps
RUN playwright install chromium

RUN mkdir -p /app/sandbox
# Run the application on port 8501
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "main.py"]
