import numpy as np
from scipy.stats import itemfreq
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC as SVM


def set_trace():
    from IPython.core.debugger import Pdb
    import sys
    Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back)


def impute(data, imputer, imp_method, params_dict):
    imp_data = None

    if imp_method == 'RandomReplace':
        imp_data = imputer.replace(data, params_dict['miss_data_cond'])
    elif imp_method == 'Summary':
        imp_data = imputer.summarize(data,
                                     params_dict['summary_func'],
                                     params_dict['miss_data_cond'])
    elif imp_method == 'RandomForest':
        clf = RandomForestClassifier(
            n_estimators=100, criterion='gini', max_depth=None,
            min_samples_split=2, min_samples_leaf=1,
            min_weight_fraction_leaf=0.0, max_features='auto',
            max_leaf_nodes=None, bootstrap=True, oob_score=False, n_jobs=1,
            random_state=None, verbose=0, warm_start=False, class_weight=None)
        imp_data = imputer.predict(data,
                                   params_dict['cat_cols'],
                                   params_dict['miss_data_cond'],
                                   clf)

    elif imp_method == 'SVM':
        clf = SVM(
            C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0,
            shrinking=True, probability=False, tol=0.001, cache_size=200,
            class_weight=None, verbose=False, max_iter=-1,
            decision_function_shape=None, random_state=None)
        imp_data = imputer.predict(data,
                                   params_dict['cat_cols'],
                                   params_dict['miss_data_cond'],
                                   clf)
    elif imp_method == 'LogisticRegression':
        clf = LogisticRegression(
            penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True,
            intercept_scaling=1, class_weight=None, random_state=None,
            solver='liblinear', max_iter=100, multi_class='ovr', verbose=0,
            warm_start=False, n_jobs=1)
        imp_data = imputer.predict(data,
                                   params_dict['cat_cols'],
                                   params_dict['miss_data_cond'],
                                   clf)
    elif imp_method == 'PCA':
        imp_data = imputer.factor_analysis(data,
                                           params_dict['cat_cols'],
                                           params_dict['miss_data_cond'])
    elif imp_method == 'KNN':
        imp_data = imputer.knn(data,
                               params_dict['n_neighbors'],
                               params_dict['knn_summary_func'],
                               params_dict['miss_data_cond'],
                               params_dict['cat_cols'])
    return imp_data


def perturbate_data(x, cols, ratio, monotone, missing_data_symbol,
                    in_place=False):
    """Perturbs data by substituting existing values with missing data symbol
    such that each feature has a minimum missing data ratio


    Parameters
    ----------
    x : np.ndarray
        Matrix with categorical data, where rows are observations and
        columns are features
    cols : int tuple
        index of columns that are categorical
    ratio : float [0, 1]
        Ratio of observations in data to have missing data
    missing_data_symbol : str
        String that represents missing data in data
    method: float [0, 1]
        Non-monotone: Any observation and feature can present a missing
            value. Restrict the number of missing values in a observations
            to not more than half of the features.
        Monotone: set to missing all the values of 30% of randomly selected
            features with categorical variables
    """

    def zero():
        return 0

    if in_place:
        data = x
    else:
        data = np.copy(x)

    n_perturbations = int(len(x) * ratio)
    if monotone:
        missing_mask = np.random.choice((0, 1), data[:, cols].shape, True,
                                        (1-ratio, ratio)).astype(bool)

        miss_dict = defaultdict(list)
        for i in xrange(len(cols)):
            rows = np.where(missing_mask[:, i])[0]
            data[rows, cols[i]] = missing_data_symbol
            miss_dict[cols[i]] = rows
        """
        cols = np.random.choice(cols, int(len(cols) * monotone))
        rows = np.random.randint(0, len(data), n_perturbations)
        cols = np.random.choice(cols, n_perturbations)

        data[rows, cols] = missing_data_symbol
        miss_dict = defaultdict(list)
        for (row, col) in np.dstack((rows, cols))[0]:
            miss_dict[col].append(row)
        """
    else:
        # slow
        row_col_miss = defaultdict(zero)
        miss_dict = defaultdict(list)
        i = 0
        while i < n_perturbations:
            row = np.random.randint(0, len(data))
            col = np.random.choice(cols)

            # proceed if less than half the features are missing
            if row_col_miss[row] < len(cols) * 0.5 \
                    and data[row, col] != missing_data_symbol:
                data[row, col] = missing_data_symbol
                row_col_miss[row] += 1
                miss_dict[col].append(row)
                i += 1

    return data, miss_dict


def compute_histogram(data, labels):
    histogram = dict(itemfreq(data))
    for label in labels:
        if label not in histogram:
            histogram[label] = .0
    return histogram


def compute_error_rate(y, y_hat, feat_imp_ids):
    error_rate = {}
    for col, ids in feat_imp_ids.items():
        errors = sum(y[ids, col] != y_hat[ids, col])
        error_rate[col] = errors / float(len(ids))

    return error_rate
