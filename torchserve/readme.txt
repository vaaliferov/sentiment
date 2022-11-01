https://github.com/pytorch/serve/blob/master/README.md
https://github.com/pytorch/serve/blob/master/docker/README.md
https://github.com/pytorch/serve/tree/master/examples/Huggingface_Transformers

git clone https://github.com/pytorch/serve.git
cd serve/examples/Huggingface_Transformers
vim setup_config.json
"model_name":"Tatyana/rubert-base-cased-sentiment-new","num_labels":"3",
vim Seq_classification_artifacts/index_to_name.json
{"0":"NEUTRAL","1":"POSITIVE","2":"NEGATIVE"}
python3 Download_Transformer_models.py

cd ../../../ && mkdir model-store
docker run --rm -it -p 8080:8080 -p 8081:8081 --name mar -v $(pwd)/model-store:/home/model-server/model-store -v $(pwd)/serve/examples:/home/model-server/examples pytorch/torchserve:latest

docker ps -a
docker exec -it 019da035a1ba /bin/bash
cd examples/Huggingface_Transformers
torch-model-archiver --model-name my_bert --version 1.0 --serialized-file Transformer_model/pytorch_model.bin --handler ./Transformer_handler_generalized.py --extra-files "Transformer_model/config.json,./setup_config.json,./Seq_classification_artifacts/index_to_name.json"
mv my_bert.mar ~/model-store
exit

docker build -t my_bert .
docker run --rm -p 8080:8080 -p 8081:8081 --name my_bert my_bert

curl http://127.0.0.1:8081/models
curl http://127.0.0.1:8081/models/my_model

curl -X POST http://127.0.0.1:8080/predictions/my_bert -T ./serve/examples/Huggingface_Transformers/Seq_classification_artifacts/sample_text_captum_input.txt

curl -X POST http://127.0.0.1:8080/explanations/my_bert -T ./serve/examples/Huggingface_Transformers/Seq_classification_artifacts/sample_text_captum_input.txt

import json, requests
url = 'http://127.0.0.1:8080/predictions/my_bert'
requests.post(url, data=json.dumps({'text':'test'})).text
