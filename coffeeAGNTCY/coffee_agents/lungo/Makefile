# Makefile for running logistic and farm services with uv
# Each target sets PYTHONPATH to project root before invoking uv

# Variables
PYTHONPATH := $(CURDIR)
UV = PYTHONPATH=$(PYTHONPATH) uv run

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  logistic-supervisor - Run logistic supervisor"
	@echo "  auction-supervisor  - Run auction supervisor"
	@echo "  shipper             - Run logistic shipper"
	@echo "  accountant          - Run logistic accountant"
	@echo "  logistic-farm       - Run logistic farm service"
	@echo "  brazil-farm         - Run Brazil farm server"
	@echo "  colombia-farm       - Run Colombia farm server"
	@echo "  vietnam-farm        - Run Vietnam farm server"
	@echo "  weather-mcp         - Run weather MCP server"
	@echo "  payment-mcp         - Run payment MCP server"
	@echo "  helpdesk            - Run logistic helpdesk"

.PHONY: logistic-supervisor
logistic-supervisor:
	$(UV) agents/supervisors/logistic/main.py

.PHONY: auction-supervisor
auction-supervisor:
	PYTHONPATH="/Users/Ruben_MACPRO/Desktop/IA DevOps/AGENTCY Sandbox/coffeeAgntcy/coffeeAGNTCY/coffee_agents/lungo" uv run agents/supervisors/auction/main.py
	
	# Ensure PYTHONPATH is quoted to handle spaces

.PHONY: shipper
shipper:
	$(UV) agents/logistics/shipper/server.py

.PHONY: accountant
accountant:
	$(UV) agents/logistics/accountant/server.py

.PHONY: logistic-farm
logistic-farm:
	$(UV) agents/logistics/farm/server.py

.PHONY: brazil-farm
brazil-farm:
	PYTHONPATH="/Users/Ruben_MACPRO/Desktop/IA DevOps/AGENTCY Sandbox/coffeeAgntcy/coffeeAGNTCY/coffee_agents/lungo" uv run agents/farms/brazil/farm_server.py

.PHONY: colombia-farm
colombia-farm:
	PYTHONPATH="/Users/Ruben_MACPRO/Desktop/IA DevOps/AGENTCY Sandbox/coffeeAgntcy/coffeeAGNTCY/coffee_agents/lungo" uv run agents/farms/colombia/farm_server.py

.PHONY: vietnam-farm
vietnam-farm:
	PYTHONPATH="/Users/Ruben_MACPRO/Desktop/IA DevOps/AGENTCY Sandbox/coffeeAgntcy/coffeeAGNTCY/coffee_agents/lungo" uv run agents/farms/vietnam/farm_server.py

.PHONY: weather-mcp
weather-mcp:
	PYTHONPATH="/Users/Ruben_MACPRO/Desktop/IA DevOps/AGENTCY Sandbox/coffeeAgntcy/coffeeAGNTCY/coffee_agents/lungo" uv run agents/mcp_servers/weather_service.py

.PHONY: payment-mcp
payment-mcp:
	$(UV) agents/mcp_servers/payment_service.py

.PHONY: helpdesk
helpdesk:
	$(UV) agents/logistics/helpdesk/server.py
