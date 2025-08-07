# ensemble.py (you already have this)
import numpy as np
from collections import Counter

class MajorityVotingEnsemble:
    def __init__(self, models, weights=None, tie_breaker_order=None, n_classes=None):
        self.models = models
        self.weights = weights if weights is not None else [1.0] * len(models)
        self.tie_breaker_order = (
            tie_breaker_order if tie_breaker_order is not None else list(range(len(models)))
        )
        self.n_classes = n_classes  # may be None

    def _infer_n_classes(self, X):
        n_classes = getattr(self, "n_classes", None)
        if n_classes is not None:
            return n_classes
        candidates = []
        for m in self.models:
            if hasattr(m, "classes_"):
                candidates.append(len(m.classes_))
        if candidates:
            n_classes = max(candidates)
        else:
            preds = [m.predict(X) for m in self.models]
            max_label = max(int(p.max()) for p in preds)
            n_classes = max_label + 1
        self.n_classes = n_classes
        return n_classes

    def predict_proba(self, X):
        n_classes = self._infer_n_classes(X)
        proba_sum = np.zeros((X.shape[0], n_classes), dtype=float)
        weight_sum = 0.0

        for model, w in zip(self.models, self.weights):
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X)
                if hasattr(model, "classes_") and proba.shape[1] != n_classes:
                    full = np.zeros((X.shape[0], n_classes), dtype=float)
                    for idx, cls in enumerate(model.classes_):
                        full[:, int(cls)] = proba[:, idx]
                    proba = full
            else:
                preds = model.predict(X)
                proba = np.zeros((X.shape[0], n_classes), dtype=float)
                for i, p in enumerate(preds):
                    proba[i, int(p)] = 1.0
            proba_sum += proba * w
            weight_sum += w

        if weight_sum == 0:
            raise ValueError("Sum of weights is zero.")
        return proba_sum / weight_sum

    def predict(self, X):
        avg_proba = self.predict_proba(X)
        return np.argmax(avg_proba, axis=1)

    def majority_vote(self, X):
        preds = [m.predict(X) for m in self.models]
        preds_array = np.vstack(preds).T
        ensemble = []
        for votes in preds_array:
            cnt = Counter(votes)
            top_vote, top_count = cnt.most_common(1)[0]
            if top_count >= 2:
                ensemble.append(top_vote)
            else:
                for idx in self.tie_breaker_order:
                    ensemble.append(votes[idx])
                    break
        return np.array(ensemble)
