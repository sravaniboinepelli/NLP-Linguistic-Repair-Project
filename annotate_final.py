import re
from nltk.util import ngrams
from collections import Counter


# ip = open("01_nltk.txt", "r")
# op = open("ann/1.txt", "w")
first_tag_start ="("
first_tag_end =")"
second_tag_start ="{"
second_tag_end ="}"

first_tag_start_pos =0
first_tag_end_pos = 0
second_tag_start_pos =0
second_tag_end_pos = 0


ip = open("input/preprocessed/test1_pre.txt", "r")
op = open("ann/test1_auto.txt", "w")
def ngrams(tokens, n):
#     sentence = sentence.lower()
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [ngram for ngram in ngrams]
def get_repeated_words_in_ngram(ngram):
    count_ng = Counter(ngram)
    repeated_words = []
    for key, value in count_ng.items():
        # print(key, value)
        if value > 1:
            repeated_words.append(key)
    # print("repeated_words:", repeated_words)
    return repeated_words
def get_ngram_sent_from_lst(ngram_list, prev_num_ngrams,length, last ):
    sent =""
    first_tag_start_f = False
    second_tag_start_f = False
    first_tag_end_f= False
    second_tag_end_f = False
    if prev_num_ngrams == 5:
        size1 = length
        sent_ngram = ""
        len =1
        found_non_tag = False
        tags = [first_tag_end, second_tag_end, first_tag_start, second_tag_end]
        while size1 > 5:
            # print("end", )
            if found_non_tag == True:
                break
            sent_ngram += ngram_list[size1-len]
            # print("sent_ngrame", sent_ngram)
            if ngram_list[size1-len] not in tags:
               found_non_tag = True
            len +=1
        return sent_ngram, 1
    if prev_num_ngrams != 0:
       return "", 0
    for ngram in ngram_list:
        sent += ngram + " "
        if ngram == first_tag_end:
           first_tag_end_f = True
        if ngram == first_tag_start:
           first_tag_start_f = True
        if ngram == second_tag_end:
           second_tag_end_f = True
        if ngram == second_tag_start:
           second_tag_start_f = True
    if second_tag_end_f == True and second_tag_start_f == True:
       return sent, 5
    elif last == True:
       return sent, 0
    # if first_tag_end_f == True and first_tag_start_f == True:
    #     return sent, 0
    else:
        sent_ngram = ""
        sent_ngram +=ngram_list[0] + " "
        if ngram_list[0] == first_tag_start or ngram[0] == second_tag_start:
           sent_ngram +=ngram_list[1] + " "
        return sent_ngram, 0



def check_end_tag_in_ngram(ngram_list):
    sent =""
    found_end_tag = False
    for ngram in ngram_list:
        sent += ngram + " "
        if ngram == first_tag_end or ngram == second_tag_end:
           found_end_tag = True
    return found_end_tag, sent, ngram
def get_second_last_index(ngram, word):
    reversed_list = list(reversed(ngram))
    reversed_index_pos = reversed_list.index(word, 0)
    last_index_pos = len(ngram) -reversed_index_pos -1
    try:
        second_last_index =  len(ngram) - reversed_list.index(word, reversed_index_pos)-1
        return secod_last_index+1
    except:
        return last_index_pos+1

