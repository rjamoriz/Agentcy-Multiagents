# Lungo Multi-Agent Coffee System - Setup Guide

This guide will help you set up and run the Lungo multi-agent coffee system on a new machine.

## Prerequisites

- **Docker Desktop** (with sufficient resources: 4GB+ RAM, 20GB+ disk space)
- **Python 3.12** (not 3.13!)
- **uv** (Python package manager)
- **Node.js 16.14.0+**
- **Git**

## Quick Setup Steps

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd coffeeAgntcy/coffeeAGNTCY/coffee_agents/lungo
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

**Required changes in `.env`:**
- Set `OPENAI_API_KEY` to your actual OpenAI API key
- Or configure another LLM provider (Anthropic, Azure, Groq)
- Verify `TRANSPORT_SERVER_ENDPOINT=http://slim-lungo:46357`
- Verify `IDENTITY_AUTH_ENABLED=false`

### 3. Start Docker Services

```bash
# Make sure Docker Desktop is running
# Start all 20 services
docker compose up -d
```

Wait about 60 seconds for all services to initialize.

### 4. Verify System is Running

```bash
# Check all containers are running
docker compose ps

# Test Brazil farm
curl -X POST http://127.0.0.1:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the Brazil farm inventory?"}'
```

You should see a response like:
```json
{"response":"The current inventory from the Brazil farm is 450,000 pounds."}
```

## System Architecture

The system consists of **20 Docker containers**:

### Infrastructure Services
- **slim-lungo**: Agent-to-agent transport (port 46357)
- **nats**: Message broker (ports 4222-4223)
- **clickhouse**: Database (ports 8123, 9000)
- **otel-collector**: Observability (ports 4317-4318)
- **grafana**: Dashboards (port 3001)

### Farm Agents
- **brazil-farm-server**: Port 9999
- **colombia-farm-server**: Port 9998 (uses Weather MCP)
- **vietnam-farm-server**: Port 9997

### Exchange & Logistics
- **exchange-server-lungo**: FastAPI on port 8000
- **logistic-supervisor**
- **logistic-farm-server**
- **logistic-shipper-server**
- **logistic-accountant-server**
- **logistic-helpdesk-server**

### MCP Servers
- **weather-mcp-server**: Port 8125 (provides weather data)
- **payment-mcp-server**: Port 8081

### UI
- **ui-lungo**: React/Vite on port 3000

## Access Points

- **UI**: http://localhost:3000
- **API**: http://localhost:8000/agent/prompt
- **Grafana**: http://localhost:3001

## Testing the System

### Test Individual Farms

```bash
# Brazil farm
curl -X POST http://127.0.0.1:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the Brazil farm inventory?"}'

# Colombia farm (with Weather MCP)
curl -X POST http://127.0.0.1:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the yield estimate for Colombia farm?"}'

# Vietnam farm
curl -X POST http://127.0.0.1:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the inventory for Vietnam farm?"}'
```

### Test All Farms Together

```bash
curl -X POST http://127.0.0.1:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the total inventory from all three coffee farms?"}'
```

## Important Configuration Notes

### Python Version
⚠️ **Must use Python 3.12**, not 3.13!
- The `ioa_observe` SDK has compatibility issues with Python 3.13
- All Dockerfiles are configured for Python 3.12-slim
- `pyproject.toml` requires Python >=3.12,<4.0

### Docker Configuration
- All farm servers use `TRANSPORT_SERVER_ENDPOINT=http://slim-lungo:46357`
- All farm servers have `IDENTITY_AUTH_ENABLED=false` for local development
- Weather MCP provides real-time weather data to Colombia farm

### Key Files Modified from Original
- `lungo/pyproject.toml`: Python 3.12 requirement, updated dependencies
- `lungo/common/llm.py`: Direct LLM provider implementation
- `lungo/docker-compose.yaml`: Environment variables for all services
- `lungo/docker/Dockerfile.*`: Python 3.12-slim, build-essential, UV_PYTHON
- `lungo/agents/farms/*/card.py`: Agent IDs use underscores
- `lungo/agents/*/agent_executor.py`: Added session_start() tracing

## Troubleshooting

### Disk Space Issues
```bash
# Clean up Docker resources
docker system prune -a -f --volumes
```

### Port Conflicts
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process if needed
kill -9 <PID>
```

### Services Not Starting
```bash
# Check logs for specific service
docker logs --tail=50 brazil-farm-server
docker logs --tail=50 exchange-server-lungo
docker logs --tail=50 weather-mcp-server
```

### Python Version Issues
```bash
# Verify Python version in containers
docker logs --tail=15 brazil-farm-server | grep -E "python3\.|CPython"
# Should show: "Using CPython 3.12.12 interpreter"
```

## Rebuilding Services

If you need to rebuild after code changes:

```bash
# Stop services
docker compose stop brazil-farm-server colombia-farm-server vietnam-farm-server exchange-server weather-mcp-server payment-mcp-server

# Rebuild
docker compose build brazil-farm-server colombia-farm-server vietnam-farm-server exchange-server weather-mcp-server payment-mcp-server

# Start again
docker compose up -d brazil-farm-server colombia-farm-server vietnam-farm-server exchange-server weather-mcp-server payment-mcp-server
```

## Stopping the System

```bash
# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
```

## Development Notes

- SLIM broadcast timeout: 60 seconds
- Agent card IDs must match @agent decorator names (use underscores)
- Identity authentication disabled for local development
- Weather MCP integration operational for Colombia farm
- All services use OpenTelemetry for observability

## Success Criteria

✅ All 20 Docker containers running
✅ Brazil farm responds with inventory
✅ Colombia farm responds with yield (using Weather MCP)
✅ Vietnam farm responds with inventory
✅ All farms respond to broadcast queries
✅ UI accessible on port 3000
✅ Python 3.12.12 in all agent containers

## Support

For issues, check:
1. Docker Desktop has sufficient resources
2. `.env` file configured correctly
3. All containers running: `docker compose ps`
4. Container logs: `docker logs <container-name>`
5. Python version in containers: `docker logs <container> | grep CPython`
