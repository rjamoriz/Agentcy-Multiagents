



![Screenshot](assets/coffee_agntcy.png)

[![Release](https://img.shields.io/github/v/release/agntcy/repo-template?display_name=tag)](CHANGELOG.md)
[![Contributor-Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-fbab2c.svg)](CODE_OF_CONDUCT.md)

## About the Project

**CoffeeAgntcy** is a reference implementation based on a fictitious coffee company to help developers understand how components in the **AGNTCY Internet of Agents** ecosystem can work together. It gives examples of the components of AGNTCY working together as a **Multi-agent System (MAS)**.

## System Architecture

### Lungo Multi-Agent System Overview

```mermaid
graph TB
    subgraph "User Interface"
        UI[React UI<br/>Port 3000]
    end
    
    subgraph "API Layer"
        API[Exchange Server<br/>FastAPI<br/>Port 8000]
    end
    
    subgraph "Agent Layer"
        BRAZIL[Brazil Farm Agent<br/>Port 9999]
        COLOMBIA[Colombia Farm Agent<br/>Port 9998]
        VIETNAM[Vietnam Farm Agent<br/>Port 9997]
        SUPERVISOR[Logistics Supervisor]
        FARM_LOG[Logistics Farm]
        SHIPPER[Shipper Agent]
        ACCOUNTANT[Accountant Agent]
        HELPDESK[Helpdesk Agent]
    end
    
    subgraph "MCP Services"
        WEATHER[Weather MCP<br/>Port 8125]
        PAYMENT[Payment MCP<br/>Port 8081]
    end
    
    subgraph "Transport Layer"
        SLIM[SLIM Transport<br/>Port 46357]
        NATS[NATS Message Broker<br/>Ports 4222-4223]
    end
    
    subgraph "Data & Observability"
        CLICKHOUSE[ClickHouse DB<br/>Ports 8123, 9000]
        OTEL[OpenTelemetry<br/>Ports 4317-4318]
        GRAFANA[Grafana Dashboards<br/>Port 3001]
    end
    
    UI --> API
    API --> SLIM
    
    SLIM <--> BRAZIL
    SLIM <--> COLOMBIA
    SLIM <--> VIETNAM
    SLIM <--> SUPERVISOR
    SLIM <--> FARM_LOG
    SLIM <--> SHIPPER
    SLIM <--> ACCOUNTANT
    SLIM <--> HELPDESK
    
    COLOMBIA --> WEATHER
    ACCOUNTANT --> PAYMENT
    
    BRAZIL --> OTEL
    COLOMBIA --> OTEL
    VIETNAM --> OTEL
    API --> OTEL
    
    OTEL --> CLICKHOUSE
    GRAFANA --> CLICKHOUSE
    
    SUPERVISOR -.-> NATS
    FARM_LOG -.-> NATS
    
    style UI fill:#e1f5ff
    style API fill:#fff4e1
    style BRAZIL fill:#d4edda
    style COLOMBIA fill:#d4edda
    style VIETNAM fill:#d4edda
    style WEATHER fill:#f8d7da
    style PAYMENT fill:#f8d7da
    style SLIM fill:#d1ecf1
    style GRAFANA fill:#e2e3e5
```

### Agent Communication Flow

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant Exchange
    participant SLIM
    participant Brazil
    participant Colombia
    participant Vietnam
    participant Weather MCP

    User->>UI: Request farm inventories
    UI->>Exchange: POST /agent/prompt
    Exchange->>SLIM: Broadcast request
    
    par Parallel Agent Processing
        SLIM->>Brazil: Get inventory
        Brazil-->>SLIM: 450,000 lbs
        
        SLIM->>Colombia: Get inventory
        Colombia->>Weather MCP: Get weather data
        Weather MCP-->>Colombia: Weather forecast
        Colombia-->>SLIM: 6,500 lbs (calculated)
        
        SLIM->>Vietnam: Get inventory
        Vietnam-->>SLIM: 1,800,000 lbs
    end
    
    SLIM-->>Exchange: Aggregated responses
    Exchange-->>UI: Combined inventory
    UI-->>User: Display results
```

### Data Flow Architecture

```mermaid
flowchart LR
    subgraph "Input Sources"
        A[User Prompts]
        B[MCP Servers]
    end
    
    subgraph "Agent Processing"
        C[LangGraph Agents]
        D[LLM Provider<br/>OpenAI/Anthropic/Groq]
    end
    
    subgraph "Communication"
        E[SLIM Transport]
        F[A2A Protocol]
    end
    
    subgraph "Observability"
        G[OpenTelemetry]
        H[ClickHouse]
        I[Grafana]
    end
    
    A --> C
    B --> C
    C <--> D
    C <--> E
    E <--> F
    C --> G
    G --> H
    H --> I
    
    style C fill:#d4edda
    style E fill:#d1ecf1
    style I fill:#e2e3e5
```

### Component Stack

```mermaid
graph TB
    subgraph "Application Layer"
        A1[React Frontend]
        A2[FastAPI Backend]
    end
    
    subgraph "Agent Framework"
        B1[LangGraph]
        B2[LangChain]
        B3[A2A SDK v0.3.0]
    end
    
    subgraph "Transport & Messaging"
        C1[SLIM v0.6.1]
        C2[NATS v2.11.8]
        C3[MCP v1.10.0+]
    end
    
    subgraph "Observability & Data"
        D1[ioa-observe-sdk v1.0.24]
        D2[OpenTelemetry]
        D3[ClickHouse]
        D4[Grafana]
    end
    
    subgraph "Infrastructure"
        E1[Docker Compose]
        E2[Python 3.12]
        E3[Node.js 16+]
        E4[uv Package Manager]
    end
    
    A1 --> B1
    A2 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> C1
    B3 --> C2
    B3 --> C3
    B1 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> D4
    
    E1 -.-> A1
    E1 -.-> A2
    E2 -.-> B1
    E3 -.-> A1
    E4 -.-> B1
    
    style B1 fill:#d4edda
    style C1 fill:#d1ecf1
    style D4 fill:#e2e3e5
```

This reference agentic application demonstrates how to:

- How **SLIM** enables **request-reply** , **unicast (fire & forget)** and **group communication** patterns.
- How tools and transports can be reused across agent implementations (e.g., **SLIM**, **NATS**, **MCP**)
- How protocol-agnostic bridges and clients interconnect modular agents
- How to orchestrate agents using **LangGraph** for structured, stateful workflows with streaming support
- How to write **A2A** client and server agents
- How to integrate data sources (e.g., weather services via **MCP**)
- How to extend or swap agents modularly using AGNTCY tooling
- How to enable observability using **AGNTCY Observe SDK**
- How to enable identity using **AGNTCY Identity Service SDK**

---

### Setups Included

We currently provide two setups you can run to see how components from AGNTCY work together — one simple two-agent use case and the other a more complex MAS:

- **Corto**:  
  A two-agent, ready-to-run setup that highlights core agent interactions using agent-to-agent (A2A) messaging via configurable transports(default: AGNTCY's SLIM). Agents are orchestrated within a LangGraph. It also shows how to enable observability using Observe SDK.

  👉 [View the Corto README](coffeeAGNTCY/coffee_agents/corto)

- **Lungo**:  
  A more advanced setup that will evolve over time as we mature components. There are two setups: 1) pub/sub A2A over NATS as default transport along with streaming support, and 2) group communication over SLIM as default along with streaming support. Agents are structured as directed LangGraphs with A2A communication using configurable transports. It includes an MCP weather-aware farm that fetches live data, observability via the Observe SDK, identity, and a group communication pattern with specialized agents (farms, shipper, accountant) that collaborate to fulfill coffee orders.

  👉 [View the Lungo README](coffeeAGNTCY/coffee_agents/lungo)

---

### Built With

- [AGNTCY App SDK](https://github.com/agntcy/app-sdk) = v0.4.1
- [SLIM](https://github.com/agntcy/slim) = v0.6.1
- [NATS](https://github.com/nats-io/nats-server) = v2.11.8
- [A2A](https://github.com/a2aproject/a2a-python) = v0.3.0
- [MCP](https://github.com/modelcontextprotocol/python-sdk) >= v1.10.0
- [LangGraph](https://github.com/langchain-ai/langgraph) >= v0.4.1
- [Observe SDK](https://github.com/agntcy/observe) = 1.0.24
- [AGNTCY Identity Service SDK](https://github.com/agntcy/identity-service) = 0.0.6

---

## Contributing

This is a developer-facing reference repo. If you're building agentic systems—or interested in shaping the future of distributed agents—we'd love your feedback, contributions, or collaboration. Contributions are what make the open-source community such an amazing place to learn, inspire, and create. For detailed contributing guidelines, please see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

Distributed under the Apache-2.0 License. See [LICENSE](LICENSE) for more information.

## Acknowledgements

- The [AGNTCY](https://github.com/agntcy) project.
