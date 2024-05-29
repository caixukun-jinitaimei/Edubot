from g4f import ChatCompletion, Provider

class FreeGPT:
    def call(self, query: str):
        chat_completion = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            provider="", 
            # stream=True,
        )  
        return True, chat_completion

freeGPTMgr = FreeGPT()