import nltk
import more_itertools as mit

def tokenize(seq: str):
    """tokenize the sring sequence

    Parameters:
    seq(str): IOB-labeled sequence

    Returns:
    token_list(list): the token from the sequence

    """
    token_list = nltk.word_tokenize(seq)
    return token_list


def name_position(token_list: list):
    """return the name position in the token list

    Parameters:
    token_list(list): token list from IOB-labeled sequence

    Returns:
    bank(dict): the dictionary of the name position, key is the position of 'B', value is the position of the rest part
    
    """
    bank = {}
    enum_seq = mit.peekable(enumerate(token_list))
    for count,elem in enum_seq:
        if elem == 'B':
            bank[count] = []
            counter = count
            if count < len(token_list)-1:
                while enum_seq.peek()[1] == 'I':
                    next(enum_seq)
                    counter +=1
                    bank[count].append(counter)
                    if counter == len(token_list)-1:
                        break
    return bank


def name_counter(token_list: list):
    """count how many names are in the token list

    Parameters:
    token_list(list): token list from IOB-labeled sequence

    Returns:
    counter(int): the name count
    
    """
    counter = 0
    for elem in token_list:
        if elem == 'B':
            counter+=1
    return counter


def evaluate_exact(truth_seq, predict_seq):
    """exactly count how many names are in the token list

    Parameters:
    truth_seq(str): IOB-labeled sequence from ground-truth
    predict_seq(str): IOB-labeled sequence from prediction

    Raises:
    ZeroDivisionError: if tp+fp = 0 or tp+fn = 0
    
    Returns:
    precision(float): the precision of the prediction compared with the ground-truth
    recall(float): the recall of the prediction compared with the ground-truth
    f_score(float): the f-score of the prediction compared with the ground-truth
    
    """
    try:
        name_in_truth = name_position(truth_seq)
        name_in_prediction = name_position(predict_seq)
        tp = 0
        for key,value in name_in_prediction.items():
            if key in name_in_truth:
                if value == name_in_truth[key]:
                    tp+=1
        true_name_count = name_counter(truth_seq)
        predict_name_count = name_counter(predict_seq)
        fp = predict_name_count - tp
        fn = true_name_count-tp
        precision = round(tp/(tp+fp),2)
        recall = round(tp/(tp+fn),2)
        f_score = round(2*precision*recall/(precision+recall),2)
    except ZeroDivisionError:
        precision = 0
        recall = 0
        f_score = 0
    return precision, recall, f_score


def evaluate_partial(truth_seq, predict_seq):
    """partially count how many names are in the token list

    Parameters:
    truth_seq(str): IOB-labeled sequence from ground-truth
    predict_seq(str): IOB-labeled sequence from prediction

    Raises:
    ZeroDivisionError: if tp+fp = 0 or tp+fn = 0
    
    Returns:
    precision(float): the precision of the prediction compared with the ground-truth
    recall(float): the recall of the prediction compared with the ground-truth
    f_score(float): the f-score of the prediction compared with the ground-truth
    
    """
    try:
        name_in_truth = name_position(truth_seq)
        true_name_count = name_counter(truth_seq)
        predict_name_count = name_counter(predict_seq)
        tp = 0
        for key,value in name_in_truth.items():
            predict_name_counter = predict_name_count
            if predict_seq[key] != 'O':
                tp+=1
                predict_name_counter-=1
                if predict_name_counter == 0:
                    break
            else:
                for elem in value:
                    if predict_seq[elem] != 'O':
                        tp+=1
                        break
        fp = predict_name_count - tp
        fn = true_name_count-tp
        precision = round(tp/(tp+fp),2)
        recall = round(tp/(tp+fn),2)
        f_score = round(2*precision*recall/(precision+recall),2)
    except ZeroDivisionError:
        precision = 0
        recall = 0
        f_score = 0
    return precision, recall, f_score


# test
if __name__ == '__main__':
    # Example 1
    gold_token_label_1 = tokenize('O B I I B I I O B O')
    predict_token_label_1 = tokenize('O B I I B I O O O O')
    evaluate_exact_1 = evaluate_exact(gold_token_label_1, predict_token_label_1)
    evaluate_partial_1 = evaluate_partial(gold_token_label_1, predict_token_label_1)
    print(f'gold: O B I I B I I O B O, \npredict: O B I I B I O O O O, \nexact evaluation: {evaluate_exact_1}, \npartial evaluation: {evaluate_partial_1};\n')
    # Example 2
    gold_token_label_2 = tokenize('O B I I B I I O B O')
    predict_token_label_2 = tokenize('B O B B O B B B O B')
    evaluate_exact_2 = evaluate_exact(gold_token_label_2, predict_token_label_2)
    evaluate_partial_2 = evaluate_partial(gold_token_label_2, predict_token_label_2)
    print(f'gold: O B I I B I I O B O, \npredict: B O B B O B B B O B, \nexact evaluation: {evaluate_exact_2}, \npartial evaluation: {evaluate_partial_2};\n')
    # Example 3
    gold_token_label_3 = tokenize('O B I I B I I O B O')
    predict_token_label_3 = tokenize('B I I I I I I I I I')
    evaluate_exact_3 = evaluate_exact(gold_token_label_3, predict_token_label_3)
    evaluate_partial_3 = evaluate_partial(gold_token_label_3, predict_token_label_3)
    print(f'gold: O B I I B I I O B O, \npredict: B I I I I I I I I I, \nexact evaluation: {evaluate_exact_3}, \npartial evaluation: {evaluate_partial_3};\n')
    # Example 4
    gold_token_label_4 = tokenize('B I I I I I I I I I')
    predict_token_label_4 = tokenize('B B B B B B B B B B')
    evaluate_exact_4 = evaluate_exact(gold_token_label_4, predict_token_label_4)
    evaluate_partial_4 = evaluate_partial(gold_token_label_4, predict_token_label_4)
    print(f'gold: B I I I I I I I I I, \npredict: B B B B B B B B B B, \nexact evaluation: {evaluate_exact_4}, \npartial evaluation: {evaluate_partial_4}.')
