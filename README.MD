# RASA chatbot

## Set up

### Create and activate virtual environment

``` shell
python3 -m venv .venv

source .venv/bin/activate
```

### Install Rasa

``` shell
pip install rasa
```

## Run

Run this to train new data

``` shell
rasa train
```

Run this to activate interactive chat

``` shell
rasa shell 
```

# LLM vs LLM

View .LLMvsLLM/LLMvsLLM.ipynb

## To chat with LLM as sale person

```shell
chainlit run sale_bot.py 
```
