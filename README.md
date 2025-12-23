# Cyber Researcher

A conversational AI research assistant powered by LangChain and DeepAgents, designed to perform detailed, structured research on any given topic using internet search and computational tools.

## Features

- **Smart Query Analysis**: Breaks down complex research questions into actionable components.
- **Real-time Web Search**: Uses the `internet_search` tool to fetch up-to-date, accurate information.
- **Mathematical Computation**: Supports symbolic math operations including differentiation, integration, equation solving, and matrix calculations.
- **Time Utilities**: Access to current datetime, timestamp conversion, and formatting.
- **Structured Output**: Generates well-organized reports with sections like Overview, Key Features, Use Cases, and Recent Developments.

## Currently Supported Tools

### Web & Data
- `internet_search(query: str)` – Performs a real-time web search using precise queries.
- `crawl_url(url: str)` – Crawls a URL and extracts text content based on a URL.

### Date & Time
- `get_current_datetime()` – Returns the current date and time.
- `get_current_timestamp()` – Returns the current Unix timestamp.
- `convert_timestamp_to_datetime(timestamp: int)` – Converts Unix timestamp to readable datetime.

### Symbolic Mathematics
- `differentiate(expression, variable)` – Differentiates a mathematical expression.
- `integrate_expression(expression, variable)` – Computes indefinite or definite integrals.
- `solve_equation(equation, variable)` – Solves algebraic equations symbolically.
- `matrix_operation(matrix_a, matrix_b, operation)` – Performs matrix addition, multiplication, inversion, etc.
- `preprocess_math(input_str)` – Cleans and parses math expressions from natural language.
- `calculate(expression)` – Evaluates basic arithmetic or symbolic expressions.

## Usage

Run the agent and ask research-oriented questions:

```bash
docker build -t cyber-researcher .
```

```bash
docker run -it cyber-researcher
```

Example prompts:
> "Compare React and Svelte for modern web development"  
> "What are the recent advancements in quantum computing?"  
> "Solve the differential equation dy/dx = x^2 + y"

The agent will use available tools to gather and synthesize accurate, cited insights.

---

Built with `langgraph`, `langchain`, and extensible tooling for deep, reliable research workflows.