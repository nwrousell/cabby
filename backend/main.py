
from llm.util import print_green
from db.vectordb import VectorDatabase
from llm.conversation import Conversation
from llm.agent import Engine
from llm.util import debug_print

import argparse
import flask

app = flask.Flask(__name__)


'''Health check endpoint'''
@app.route('/health', methods=['GET'])
def health():
    return 'HEALTH CHECK PASSED'


@app.route('/query', methods=['POST', 'OPTIONS'])
def query():
    if flask.request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600',
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    query = flask.request.json['query']
    messages = flask.request.json['messages']
    conversation = Conversation(messages=messages)
    engine = Engine()

    response = engine(query, conversation)

    ''' Stream Response '''
    def stream():
        for chunk in response:
            yield chunk

    return stream(), 200, headers



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--mode', type=str, default='', help='local | server')
    args = parser.parse_args()

    if args.mode == 'local':
        conversation = Conversation()
        engine = Engine()
        
        query = input('Enter query: ')
        while query:
            response = engine(query, conversation)
            debug_print([response])
            
            conversation.add_message(query, 'user')
            conversation.add_message(response, 'assistant')
            
            query = input('Query: ')
    elif args.mode == 'server':
        app.run(debug=True, host="0.0.0.0", port=8080)
        
        