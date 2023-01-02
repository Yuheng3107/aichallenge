import json
from sgnlp.models.emotion_entailment import train_model
from sgnlp.models.emotion_entailment import evaluate
from sgnlp.models.emotion_entailment.utils import parse_args_and_load_config

cfg = parse_args_and_load_config('C:/Users/ivany/Documents/Programming/Py3.9/config.json')
train_model(cfg)

