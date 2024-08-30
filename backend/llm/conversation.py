class Conversation:
    def __init__(self, messages: list[dict] = None):
        self.messages = messages if messages is not None else []
    
    def add_message(self, message: str, role: str):
        self.messages.append({ 'message': message, 'role': role })

    def get_context(self):
        history = '' if len(self.messages) > 0 else 'NONE — START OF CONVERSATION'
        for i in range(len(self.messages)):
            r = self.messages[i]
            if i % 2 == 0:
                history += f'Student: {r['message']}\n'
            else:
                history += f'Cabby: {r['message']}\n\n'
        return history