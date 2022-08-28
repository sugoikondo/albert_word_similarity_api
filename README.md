# albert_word_similarity_api
API that calculates and returns the similarity between words.
Currently only Japanese is supported.

## Getting Started
### Docker (Docker Compose)

```bash
docker-compose up -d
```

### On local environment
#### Prerequisites
- Python 3.10.6
- [poetry](https://cocoatomo.github.io/poetry-ja/#_3) 1.1.6 or higher


#### Project set up
First, you need to install dependencies.

```bash
poetry install
```

Next, start and enter the virtual environment.
```bash
poetry shell
```

Then you can run application server.
```bash
uvicorn main:app --reload
```

## Usage
When you send requests to `POST /word_similarity`, with body like this:

```json
{
  "target_words": ["銀行"],
  "candidates": ["現金", "リース資産", "貸倒引当金", "当座預金"],
  "top_n": 3
}
```

Then you can obtain below result

```json
{
    "results": [
        {
            "word": "銀行",
            "similar_words": [
                {
                    "word": "現金",
                    "similarity": 0.8859629034996033
                },
                {
                    "word": "リース資産",
                    "similarity": 0.8650936484336853
                },
                {
                    "word": "当座預金",
                    "similarity": 0.7373276352882385
                }
            ]
        }
    ]
}
```
