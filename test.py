all_list = ['stikejdij', 'stik', 'stol', 'kit', 'korm', 'steik']
x = 'korpus'

len_x = len(x)

kk = []

for i in range(len_x):
    if i == 0:
        xx = x
        print(f'item 0: {x}')
    else:
        xx = x[:-i]
        print(f'item {-i}: {x[:-i]}')

    count_x_in_all = sum(1 for item in all_list if xx in item)
    len_all = len(all_list)

    k = count_x_in_all / len_all
    print(f'Ratio: {k}')
    kk.append(k)

sum_k = sum(kk)
similarity = (sum_k/len_x)
print(similarity)
