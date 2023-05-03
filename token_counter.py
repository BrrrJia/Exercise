import nltk

def token_counter(file_name):
    with open(file_name,'r') as text_file:
        text = text_file.readlines()
        counter = []
        for sentence in text:
            word_list = nltk.word_tokenize(sentence)
            token_list = set(word_list)
            token_list_length = len(token_list)
            counter.append(token_list_length)
        maximum = max(counter)
        minimum = min(counter)
        mean = sum(counter)/len(counter)
        return maximum, minimum, mean

        

if __name__ == '__main__':
    token_info = token_counter('corpus.txt')
    print('Maximum: ', token_info[0])
    print('Minimum: ', token_info[1])
    print('Im Durchschnitt: ', token_info[2])
                  
        


