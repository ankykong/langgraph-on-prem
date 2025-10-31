# Fin-Chat example (LangGraph)

## Installation

```bash
poetry install
```

Copy `.env.example` file into a file `.env`. It should look like this:

```bash
# OpenAI
OPENAI_API_KEY="..."

# Arize
ARIZE_SPACE_ID="..."
ARIZE_API_KEY="..."
ARIZE_PROJECT_NAME="..."
# Optional
# ARIZE_ENDPOINT="..."
# ARIZE_TRANSPORT="..."

# FMP
FMP_API_KEY="...."
```

Where FMP_API_KEY is the API obtained from [FMP API](https://site.financialmodelingprep.com/developer/docs).

## Quickstart

The finchat has one mode `interactive`

### Interactive

In interactive mode you can ask your questions in a chat-like fashion.

```bash
poetry run finchat --interactive
```

Each question will create a new trace with the same session-id.

## Arize Tracing

This project uses [Arize AI](https://arize.com/) for tracing and observability of LangGraph agent runs. Arize captures detailed traces of your agent's execution, including:

- LLM calls and responses
- Tool invocations
- Agent decision-making steps
- Timing and performance metrics
- Input/output data at each step

### Default Configuration (Arize Cloud)

By default, traces are sent to Arize's cloud platform. Simply configure these environment variables in your `.env` file:

```bash
ARIZE_SPACE_ID="your-space-id"
ARIZE_API_KEY="your-api-key"
ARIZE_PROJECT_NAME="your-project-name"
```

### Custom Endpoint Configuration (Self-Hosted/On-Premise)

If you're using a self-hosted or on-premise Arize deployment, you can configure custom endpoints using the optional environment variables:

```bash
ARIZE_ENDPOINT="https://arize-app.<your-domain>/v1"
ARIZE_TRANSPORT="grpc"  # or "http"
```

#### gRPC Transport (Default)

gRPC is the default transport protocol and is recommended for better performance:

```python
from arize.otel import register, Transport

tracer_provider = register(
    space_id=SPACE_ID,
    api_key=API_KEY,
    endpoint="https://arize-app.<domain>/v1",
    # transport=Transport.GRPC,  # default
)
```

Configuration in `.env`:
```bash
ARIZE_ENDPOINT="https://arize-app.<your-domain>/v1"
# ARIZE_TRANSPORT defaults to gRPC if not specified
```

#### HTTP Transport

For environments where gRPC is not available or preferred, use HTTP transport:

```python
from arize.otel import register, Transport

tracer_provider = register(
    space_id=SPACE_ID,
    api_key=API_KEY,
    endpoint="https://arize-app.<domain>/v1/traces",
    transport=Transport.HTTP,
)
```

Configuration in `.env`:
```bash
ARIZE_ENDPOINT="https://arize-app.<your-domain>/v1/traces"
ARIZE_TRANSPORT="http"
```

**Note:** When using HTTP transport, the endpoint should include `/traces` at the end.

### Viewing Traces

After running your agent, visit your Arize dashboard to:
- View detailed execution traces
- Analyze performance bottlenecks
- Debug agent behavior
- Monitor token usage and costs

For more information on self-hosted deployments, see the [Arize On-Premise SDK Usage documentation](https://arize.com/docs/ax/selfhosting/on-premise-sdk-usage).