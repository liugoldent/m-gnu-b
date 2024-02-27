def getDifferenceFunc(list1, list2):
    result_list = [item for item in list2 if item['code'] not in [a['code'] for a in list1]]
    return result_list