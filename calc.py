from tokenizer import Token, Tokenizer

if __name__ == "__main__":
    program = "3 & 5 + 899 0  ^ ~"
    t = Tokenizer(program)
    while(t.has_more_tokens()):
        print(t.get_next_token())