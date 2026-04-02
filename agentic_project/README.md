# ECommerce Support Agent

This project implements an ECommerce Support Agent that can assist users with order tracking, product information, and other common customer support tasks.

## Project Structure

agentic_project/
├── config/
│   └── config.yaml              # Agent configuration (LLM settings, security, error handling)
├── data/
│   ├── datasets/                # Data sources
│   ├── memory/
│   │   ├── long_term/             # Persistent memory storage
│   │   └── short_term/            # Session memory
│   └── tools/                   # Tool-specific data
├── agents/
│   └── main_agent.py            # Main Agent class
├── tools/
│   └── tool_manager.py          # Tool implementations (currently empty, logic in main_agent.py)
├── workflows/
│   └── default_workflow.py      # Agent workflow definitions (currently empty, logic in main_agent.py)
├── observability/
│   └── monitoring.py            # Logging, metrics, tracing
├── guardrails/
│   └── safety.py                # Input/output validation, content filtering
├── error_handling/
│   └── handler.py               # Retry logic, circuit breaker, fallback
├── gcp/
│   └── deploy.py                # GCP deployment utilities (currently empty)
├── tests/
│   └── test_agent.py            # Unit tests
├── Dockerfile                 # Container definition
├── requirements.txt           # Python dependencies
├── main.py                    # Entry point
└── README.md                  # Project documentation

## Configuration

The agent's behavior is configured in `config/config.yaml`. This file includes settings for:

-   **LLM:** Model name, temperature, max tokens, and API key.
-   **Security:** Authentication type (API\_KEY, NONE, OAUTH), API key, and allowed origins.
-   **Error Handling:** Retry attempts, retry delay, circuit breaker threshold, and circuit breaker timeout.
-   **Data Sources:** Configuration for connecting to order databases, product catalogs, and shipping APIs.
-   **Agent Behavior:** Greeting, farewell, and forbidden topics.
-   **Observability:** Logging level, metrics, and tracing.

## Data Sources

The agent can access data from various sources, including:

-   **Order Database:** A PostgreSQL database containing order information.
-   **Product Catalog:** A CSV file containing product details.
-   **Shipping API:** An API for retrieving shipping updates.

## Error Handling

The agent implements robust error handling using:

-   **Retry Logic:** Automatically retries failed requests.
-   **Circuit Breaker:** Prevents the agent from making requests to a failing service.
-   **Fallback Mechanisms:** Provides informative error messages to the user.

## Security

The agent supports different authentication methods, including API key authentication.  Input validation is performed to prevent the agent from handling forbidden topics.

## Observability

The agent provides detailed logging and monitoring capabilities, including:

-   **Request Logging:** Logs all user requests.
-   **Response Logging:** Logs all agent responses.
-   **Error Logging:** Logs any errors that occur.
-   **Performance Monitoring:** Tracks the time it takes to process requests.

## Usage

1.  **Install Dependencies:**

    pip install -r requirements.txt

2.  **Configure the Agent:**

    -   Update `config/config.yaml` with your desired settings, including your LLM API key and data source connections.
    -   Replace placeholder values in `agents/main_agent.py` with your actual GCP project ID, location, and service account path.

3.  **Run the Agent:**

    python main.py

## Testing

Run the unit tests to verify the agent's functionality:

python -m unittest discover -s tests

## Deployment

The project includes a `Dockerfile` for containerized deployment. You can build and run the Docker image using:

docker build -t ecommerce-support-agent .
docker run -p 8000:8000 ecommerce-support-agent

The `gcp/deploy.py` file (currently empty) would contain the necessary code to deploy the agent to Google Cloud Platform using services like Vertex AI.

## Contributing

Contributions are welcome! Please submit a pull request with your changes.