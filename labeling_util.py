
def get_false_positives(df
                        , classifier
                        , concept):
    return df[(df[classifier] == True) & (df[concept] == False)]

def get_false_negatives(df
                        , classifier
                        , concept):
    return df[(df[classifier] == False) & (df[concept] == True)]
