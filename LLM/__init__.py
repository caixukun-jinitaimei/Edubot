from .Linly import Linly
from .Qwen import Qwen
from .Gemini import Gemini
from .ChatGPT import ChatGPT
from .ChatGLM import ChatGLM
# import Linly
# import Qwen
# import Gemini

def test_Linly(question = "如何应对压力？", mode='offline', model_path="Linly-AI/Chinese-LLaMA-2-7B-hf"):
    llm = Linly(mode, model_path)
    answer = llm.generate(question)
    print(answer)
    
def test_Qwen(question = "如何应对压力？", mode='offline', model_path="Qwen/Qwen-1_8B-Chat"):
    llm = Qwen(mode, model_path)
    answer = llm.generate(question)
    print(answer)
    
def test_Gemini(question = "如何应对压力？", model_path='gemini-pro', api_key=None, proxy_url=None):
    llm = Gemini(model_path, api_key, proxy_url)
    answer = llm.generate(question)
    print(answer)
    
def test_ChatGPT(question = "如何应对压力？", model_path = 'gpt-3.5-turbo', api_key = None, proxy_url = None):
    llm = ChatGPT(model_path, api_key, proxy_url)
    answer = llm.generate(question)
    print(answer)
    
class LLM:
    def __init__(self, mode='offline'):
        self.mode = mode
        
    def init_model(self, model_name, model_path, api_key=None, proxy_url=None):
        if model_name not in ['Linly', 'Qwen', 'Gemini', 'ChatGLM', 'ChatGPT']:
            raise ValueError("model_name must be 'Linly', 'Qwen', 'ChatGPT' or 'Gemini'(其他模型还未集成)")
        if model_name == 'Linly':
            llm = Linly(self.mode, model_path)
        elif model_name == 'Qwen':
            llm = Qwen(self.mode, model_path)
        elif model_name == 'Gemini':
            llm = Gemini(model_path, api_key, proxy_url)
        elif model_name == 'ChatGLM':
            llm = ChatGLM(self.mode, model_path)
        elif model_name == 'ChatGPT':
            llm = ChatGPT(model_path, api_key, proxy_url)
        return llm
    
    def test_Linly(self, question="如何应对压力？", model_path="Linly-AI/Chinese-LLaMA-2-7B-hf"):
        llm = Linly(self.mode, model_path)
        answer = llm.generate(question)
        print(answer)

    def test_Qwen(self, question="如何应对压力？", model_path="Qwen/Qwen-1_8B-Chat"):
        llm = Qwen(self.mode, model_path)
        answer = llm.generate(question)
        print(answer)

    def test_Gemini(self, question="如何应对压力？", model_path='gemini-pro', api_key=None, proxy_url=None):
        llm = Gemini(model_path, api_key, proxy_url)
        answer = llm.generate(question)
        print(answer)
    
    def test_ChatGPT(self, question="如何应对压力？", model_path = 'gpt-3.5-turbo', api_key = None, proxy_url = None):
        llm = ChatGPT(model_path, api_key, proxy_url)
        answer = llm.generate(question)
        print(answer)
        
    def test_ChatGLM(self, question="如何应对压力？", model_path="THUDM/chatglm-6b"):
        llm = ChatGLM(mode=self.mode, model_name_or_path=model_path)
        answer = llm.generate(question)
        print(answer)

if __name__ == '__main__':
    llm = LLM(mode='offline')
    # llm.test_Qwen()
    # llm.test_Linly()
    # llm.test_Gemini()
    # llm.test_ChatGLM()