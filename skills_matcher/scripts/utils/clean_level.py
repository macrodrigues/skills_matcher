# INSTRUCTIONS

# 1) data_cleaned['LEVEL'] = data_cleaned['LEVEL'].apply(clean_level)


def clean_level(s):
    valid_level = ['phd', 'master', 'bachelor', 'hnd', 'hnc', 'degree']
    better_list = []
    for degree in s:
        better_list += degree.split(" ")

    new_list = [degree.replace('a ', '') for degree in better_list]
    new_list = [degree.replace(' and ', ' ') for degree in new_list]
    new_list = [degree for degree in new_list if len(degree) > 2]
    new_list = [degree.replace('mscbsc', 'msc bsc') for degree in new_list]
    new_list = [degree.replace('msc', 'master') for degree in new_list]
    new_list = [degree.replace('masters', 'master') for degree in new_list]
    new_list = [degree.replace('bachelors', 'bachelor') for degree in new_list]
    new_list = [degree.replace('bsc', 'bachelor') for degree in new_list]
    new_list = [
        degree.replace('ba', 'bachelor')
        if not 'bachelor' in degree else 'bachelor' for degree in new_list
    ]

    new_list = [
        degree.replace('postgraduate degree', 'degree') for degree in new_list
    ]
    new_list = [degree.replace('university', 'degree') for degree in new_list]
    new_list = [degree.replace('educated', 'degree') for degree in new_list]
    new_list = [degree.replace('deploma', 'degree') for degree in new_list]
    new_list = [degree.replace('graduate', 'degree') for degree in new_list]
    new_list = [degree.replace('nvq', 'degree') for degree in new_list]
    new_list = [
        degree.replace(degree, 'degree') if 'degree' in degree else degree
        for degree in new_list
    ]

    new_list = [degree for degree in new_list if degree in valid_level]

    new_list = list(set(new_list))

    if len(new_list) > 1:
        if 'degree' in new_list:
            new_list.remove('degree')

    new_list = sorted(new_list, key=lambda x: valid_level.index(x))

    return new_list
