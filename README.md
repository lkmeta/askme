<div align="center">

<p align="center"> <img src="https://github.com/lkmeta/askme/blob/main/app/static/askme.png" width="300px"></p>

<hr class="custom-line">

</div>

<div align="center">
  <p>
    <img src="https://img.shields.io/badge/FastAPI-1f425f.svg" alt="FastAPI">
    <img src="https://img.shields.io/badge/LangChain-1f425f.svg" alt="LangChain">
    <img src="https://img.shields.io/badge/OpenAI-1f425f.svg" alt="OpenAI">
    <img src="https://img.shields.io/badge/PostgreSQL-1f425f.svg" alt="PostgreSQL">
    <img src="https://img.shields.io/badge/Python_3.10-1f425f.svg" alt="Python">
    <img src="https://img.shields.io/badge/Docker-1f425f.svg" alt="Docker">
  </p>
</div>

# AskMe
An intelligent FAQ assistant that accurately answers user queries by matching them with semantically similar questions from a predefined [FAQ database](https://github.com/lkmeta/askme/blob/main/data/faq_data.json). When a close enough match isn't found, the system seamlessly interacts with the OpenAI API to generate the most relevant response.


## Table of Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Monitoring](#monitoring)
- [Testing](#testing)
- [FAQ Database](#faq-database)
- [License](#license)

## About

AskMe is a web-based FAQ assistant powered by NLP models and PostgreSQL's `pgvector` for embedding similarity search. It provides users with precise answers by querying preloaded FAQs stored in a PostgreSQL database and can be extended using OpenAI's GPT models for more complex queries.

## Features

- **FAQ Querying**: Get precise answers to commonly asked questions.
- **Embedding Computing**: Compute embeddings from the provided FAQ data for later similarity searches.
- **LangChain**: Utilize LangChain for NLP tasks outside of OpenAI interactions.
- **OpenAI Integration**: For queries that don't match any existing FAQ, the system can generate responses using OpenAI via LangChain.
- **FastAPI Endpoint**: Provide an API for users to submit questions and receive answers.
- **Authentication**: Added to endpoints using FastAPI’s dependency mechanism.
- **PostgreSQL for FAQ and Embeddings**: Integrated pgVector to store and query vector embeddings.
- **Containerized Deployment**: Full Docker support for easy deployment.

## Project Structure

```bash
.
├── app
│   ├── scripts
│   │   ├── initialize_embeddings.py
│   │   └── load_faq_data.py
│   ├── services
│   │   ├── config.py
│   │   ├── embeddings.py
│   │   ├── openai_client.py
│   │   └── similarity.py
│   ├── static
│   │   ├── favicon.ico
│   │   ├── main.js
│   │   └── styles.css
│   ├── templates
│   │   ├── error.html
│   │   └── index.html
│   ├── utils
│   │   └── logger.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   └── init.sql
├── data
│   └── faq_data.json
├── tests
├── .env_example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.10+**
- **Docker** 

>  <sub>**Note:** You will also need an OpenAI API key to interact with OpenAI.</sub>

## Installation

To install and run AskMe app using Docker, follow these steps:

1. Clone the repository:
```sh
git clone https://github.com/lkmeta/askme.git
cd askme
```

2. Set Up Environment Variables

  ```sh
  cp .env_example .env
  ```
> <sub>Edit the .env file and add your API keys for OpenAI API, Authentication, and PostgreSQL necessary environment variables.    
Additionally, you can configure the following parameters:</sub>  
> <sub>EMBEDDINGS_MODEL: Define the model for embeddings (e.g., text-embedding-3-small).</sub>  
> <sub>SIMILARITY_THRESHOLD: Set the similarity threshold for searching (default: 0.7).</sub>  


3. Build the Docker Image  

  ```sh
 docker-compose build
  ```

4. Run the app

```sh
docker-compose up
```

>  <sub>**Note:** Upon the first run, init.sql is automatically executed, initializing the database with the required schema. The `load_faq_data.py` and `initialize_embeddings.py` scripts will load the FAQs and embeddings.</sub>  

## Usage

### Access the Application
Open your web browser and navigate to ```http://localhost:8000``` to access AskMe.

## API Documentation
FastAPI automatically generates interactive API documentation. Once the application is running, access the documentation at:
```bash
http://localhost:8000/docs
```

## Monitoring

To monitor the application and the services:

1. Ensure you have completed the installation steps above.

2. You can view the logs of the running Docker container to monitor the application output.
  ```sh
  docker-compose logs -f
  ```
>  <sub>**Note:** The -f option follows the log output in real-time.</sub>

## Testing

To benchmark the performance of the AskMe application, you can use [Locust](https://locust.io/), a load-testing tool that helps simulate concurrent users sending requests to your API.

The `locustfile.py` is located inside the `test` directory.

### Steps to Run Locust Test

1. **Install Locust**: If you don't have Locust installed, you can install it using pip (preferably within a virtual environment such as [python env](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)):
    ```bash
    pip install locust
    ```

2. **Navigate to the Test Directory**: 
    ```bash
    cd test
    ```

3. **Run Locust**: Start Locust by running:
    ```bash
    locust -f locustfile.py
    ```

4. **Open Locust Web Interface**: Open your web browser and go to `http://localhost:8089`.

5. **Start the Test**: Fill in the required fields (like the number of users) and set the Host to `http://localhost:8000` to begin testing the AskMe application.

## FAQ Database  
The predefined set of FAQ questions and answers used to compute the embeddings is located in the file [`data/faq_data.json`](https://github.com/lkmeta/askme/blob/main/data/faq_data.json). You can update this file with additional FAQs to improve the system’s accuracy.

## License
This project is licensed under the Apache-2.0 License.
