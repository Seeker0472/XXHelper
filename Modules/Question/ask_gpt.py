from openai import OpenAI
from General.secret import Open_AI_API_KEY, Open_AI_MIRROR_URL

client = OpenAI(
    api_key=Open_AI_API_KEY,
    base_url=Open_AI_MIRROR_URL
)

def ask_gpt3(text,contents):
    """
    问答,返回问题的答案
    :param text: 问题
    :param contents: 选项(List)
    :return: 答案(str)
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system",
             "content": "You are an assistant,skilled in answering questions about China"},
            {"role": "user",
             "content": f"Please return only the right answer and nothing else. \nExample:input:{{'question': 'What is the capital of China?','options': ['Beijing','Shanghai','Guangzhou','Shenzhen']}} output: Beijing .\nQuestion: {text}\nOptions: {contents}"}
        ]
    )
    response = completion.choices[0].message.content
    print(response)
    return response