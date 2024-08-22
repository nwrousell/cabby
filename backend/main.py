from utils import print_green
from vector_database import VectorDatabase
from agent import Conversation, OpenAILLM, Agent


if __name__ == '__main__':
    db = VectorDatabase()
    
    conversation = Conversation()
    agent = Agent(llm=OpenAILLM())
    
    query = input('Query: ')
    while query != 'q':
        documents = db.retrieve_top_k(db.gen_embedding(query))
        response = agent(documents, conversation)
        print_green(response)
        
        conversation.add_message(query, 'user')
        conversation.add_message(response, 'assistant')
        
        query = input('Query: ')
        
        