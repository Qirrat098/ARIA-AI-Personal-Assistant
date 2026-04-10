memory = []

def add_memory(user, assistant):
    memory.append({"user": user, "assistant": assistant})

def get_memory():
    return memory