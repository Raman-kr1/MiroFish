# MiroFish Project Structure and Overview

MiroFish is a next-generation AI prediction engine powered by multi-agent technology. By extracting seed information from the real world (such as breaking news, policy drafts, or financial signals), it automatically constructs a high-fidelity parallel digital world where thousands of intelligent agents with independent personalities, long-term memory, and behavioral logic freely interact and undergo social evolution. 

It allows users to dynamically inject variables to simulate and deduce future trajectories, effectively acting as a rehearsal laboratory for decision-makers and a creative sandbox for individual users.

## 🏗️ Overall Architecture

The project follows a standard decoupled Client-Server architecture:
- **Frontend** built with Vue 3 and Vite, providing a modern, interactive web interface for building the simulation graph, setting up the environment, running simulations, and generating reports.
- **Backend** built with Python Flask, acting as the core simulation engine. It orchestrates LLMs, Zep Cloud for long-term agent memory, and the OASIS framework for social media interaction simulation.

---

## 💻 Frontend Structure (`/frontend`)

The frontend is a Single Page Application (SPA) built using **Vue.js 3** and **Vite** as the build tool.

### Directory Breakdown (`/frontend/src/`)

- **`api/`**: Contains Javascript files (`index.js`, `graph.js`, `simulation.js`, `report.js`) that encapsulate `axios` API calls to the backend. This modular approach keeps frontend components clean from direct network requests.
- **`assets/`**: Static assets like images, icons, and global CSS files used across the application components.
- **`components/`**: Reusable Vue components that make up the building blocks of the UI.
  - `GraphPanel.vue`: Component for visualizing the GraphRAG entities and relationships.
  - `HistoryDatabase.vue`: Component for viewing historical prediction runs and simulations.
  - `Step1GraphBuild.vue` to `Step5Interaction.vue`: These represent the core 5-step workflow of the application:
    1. **Graph Building**: Extracting seed content.
    2. **Env Setup**: Setting up agent personalities and rules.
    3. **Simulation**: Running the multi-agent parallel simulation.
    4. **Report**: Viewing the generated prediction reports.
    5. **Interaction**: Deep chat interaction with the simulated agents.
- **`views/`**: Higher-level page components (e.g., `Home.vue`, `MainView.vue`, `Process.vue`) that compose multiple smaller components from `components/` and are mapped to routing paths.
- **`router/`**: Defines the application's navigation paths (vue-router) mapping URLs to specific `views/`.
- **`store/`**: Likely contains state management modules (e.g., `pendingUpload.js`) to handle shared states across different components (like user session, current simulation progress, etc.).
- **`App.vue` & `main.js`**: The root component and entry point of the Vue application where plugins (router, store, etc.) are initialized.

---

## ⚙️ Backend Structure (`/backend`)

The backend is a **Python Flask** application designed to handle the heavy lifting of document processing, LLM interactions, graph building, and multi-agent simulation orchestration.

### Key Technologies 
- **Framework**: Flask (handling REST API requests)
- **LLM Integration**: OpenAI SDK compatible interfaces (defaults to Alibaba Qwen via Configuration).
- **Memory Management**: Zep Cloud for agent memory and GraphRAG.
- **Simulation Engine**: CAMEL-AI OASIS framework for agent social interactions.

### Directory Breakdown (`/backend/app/`)

#### 1. `api/` (Controllers / Routes)
Contains the Flask route definitions that expose the backend functionalities to the frontend.
- `graph.py`: Endpoints for uploading seed files, extracting GraphRAG, and building agent memory.
- `simulation.py`: Endpoints related to configuring, starting, and monitoring the multi-agent simulation environment.
- `report.py`: Endpoints for interacting with the ReportAgent and generating the final prediction documents.

#### 2. `models/` (Data Models)
Defines the data structures and business objects used in the application.
- `project.py` & `task.py`: Data classes handling the core abstractions of a simulation "Project" and the underlying queued "Tasks".

#### 3. `services/` (Core Business Logic)
This is the **most critical** part of the backend. It contains the complex logic that drives MiroFish.
- **Data & Graph Processing**:
  - `graph_builder.py`: Logic for parsing seed text and building the initial knowledge graph.
  - `ontology_generator.py`: Generates the ontological structure (schemas/rules) for the specific simulation topic.
  - `zep_entity_reader.py` & `zep_graph_memory_updater.py`: Code responsible for interacting with Zep Cloud to store, retrieve, and update the memory graphs for individual agents and the collective environment.
- **Simulation Management**:
  - `simulation_manager.py` & `simulation_runner.py`: The core engine controllers that spawn, monitor, and run the parallel agent simulations using the OASIS framework.
  - `simulation_ipc.py`: Handles Inter-Process Communication, likely to manage parallel running simulation environments.
  - `simulation_config_generator.py`: Dynamically generates the configuration parameters and constraints for a specific simulation run based on user input.
  - `oasis_profile_generator.py`: Generates the detailed, independent personas and behavioral traits for the thousands of agents in the simulation.
- **Analysis & Reporting**:
  - `report_agent.py`: A specialized agent with tool access designed to analyze the post-simulation environment and synthesize the comprehensive prediction report.
- **Helpers**:
  - `text_processor.py`: Utilities for chunking and analyzing raw text from seed documents.
  - `zep_tools.py`: Helper functions wrapping the Zep API for easier consumption by other services.

#### 4. `utils/` (Shared Utilities)
Contains common helper functions used across the backend.
- `llm_client.py`: A standardized wrapper for making calls to the configured LLM provider (handling retries, API keys, parsing).
- `file_parser.py`: Logic for parsing uploaded seed documents (e.g., extracting text from PDFs via `PyMuPDF`, handling different file encodings via `charset-normalizer`).
- `logger.py`: Standardized logging configuration for debugging and monitoring parallel processes.
- `retry.py`: Decorators or utility functions to handle transient network/API failures.
- `zep_paging.py`: Helper to handle pagination when retrieving large amounts of data from Zep Cloud.

#### Configuration and Scripts
- **`config.py`**: Centralized configuration management, loading variables from the `.env` file (like `LLM_API_KEY`, `ZEP_API_KEY`, ports, and host data) and making them available to the Flask app.
- **`run.py`**: The main entry point script that initializes the Flask application using `app.create_app()` and binds it to the specified host and port.
- **`/backend/scripts/`**: Directory containing standalone Python scripts (like `run_parallel_simulation.py`) that can be executed independently of the Flask server, likely used for testing, cron jobs, or heavy offline processing.
