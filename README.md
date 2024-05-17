# LLM Code Capability Evaluation System

## Introduction

Welcome to the LLM Code Capability Evaluation System! This innovative system is engineered to assess the coding prowess of language model algorithms. Utilizing the power of PySpark, it implements distributed computing to process and analyze extensive datasets with remarkable efficiency.

## Evaluation Process

Our evaluation system encompasses three primary steps to ensure a comprehensive evaluation of each language model's capabilities:

1. **Infer**

<img src="public/imgs/map1.png" align="center" width="800" height="160">

2. **Evaluate**

<img src="public/imgs/map2.png" align="center" width="800" height="210">

3. **Summarize**

<img src="public/imgs/reduce.png" align="center" width="800" height="250">

## Workflow

<img src="public/imgs/flow.png" align="center" width="800" height="400">

## Framework

<img src="public/imgs/framework.png" align="center" width="800" height="400">

## Getting Started

### Prerequisites

- Docker is enough

### Installation

To prepare the environment for code testing, you can either build the Docker image by:

```bash
docker build -t mypytorch .
```

or pull it from Docker Hub using the commands below:

```bash
sudo docker pull michaelyang0050/llm_benchmark
docker tag michaelyang0050/llm_benchmark mypytorch
```

Then you need to create an .env file containning your API keys with the following format:

```
OPENAI_API_KEY= ...
BAIDU_SECRET_KEY= ...
...
```

## Jobs Directory

Within the `jobs` directory, you'll find multiple executable jobs. Each job is tailored to test a different model on a designated dataset, crafted to rigorously assess model performance and precision.

## Running the Tests

Navigate to the `jobs` directory and execute the job file of your choice to run a test. Ensure you have the correct permissions and that the environment variables are properly configured.just run:

```bash
sudo bash run_cluster.sh
```

or if you want to run it locally:

```bash
sudo bash run.sh
```

## Experiments

We test four different LLMs based on our benchmark. And the results are as follows:

<img src="public/imgs/experiments.png" align="center" width="1000" height="200">

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Acknowledgments

- The PySpark community
- Docker Hub
- All the contributors who have played a role in developing this project
