# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import scipy as sp
import scipy.stats
import six

from utils import *
from stepwisefit import *


def calc_uncorr_gene_score(input_gene, input_snp, pruned_snps, hotspots, boundr_upstr, boundr_downstr):
    n_genes = len(input_gene)
    uncorr_score = np.zeros(n_genes)
    n_snps_per_gene = np.zeros(n_genes, dtype="i")
    n_indep_snps_per_gene = np.zeros(n_genes, dtype="i")
    n_hotspots_per_gene = np.zeros(n_genes, dtype="i")
    n_genes_score_nan = 0

    for gene in six.moves.range(n_genes):
        # if reverse strand
        if input_gene[gene, 3] == 0:
            boundr_upstr, boundr_downstr = boundr_downstr, boundr_upstr

        # find local snps given a gene
        cond_snps_near_gene = logical_and(np.equal(input_snp[:, 0], input_gene[gene, 0]),
                                          np.greater_equal(input_snp[:, 1], (input_gene[gene, 1] - boundr_upstr)),
                                          np.less_equal(input_snp[:, 1], (input_gene[gene, 2] + boundr_downstr)))
        # if no snps found
        if not np.any(cond_snps_near_gene):
            n_genes_score_nan += 1
            uncorr_score[gene] = np.nan
            continue

        n_snps_zscore_finite = np.sum(np.isfinite(input_snp[cond_snps_near_gene][:, 3]))
        # if no snps with finite zcore
        if n_snps_zscore_finite == 0:
            n_genes_score_nan += 1
            uncorr_score[gene] = np.nan
            continue

        n_snps_per_gene[gene] = n_snps_zscore_finite

        # use p-value to find most significant SNP
        idx_min_pval = np.nanargmin(input_snp[cond_snps_near_gene][:, 3])

        uncorr_score[gene] = input_snp[idx_min_pval, 2]

        # count number of independent SNPs per gene
        n_indep_snps_per_gene[gene] = np.sum(logical_and(np.equal(pruned_snps[:, 0], input_gene[gene, 0]),
                                                         np.greater_equal(pruned_snps[:, 1], (input_gene[gene, 1] - boundr_upstr)),
                                                         np.less_equal(pruned_snps[:, 1], (input_gene[gene, 2] + boundr_downstr))))

        # count number of hotspots per gene
        n_hotspots_per_gene[gene] = np.sum(np.logical_and(np.equal(hotspots[:, 0], input_gene[gene, 0]),
                                                          np.greater(np.fmin(hotspots[:, 2], (input_gene[gene, 2] + boundr_downstr))
                                                                     - np.fmax(hotspots[:, 1], (input_gene[gene, 1] - boundr_upstr)), 0)))

    return (np.fabs(uncorr_score), n_snps_per_gene, n_genes_score_nan, n_indep_snps_per_gene, n_hotspots_per_gene)


def calc_corr_gene_score(confounders, uncorr_score):
    n_genes, n_confounders = confounders.shape
    cutoff = 0.05
    cond_score_finite = np.isfinite(uncorr_score)
    beta, se, pval, inmodel, stats, nextstep, history = stepwisefit(confounders[cond_score_finite], uncorr_score[cond_score_finite])
    residuals = uncorr_score - stats.intercept
    for j in six.moves.range(n_confounders):
        if pval[j] <= cutoff:
            residuals = residuals - beta[j] * confounders[:, j]

    cond_residuals_finite = np.isfinite(residuals)
    corr_score = 1 - sp.stats.norm.cdf(residuals,
                                       np.mean(residuals[cond_residuals_finite]),
                                       np.std(residuals[cond_residuals_finite]))
    return (corr_score, residuals)
