# Based on paulkernfeld answer to
# https://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree

from os.path import join

import sklearn
from sklearn.tree import _tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

def tree_to_code(tree
                 , feature_names
                 , function_name
                 , output_file
                 , signature_formatter
                 , end_formatter
                 , leaf_formatter
                 , if_formatter
                 , else_formatter
                 , node_end_formatter):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    output_file_handle = open(output_file, "w")

    output_file_handle.write(signature_formatter(function_name
                                                    , feature_names))

    def recurse(node
                , depth
                , output_file_handle):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            output_file_handle.write(if_formatter(name=feature_name[node]
                     , threshold=tree_.threshold[node]
                     ,indent=indent))
            recurse(tree_.children_left[node]
                    , depth + 1
                    , output_file_handle)
            output_file_handle.write(else_formatter(name=feature_name[node]
                     , threshold=tree_.threshold[node]
                     ,indent=indent))
            recurse(tree_.children_right[node]
                    , depth + 1
                    , output_file_handle)
            output_file_handle.write(node_end_formatter(indent))
        else:
            output_file_handle.write(leaf_formatter(node=tree_.value[node]
                                                    ,indent=indent))

    recurse(node=0
            , depth=1
            , output_file_handle=output_file_handle)

    output_file_handle.write(end_formatter())
    output_file_handle.close()

def python_format_leaf(node
                       , indent):
    return "{}return {}\n".format(indent
                                       , node[0][1]/(node[0][0] + node[0][1]))

def python_format_if(name
                     , threshold
                     ,indent):
    return "{}if {} <= {}:\n".format(indent
                                     , name
                                     , threshold)

def python_format_else(name
                     , threshold
                     ,indent):
    return "{}else:  # if {} > {}\n".format(indent
                                            , name
                                            , threshold)
def python_format_signature(function_name
                                , feature_names):
    return "def {}}({}):\n".format(function_name
                                        , ", ".join(feature_names))

def tree_to_python(tree
                 , feature_names
                 , function_name
                 , output_file):
    tree_to_code(tree
                 , feature_names
                 , function_name
                 , output_file
                 , signature_formatter=python_format_signature
                 , end_formatter=lambda : ""
                 , leaf_formatter=python_format_leaf
                 , if_formatter=python_format_if
                 , else_formatter=python_format_else
                 , node_end_formatter=lambda x : "")

def sql_format_leaf(node
                       , indent):
    return "{indent} return {pos_rate} # ({pos} out of {pop})\n".format(
                        indent=indent
                        , pos_rate=node[0][1]/(node[0][0] + node[0][1])
                        , pos=node[0][1]
                        , pop=(node[0][0] + node[0][1]))

def sql_format_if(name
                     , threshold
                     ,indent):
    return "{}case when {} <= {} then\n".format(indent
                                     , name
                                     , threshold)

def sql_format_else(name
                     , threshold
                     ,indent):
    return "{}else  # if {} > {}\n".format(indent
                                            , name
                                            , threshold)

def sql_format_signature(function_name
                                , feature_names):
    parameters = ["{} int64".format(i) for i in feature_names]
    return "create or replace function {} ({}) as (\n".format(function_name
                                                                , ", ".join(parameters))


def tree_to_sql(tree
                 , feature_names
                 , function_name
                 , output_file):
    tree_to_code(tree
                 , feature_names
                 , function_name
                 , output_file
                 , signature_formatter=sql_format_signature
                 , end_formatter=lambda : ")"
                 , leaf_formatter=sql_format_leaf
                 , if_formatter=sql_format_if
                 , else_formatter=sql_format_else
                 , node_end_formatter=lambda x : "{}end ".format(x))


def random_forest_to_sql(rf
                         , feature_names
                         , function_name_prefix
                         , output_file_prefix):
    for i in range(rf.n_estimators):
        tree_to_sql(tree=rf.estimators_[i]
                    , feature_names=feature_names
                    , function_name="{}_{}".format(function_name_prefix
                                           , i)
                    , output_file="{}_{}.sql".format(output_file_prefix
                                           , i))

    agg_sql = sql_format_signature(function_name_prefix +"_agg"
                                , feature_names)
    agg_sql += " \n(\n"
    agg_sql += " + ".join(["{}_{}({})\n".format(function_name_prefix
                                           , i
                                           , ",".join(feature_names)) for i in range(rf.n_estimators)])
    agg_sql += ") /{}\n)".format(rf.n_estimators)

    output_file_handle = open("{}_{}.sql".format(output_file_prefix
                                           , "agg"), "w")
    output_file_handle.write(agg_sql)
    output_file_handle.close()


def models_to_text(models_dict
                   , output_path: str
                   , file_name_format):

    for model_name in models_dict.keys():
        if isinstance(models_dict[model_name]['model']
                , sklearn.tree._classes.DecisionTreeClassifier):
            tree_to_sql(models_dict[model_name]['model']
                        , models_dict[model_name]['model'].feature_names_in_
                        , model_name
                        , output_file=join(output_path
                                           , file_name_format).format(model_name=model_name))

        elif isinstance(models_dict[model_name]['model']
                , sklearn.ensemble._forest.RandomForestClassifier):
            random_forest_to_sql(models_dict[model_name]['model']
                         , models_dict[model_name]['model'].feature_names_in_
                         , model_name
                         , output_file_prefix=join(output_path
                                           , file_name_format).format(model_name=model_name))
