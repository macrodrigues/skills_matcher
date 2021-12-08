import pandas as pd

### INSTRUCTIONS

# 1) table = print_final_table(<position>, <data>)
# position is the position the user selected
# data is the dataframe that contains all job descriptions, cleaned
# example: print_final_table('Applied Physicist id54308', data_cleaned)

### IMPLEMENTATION FOR STREAMLIT

# 1) table = print_final_table(<position>, <data>)
# 2) hdf = table.assign(hack='').set_index('hack')
# 2) st.table(hdf)


def print_final_table(position, data):

    index = data.index[data['position'] == position].to_list()

    list_skills = data['SKILL'][index].to_list()[0]
    list_knowledge = data['KNOWLEDGE'][index].to_list()[0]
    list_min_exp = data['MIN_EXP'][index].to_list()[0]
    list_level = data['LEVEL'][index].to_list()[0]

    table = pd.DataFrame({
        'skills': pd.Series(list_skills),
        'knowledge': pd.Series(list_knowledge),
        'level': pd.Series(list_min_exp),
        'min_exp': pd.Series(list_level)
    })

    table = table.fillna('')

    return table
