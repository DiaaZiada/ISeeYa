from io_blueprint import IOBlueprint
from flask_socketio import emit
from iseeya.models import User
from iseeya.ai import  models, ct, transforms 
from iseeya.streamer.utils import get_outputs
import pickle
streamer = IOBlueprint('/streamer')

@streamer.on('forward')
def forward(data):
    
    token = data.get('token')
    inputs = pickle.loads(data.get('inputs'))
    opts = data.get('opts')

    if User.verify_stream_token(token):
        outputs = get_outputs(inputs, opts)
        emit('reciver', pickle.dumps(outputs), namespace='/')
    else:
        emit('reciver', pickle.dumps({"message":"That is an invalid or expired token"}), namespace='/')
