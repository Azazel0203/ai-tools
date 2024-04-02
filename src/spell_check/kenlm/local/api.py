from model import Model
from request import ModelRequest, ModelUpdateRequest
from quart import Quart, request
import aiohttp

app = Quart(__name__)

model = None

model_paths = {
    'ory': '5gram_model.bin',
    'eng': '5gram_model_eng.bin'
}

vocab_paths = {
    'ory': 'lexicon.txt',
    'eng': 'lexicon_eng.txt'
}

freq_dict_paths = {
    'ory': 'freq_dict.txt',
    'eng': 'freq_dict_eng.txt'
}


@app.before_serving
async def startup():
    app.client = aiohttp.ClientSession()
    global model
    model = Model(app, model_paths, vocab_paths, freq_dict_paths)

@app.route('/', methods=['POST'])
async def embed():
    global model
    data = await request.get_json()
    req = ModelRequest(**data)
    result = await model.inference(req)
    return result

@app.route('/', methods=['PUT'])
async def update():
    global model
    data = await request.get_json()
    req = ModelUpdateRequest(**data)
    result = await model.update_symspell(req)
    return result

if __name__ == "__main__":
    app.run()