def tag_ngram_words(ngram_seq):
    tag_pos_list =[]
    prev_ngram_word = None
    ngram_seq_idx = 0
    for ngram in ngram_seq:
        tag_pos_dict ={"first_tag_start_pos": -1, "first_tag_end_pos": -1,"second_tag_start_pos": -1,"second_tag_end_pos": -1}
        rep_words = get_repeated_words_in_ngram(ngram)
        rep_num = 0
        for rep in rep_words:
            # print("rep", rep)
            if rep_num == 0:
                # print(prev_ngram_word, rep)
                if prev_ngram_word == rep:
                    # print("adjacentword")
                    tag_pos_list[ngram_seq_idx-1]["first_tag_start_pos"]= -1
                    # tag_pos_list[ngram_seq_idx-1]["second_tag_start_pos"] = 1
                    if tag_pos_list[ngram_seq_idx-1]["second_tag_end_pos"] != tag_pos_list[ngram_seq_idx-1]["first_tag_end_pos"]-1:
                        tag_pos_list[ngram_seq_idx-1]["first_tag_end_pos"]= -1
                    # tag_pos_list[ngram_seq_idx-1]["second_tag_end_pos"] -=1
                    # print("list", tag_pos_list)
                tag_pos_dict["first_tag_start_pos"] = ngram.index(rep)
                tag_pos_dict["first_tag_end_pos"] = len(ngram) - list(reversed(ngram)).index(rep)-1
                # print(tag_pos_dict)
            else:
                tag_pos_dict["second_tag_start_pos"] = ngram.index(rep)
                tag_pos_dict["second_tag_end_pos"] = len(ngram) - list(reversed(ngram)).index(rep)-1
                # print("second repeat", tag_pos_dict["first_tag_end_pos"])
                # print(tag_pos_dict)
            rep_num += 1
        if rep_num > 2:
            print("greater Rep num:", rep_num)
        if tag_pos_dict["first_tag_end_pos"] <  tag_pos_dict["second_tag_end_pos"]:
           # print("change end")
           tag_pos_dict["first_tag_end_pos"] = tag_pos_dict["second_tag_end_pos"]+1

        tag_pos_list.append(tag_pos_dict)
        prev_ngram_word = ngram[1]

        ngram_seq_idx += 1
    return tag_pos_list


if ip.mode == 'r':
    contents =ip.read()
    tokens = contents.split()
    ngram_seq = ngrams(tokens, 5)
    # print(ngram_seq)
    final_list = []
    tag_pos_list =tag_ngram_words(ngram_seq)
    # print("====")
    # print(tag_pos_list)
    new_sent = ""
    tag_pos_list_idx =0
    new_ngram_seq = []
    for ngram in ngram_seq:
        new_ngram_sent = ""
        tag_pos = tag_pos_list[tag_pos_list_idx]
        new_ngram_list = list(ngram)
        num_paren_adds =0
        if tag_pos["first_tag_start_pos"] != -1:
           new_ngram_list.insert(tag_pos["first_tag_start_pos"], first_tag_start)
           num_paren_adds +=1
        if tag_pos["first_tag_end_pos"] != -1:
           new_ngram_list.insert(tag_pos["first_tag_end_pos"]+1+num_paren_adds, first_tag_end)
           num_paren_adds +=1
        if tag_pos["second_tag_start_pos"] != -1:
           new_ngram_list.insert(tag_pos["second_tag_start_pos"]+num_paren_adds, second_tag_start)
           num_paren_adds +=1
        if tag_pos["second_tag_end_pos"] != -1:
            if tag_pos["second_tag_end_pos"] == tag_pos["first_tag_end_pos"]-1:
               new_ngram_list.insert(tag_pos["second_tag_end_pos"]+1+num_paren_adds-1, second_tag_end)
            else:
               new_ngram_list.insert(tag_pos["second_tag_end_pos"]+1+num_paren_adds, second_tag_end)

        new_ngram_seq.append(new_ngram_list)
        # print(new_ngram_list)
        tag_pos_list_idx += 1
    ngram_list_idx = 0
    size = len(new_ngram_seq)-1
    # print(new_ngram_seq)
    sent = ""
    sent_prev_ngram =""
    sent_ngram =""
    end_tag_found = False
    prev_end_tag_found = False
    sent = ""
    prev_num_ngrams = 0
    for ngram_list in new_ngram_seq:
        # print(ngram_list)
        size2 = len(ngram_list)
        if ngram_list_idx < size:
           ngram_sent, num_ngrams = get_ngram_sent_from_lst(ngram_list, prev_num_ngrams,size2, False)
           # print("ngram_sent", ngram_sent, prev_num_ngrams)
           if prev_num_ngrams != 5:
               sent += ngram_sent
           prev_num_ngrams = num_ngrams

        else:
            if prev_num_ngrams == 4:
                prev_num_ngrams = prev_num_ngrams+1
            # print(ngram_list, prev_num_ngrams+1, size2)
            ngram_sent, num_ngrams = get_ngram_sent_from_lst(ngram_list, prev_num_ngrams,size2, True)
            # print("ngram_sent", ngram_sent)
            sent += ngram_sent
            prev_num_ngrams = num_ngrams
        if prev_num_ngrams != 0:
            prev_num_ngrams -= 1
        ngram_list_idx += 1
    # print("====")
    op.write(sent)
