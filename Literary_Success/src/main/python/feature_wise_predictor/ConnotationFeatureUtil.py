__author__ = 'santhosh'

from util import NovelMetaGenerator
import SyntaticTreeFeaturesUtil
from nltk.corpus.reader import Synset
from sklearn.linear_model import LogisticRegression
import math

def calculate_Entropy(dist):
    entropy_list = [-p*math.log(p) for p in dist if p != 0]
    if len(entropy_list) > 0:
        return sum(entropy_list)
    else:
        return 0

def extractFeatures(conn_files):
    feature_dict = dict()
    for genre_file_path, genre_file_name in conn_files:
        all_entropy = []
        f = open(genre_file_path)
        lines = f.readlines()
        f.close()
        assert len(lines) == 1
        line = lines[0]
        data = []
        line = 'data='+line
        exec(line)
        for line in data:
         for word, synset in line:
            if synset == None:
                continue
            entropy = calculate_Entropy([p for p, syn in synset])
            if entropy > 0:
                all_entropy.append(entropy)
        avg_entropy = 0.0
        if len(all_entropy) > 0:
            avg_entropy = sum(all_entropy)/len(all_entropy)
        key = genre_file_name.replace(NovelMetaGenerator.SYNSET_WSD_FILE_SUFFIX, '')
        feature_dict[key] = {'AVG_ENTROPY': avg_entropy}
    return feature_dict



def doClassification():
    conn_files_dict = NovelMetaGenerator.listGenreWiseFileNames(NovelMetaGenerator.CORE_NLP_BASE,\
                                                                NovelMetaGenerator.SYNSET_WSD_TAG_PATTERN)
    meta_dict = NovelMetaGenerator.loadInfoFromMetaFile()
    for genre in conn_files_dict:
        if genre != 'Adventure Stories':
            continue
        meta_dict_for_genre = meta_dict[genre]
        core_nlp_files = conn_files_dict[genre]
        feature_dict = extractFeatures(core_nlp_files)
        train_data, train_result, test_data, test_result =\
            SyntaticTreeFeaturesUtil.splitTrainAndTestData(meta_dict_for_genre, feature_dict)


