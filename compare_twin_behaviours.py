import pandas as pd

COMPARISON_SUFFIX = '_cmp'


def compare_twin_behaviours(first_behaviour : pd.DataFrame
                            , second_behaviour : pd.DataFrame
                            , keys : list
                            , comparision_columns : list
                            , comparision_function
                            , filtering_function = None
                            , differences_num : str = None) -> pd.DataFrame:

    first_to_match = first_behaviour[keys + comparision_columns].copy()
    second_to_match = second_behaviour[keys + comparision_columns].copy()
    joint = pd.merge(first_to_match, second_to_match, on=keys)

    if filtering_function:
        filter_column = 'filter'
        joint[filter_column] = joint.apply(filtering_function, axis=1)
        joint = joint[~joint[filter_column]]
        joint = joint.drop(columns=[filter_column])

    joint_cols = keys.copy()
    for i in comparision_columns:
        key = i + COMPARISON_SUFFIX
        joint_cols.append(key)
        joint[key] = joint.apply(lambda x : comparision_function(x[i +'_x'], x[i +'_y'])
                                ,axis=1)

    if differences_num:
        joint[differences_num] = joint[[i + COMPARISON_SUFFIX for i in comparision_columns]].sum(axis=1)
        relevant_columns = joint_cols + [differences_num]
    else:
        relevant_columns = joint_cols

    return joint[relevant_columns]

