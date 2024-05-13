import pandas as pd

from analysis_utils.greedy_set_cover import greedy_set_cover

def get_lb_disagreements(df: pd.DataFrame
                        , lb: list[str]
                        , key: str):

    disagreements = []
    # first iterator on functions
    for i in lb:
        # second iterator on functions
        for j in lb:
            # Breaking symetry
            if i < j:
                cur_disagreements = df[df[i] != df[j]][[key]].copy()
                cur_disagreements['first_function'] = i
                cur_disagreements['second_function'] = j
                disagreements.append(cur_disagreements)

    disagreements_df = pd.concat(disagreements)

    return disagreements_df


def build_set_representation(disagreements_df: pd.DataFrame
                             , key: str):

    functions_columns = ['first_function', 'second_function']

    sets_to_cover = []

    functions_to_cover = \
        disagreements_df[
            functions_columns].drop_duplicates().sort_values(functions_columns)
    # Go over functions, sorting is to ease understanding
    for _, cur_functions in functions_to_cover.iterrows():
        covering_samples = disagreements_df[
                (disagreements_df['first_function'] == cur_functions['first_function'])
                & (disagreements_df['second_function'] == cur_functions['second_function'])
            ][key].values.tolist()
        covering_samples = frozenset(covering_samples)
        sets_to_cover.append(covering_samples)

    return sets_to_cover

def classifiers_disagreements_cover(df: pd.DataFrame
                        , lb: list[str]
                        , key: str
                        , coverage_file: str = None)-> pd.DataFrame:
    disagreements_df = get_lb_disagreements(df
                                            , lb
                                            , key)

    sets_to_cover = build_set_representation(disagreements_df
                                    , key)

    cover = greedy_set_cover(sets_to_cover)

    cover_df = pd.DataFrame(cover
                            , columns=[key])

    if coverage_file:
        cover_df.to_csv(coverage_file
                        , index=False)

    return cover_df
