# 🤖 Data Analyst 1

This is a **Data Analyst Agent** built with LangChain, designed to clean, transform, and enrich tabular data. The agent uses a suite of specialized tools to perform operations on pandas DataFrames based on natural language commands.

---

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Set up the Python environment:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    For development, use `requirements-dev.txt`:
    ```bash
    pip install -r requirements-dev.txt
    ```
    For production, use `requirements.txt`.

4.  **Configure Environment Variables:**
    Copy the `env.example` file to `.env` in the project root and fill in your configuration details.

    **env.example:**
    ```ini
    # Required environment variables for the application

    # LLM Configuration
    MODEL_NAME=gpt-3.5-turbo  # or any other supported model
    LLM_API_KEY=your_openai_api_key_here  # Required if using OpenAI models

    # Logging Configuration
    LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

    # Application Settings
    MAX_ITERATIONS=10  # Maximum iterations for the agent to run
    ```
    Ensure you replace placeholder values like `your_openai_api_key_here` with your actual credentials.

---

## 📂 Dataset

The test_agent.py is currently using the **Student Stress Monitoring Datasets** as an example, you can change it to use any other dataset.

1.  **Download the dataset:**
    Download the dataset from Kaggle: [https://www.kaggle.com/datasets/mdsultanulislamovi/student-stress-monitoring-datasets](https://www.kaggle.com/datasets/mdsultanulislamovi/student-stress-monitoring-datasets)

2.  **Place the files:**
    Create a `data` directory in the project root and place the downloaded CSV files inside it. The file structure should look like this:
    ```
    .
    ├── data/
    │   └── Student Stress Monitoring Datasets/
    │       ├── Stress_Dataset.csv
    │       └── StressLevelDataset.csv
    ├── app/
    │   └── ...
    ├── requirements-dev.txt
    ├── requirements.txt
    ├── env.example
    └── ...
    ```

---

## 🚀 Usage

The agent can be run using the provided test script.

1.  **Execute the script:**
    ```bash
    python test_agent.py
    ```

2.  **Interact with the agent:**
    You can now enter your data manipulation commands at the prompt. The agent will respond by executing the appropriate tools.

    **Example Interaction:**
    ```
    User: I have provided the two datasets, one primary and one mapping, can you analyse and tell me how many students are aged below 19
    > Entering new AgentExecutor chain...
    // Agent plans and executes tool calls to inspect the data and find the answer
    ...
    > Finished chain.
    Agent Final Answer: Based on the analysis of the 'Stress_Dataset.csv', there are XX students aged below 19.
    ```