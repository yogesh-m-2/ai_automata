from chatgpt import Chat

gpt = Chat(kill_chrome=True)
res = gpt.generate_image("generate an image of a good quote")
print(res)