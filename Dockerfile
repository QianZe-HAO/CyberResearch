FROM ghcr.io/astral-sh/uv:trixie-slim
WORKDIR /app

COPY . .

# Install dependencies
RUN uv sync

# Install playwright and dependencies
# RUN uv run playwright install-deps
# RUN uv run playwright install chromium
# Conditionally install Playwright only if USE_CRAWL4AI is True
RUN if [ "$USE_CRAWL4AI" = "True" ] || [ "$USE_CRAWL4AI" = "true" ]; then \
  echo "Installing Playwright for Crawl4AI..."; \
  uv run playwright install-deps; \
  uv run playwright install chromium; \
  else \
  echo "Skipping Playwright installation (USE_CRAWL4AI=$USE_CRAWL4AI)"; \
  uv remove crawl4ai; \
  fi


RUN mkdir -p /app/sandbox
# Run the application on port 8501
EXPOSE 8501

# Run the application
CMD ["uv", "run", "streamlit", "run", "main.py"]
