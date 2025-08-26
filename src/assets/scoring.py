import pandas as pd
import numpy as np
from scipy.stats import rankdata

def get_scores(scores, max_score, scale_factor=0.9):
    podium = {'Gold': [], 'Silver': [], 'Bronze': []}
    scores = scores.sort_values(by=['Score'], ascending=False)
    scores = scores[scores['Score']>0].reset_index(drop=True)
    # return scores

    # Gold
    scores_gold = scores.copy(deep=True).reset_index(drop=True)
    scores_gold['Norm'] = (scores_gold['Score'] - scores_gold['Score'].mean())/(scores_gold['Score'].max() - scores_gold['Score'].mean())
    if (scores_gold['Norm']==1).sum() > 1:
        podium['Gold'] = list(scores_gold[scores_gold['Norm']==1]['Team'])
    elif scores_gold['Norm'][0] - scores_gold['Norm'][1] <= 0.05 and scores_gold['Norm'][1] != scores_gold['Norm'][2]:
        podium['Gold'] = [scores_gold['Team'][0], scores_gold['Team'][1]]
    else:
        podium['Gold'] =  [scores_gold['Team'][0]]
    cut = len(podium['Gold'])

    # Silver
    scores_silver = scores.copy(deep=True).iloc[cut:].reset_index(drop=True)
    scores_silver['Norm'] = (scores_silver['Score'] - scores_silver['Score'].mean())/(scores_silver['Score'].max() - scores_silver['Score'].mean())
    if (scores_silver['Norm']==1).sum() > 1:
        podium['Silver'] = list(scores_silver[scores_silver['Norm']==1]['Team'])
    elif scores_silver['Norm'][0] - scores_silver['Norm'][1] <= 0.05 and scores_silver['Norm'][1] != scores_silver['Norm'][2]:
        podium['Silver'] = [scores_silver['Team'][0], scores_silver['Team'][1]]
    else:
        podium['Silver'] =  [scores_silver['Team'][0]]
    cut += len(podium['Silver'])

    # Bronze
    scores_bronze = scores.copy(deep=True).iloc[cut:].reset_index(drop=True)
    scores_bronze['Norm'] = (scores_bronze['Score'] - scores_bronze['Score'].mean())/(scores_bronze['Score'].max() - scores_bronze['Score'].mean())
    if (scores_bronze['Norm']==1).sum() > 1:
        podium['Bronze'] = list(scores_bronze[scores_bronze['Norm']==1]['Team'])
    elif scores_bronze['Norm'][0] - scores_bronze['Norm'][1] <= 0.05 and scores_bronze['Norm'][1] != scores_bronze['Norm'][2]:
        podium['Bronze'] = [scores_bronze['Team'][0], scores_bronze['Team'][1]]
    else:
        podium['Bronze'] =  [scores_bronze['Team'][0]]
    cut += len(podium['Bronze'])

    # Points
    scores_points = scores.copy(deep=True).reset_index(drop=True)
    scores_points['Norm'] = (scores_points['Score'] - scores_points[scores_points['Score']<=scores_points['Score'].mean()]['Score'].mean())/(scores_points['Score'].max() - scores_points[scores_points['Score']<=scores_points['Score'].mean()]['Score'].mean())
    scores_points['Norm'] = scores_points['Norm'].apply(lambda x: max(x, 0))
    scores_points['Scale'] = [1]*len(podium['Gold']) + [scale_factor]*len(podium['Silver']) + [scale_factor**2]*len(podium['Bronze']) + list(np.power(scale_factor, 2+rankdata(max_score-scores['Score'].to_numpy()[cut:], method='min')))
    scores_points['Point'] = scores_points['Norm'] * scores_points['Scale'] * max_score
    scores_points['Point'] = scores_points['Point'].apply(lambda x: round(max(x, 0.1*max_score) if x > 0 else 0, 2))

    scores_points['Medal'] = ['Gold']*len(podium['Gold']) + ['Silver']*len(podium['Silver']) + ['Bronze']*len(podium['Bronze']) + ['']*(len(scores_points)-cut)

    scores['Point'] = scores_points['Point']
    scores['Medal'] = scores_points['Medal']
    scores['Scale'] = scores_points['Scale']
    scores['Norm'] = scores_points['Norm']
    del scores_gold, scores_silver, scores_bronze, scores_points

    return scores
    # return scores.sort_values(by=['Team'], ascending=True).reset_index(drop=True)

