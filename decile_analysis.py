from math import log10
import os
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

from configuration import DATA_PATH, ANALYZED_YEAR, FIGURES_PATH
from feature_pair_analysis import bin_metric_by_quantiles
from repo_utils import get_valid_repos


# TODO - add longevity
metrics = ['capped_avg_file', 'avg_capped_files', 'commit_per_user_above_11_cap', 'age'
    , 'repo_all_commits', 'authors', 'stargazers_count'
    , 'repo_all_commits_log10', 'authors_log10', 'stargazers_count_log10'
    , 'continuing_developers_ratio', 'comming_involved_developers_ratio']


def decile_analysis(major_extensions_file
                    , coupling_file
                    , commits_per_user_file
                    , churn_file
                    , onboarding_file
                    , output_file):

    repos = get_valid_repos()

    repos = repos.rename(columns={'commits' : 'repo_all_commits'})

    bin_metric_by_quantiles(repos
                            , 'y2019_ccp'
                            , 'y2019_ccp_10bins'
                            , bins=10
                            )
    rep_size = pd.read_csv(major_extensions_file)
    df = pd.merge(repos,rep_size,on='repo_name', how='left')

    coupling_size = pd.read_csv(coupling_file)
    coupling_size = coupling_size[coupling_size.year == ANALYZED_YEAR]

    df = pd.merge(df, coupling_size, on='repo_name', how='left')

    users_per_project = pd.read_csv(commits_per_user_file)
    users_per_project = users_per_project[users_per_project.year == ANALYZED_YEAR]
        
    df = pd.merge(df, users_per_project, on='repo_name', how='left')

    df['commit_per_user'] = df.apply(
        lambda x: x.y2019_commits/x.users if x.users > 0 else None, axis=1)
    df['commit_per_user_above_11'] = df.apply(
        lambda x: x.users_above_11_commits/x.users_above_11 if x.users_above_11 > 0 else None, axis=1)

    df['commit_per_user_cap'] = df.apply(
        lambda x: x.users_capped_commit/x.users if x.users > 0 else None, axis=1)
    df['commit_per_user_above_11_cap'] = df.apply(
        lambda x: x.commits_above_11_500_cap/x.users_above_11 if x.users_above_11 > 0 else None, axis=1)


    df['repo_all_commits_log10']= df.repo_all_commits.map(lambda x: log10(x) if x> 0 else x)
    df['authors_log10']= df.authors.map(lambda x: log10(x) if x> 0 else x)
    df['stargazers_count_log10']= df.stargazers_count.map(lambda x: log10(x) if x> 0 else x)

    churn = pd.read_csv(churn_file)
    churn = churn[churn.year == ANALYZED_YEAR-1]

    df = pd.merge(df, churn, on='repo_name')

    onboarding = pd.read_csv(onboarding_file)
    onboarding = onboarding[onboarding.year == ANALYZED_YEAR]
    df = pd.merge(df, onboarding, on='repo_name')

    aggregations = {i : 'mean' for i in metrics}
    aggregations['repo_name'] = 'count'
    g = df.groupby('y2019_ccp_10bins', as_index=False).agg(aggregations)


    g.to_csv(output_file)

    plot_all_metrics(df
                     , grouping_column='y2019_ccp_10bins')

    return df

def plot_all_metrics(df
                 , grouping_column):

    df = df.sort_values(grouping_column)

    for metric_column in metrics:
        plot_deciles(df
                     , grouping_column=grouping_column
                     , metric_column=metric_column
                     , output_file=os.path.join(FIGURES_PATH, metric_column + '.png'))


def plot_deciles(df
                 , grouping_column
                 , metric_column
                 , output_file):

    fig = go.Figure()
    item = 0;
    for cur_group in df[grouping_column].unique():
        color = 'rgb(' +str(20*item +1) + ',' + str(100 + 10*item) +',' + str(254 - 15*item) + ')'
        trace = go.Box(
            y=df[df[grouping_column] == cur_group][metric_column].tolist(),
            name=str(cur_group),
            marker=dict(
                color=color,
            ),
            boxpoints=False,
            boxmean=True
        )
        fig.add_trace(trace)
        item += 1

    fig.update_layout(
        title="CCP groups vs. " + metric_column,
        xaxis_title="CCP groups",
        yaxis_title=metric_column,
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    fig.show()
    fig.write_image(output_file)


def plot_longevity(repo_properties_file
                   , longevity_file):
    """
    Longevity is on 2018 porjects, which are in a different file and therfore get a different function.
    """
    repos = pd.read_csv(repo_properties_file)
    longevity = pd.read_csv(longevity_file)

    df = pd.merge(repos, longevity, on='repo_name', how='left')
    df = df[(df.fork == False) & (df.y2018_ccp > 0) & (df.y2018_ccp < 1)]

    df['after_2019_end'] = df.days_from_2019_end.map(lambda x: 1 if x > 0 else 0)
    grouping_column = 'y2018_ccp_10bins'

    repos_2019 = get_valid_repos()
    bins = 10
    cuts = [0.0] + [repos_2019['y2019_ccp'].quantile((1.0/bins)*i) for i in range(1, bins)] + [1.0]

    df[grouping_column] = pd.cut(df['y2018_ccp'], cuts)

    """
    bin_metric_by_quantiles(df
                            , 'y2018_ccp'
                            , grouping_column
                            , bins=10
                            )
    """
    df = df.sort_values(grouping_column)
    plot_deciles(df
                 , grouping_column
                 , 'after_2019_end'
                 , os.path.join(FIGURES_PATH,'longevity.png'))

def run_plot_longevity():
    plot_longevity(repo_properties_file=os.path.join(DATA_PATH, 'repos_full_2018.csv')
                   , longevity_file=os.path.join(DATA_PATH, 'longevity_2018.csv'))
def run_decile_analysis():
        return decile_analysis(major_extensions_file=
                               os.path.join(DATA_PATH
                                            , 'repo_programming_file_size_with_major_extension99.csv')
                               , coupling_file=os.path.join(DATA_PATH
                                                        , 'coupling_by_repo.csv')
                               , commits_per_user_file=os.path.join(DATA_PATH
                                                                    , 'project_user_contribution_stats.csv')
                               , churn_file=os.path.join(DATA_PATH
                                    , 'invovled_developers_churn.csv')
                               , onboarding_file = os.path.join(DATA_PATH
                                       , 'developer_on_boarding.csv')
                               , output_file=os.path.join(DATA_PATH, 'decile_bins.csv'))

if __name__ == '__main__':
    df = run_decile_analysis()
    run_plot_longevity()