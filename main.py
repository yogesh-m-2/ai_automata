from chatgpt import Chat

gpt = Chat(kill_chrome=True)
res = gpt.prompt("tell me a story about world war 1")
print(res)