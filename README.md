# LLM Code Capability Evaluation System

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)

<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Introduction

Welcome to the LLM Code Capability Evaluation System! This innovative system is engineered to assess the coding prowess of language model algorithms. Utilizing the power of PySpark, it implements distributed computing to process and analyze extensive datasets with remarkable efficiency. This benchmark can help to evaluate LLM's code capability in higher level like CV and NLP tasks. Here is an example case: https://github.com/MichaelYang-lyx/LLM-Code-Benchmark/tree/main/data/AItest/test2.

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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MichaelYang-lyx"><img src="https://avatars.githubusercontent.com/u/111903735?v=4?s=100" width="100px;" alt="Michael"/><br /><sub><b>Michael</b></sub></a><br /><a href="https://github.com/MichaelYang-lyx/LLM-Code-Benchmark/commits?author=MichaelYang-lyx" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ZixinMa27"><img src="https://avatars.githubusercontent.com/u/72734552?v=4?s=100" width="100px;" alt="ZixinMa27"/><br /><sub><b>ZixinMa27</b></sub></a><br /><a href="https://github.com/MichaelYang-lyx/LLM-Code-Benchmark/commits?author=ZixinMa27" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hareisland"><img src="https://avatars.githubusercontent.com/u/146825972?v=4?s=100" width="100px;" alt="Z.Shen"/><br /><sub><b>Z.Shen</b></sub></a><br /><a href="https://github.com/MichaelYang-lyx/LLM-Code-Benchmark/commits?author=hareisland" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JifengCHN"><img src="https://avatars.githubusercontent.com/u/158441842?v=4?s=100" width="100px;" alt="JifengCHN"/><br /><sub><b>JifengCHN</b></sub></a><br /><a href="https://github.com/MichaelYang-lyx/LLM-Code-Benchmark/commits?author=JifengCHN" title="Code">💻</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
