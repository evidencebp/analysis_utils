import pandas as pd

def compare_twin_behaviours(first_behaviour : pd.DataFrame
                            , second_behaviour : pd.DataFrame
                            , keys : list
                            , comparision_columns : list
                            , comparision_function) -> pd.DataFrame:

    first_to_match = first_behaviour[keys + comparision_columns].copy()
    second_to_match = second_behaviour[keys + comparision_columns].copy()
    joint = pd.merge(first_to_match, second_to_match, on=keys)

    joint_cols = keys.copy()
    for i in comparision_columns:
        key = i + '_cmp'
        joint_cols.append(key)
        joint[key] = joint.apply(lambda x : comparision_function(x[i +'_x'], x[i +'_y'])
                                ,axis=1)

    return joint[joint_cols]

