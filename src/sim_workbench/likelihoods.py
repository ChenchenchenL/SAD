"""Likelihood repairs for current runs using archived diagnosis engines.

Historical engines and saved observations remain reproducible as recorded.
Apply this adapter immediately after constructing a model in a repaired run.
"""
from __future__ import annotations

import math
from types import MethodType
from typing import TypeVar

Model = TypeVar("Model")


def normalize_single_answer_items(model: Model) -> Model:
    """Give a singleton answer probability one under every hypothesis.

    All other likelihood rows remain bit-for-bit unchanged. The companion
    slip log-likelihood uses the same degenerate distribution, so accumulated
    likelihood ratios agree with the matrix used by Bayesian updates.
    """
    if getattr(model, "_single_answer_normalized", False):
        return model
    singleton = {i for i, answers in enumerate(model.answer_index) if len(answers) == 1}
    for i in singleton:
        model.L[i][:] = 0.0
        model.L[i][:, 0] = 1.0
        model.L_stack[i] = model.L[i]

    if singleton:
        original_slip = model.slip_loglik

        def slip_loglik(self, item_idx, outcome, eps=None):
            if item_idx in singleton:
                return 0.0 if outcome in self.answer_index[item_idx] else math.log(1e-12)
            return original_slip(item_idx, outcome, eps)

        model.slip_loglik = MethodType(slip_loglik, model)
    model._single_answer_normalized = True
    return model
