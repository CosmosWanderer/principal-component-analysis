#!/usr/bin/env python3

# Usage: python pca_analysis.py data/metrics.csv

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df = pd.read_csv(sys.argv[1])
print(f"\nRows {len(df)} \ncols: {', '.join(df.columns)}")


X = StandardScaler().fit_transform(df)

pca = PCA()
pca.fit(X)

print("\nExplained variance:")
cumsum = np.cumsum(pca.explained_variance_ratio_)
for i in range(min(5, len(pca.explained_variance_ratio_))):
    print(f"  PC{i+1}: {pca.explained_variance_ratio_[i]:.3f} (sum: {cumsum[i]:.3f})")

print("\nFirst 3 components")
loadings = pd.DataFrame(
    np.abs(pca.components_.T[:, :3]),
    index=df.columns,
    columns=['PC1', 'PC2', 'PC3']
)
print(loadings.round(3))

print("\nBiggest correlations (>0.9) between metrics:")
corr = df.corr()
high_corr = []
for i in range(len(corr.columns)):
    for j in range(i+1, len(corr.columns)):
        if abs(corr.iloc[i, j]) > 0.9:
            high_corr.append((corr.columns[i], corr.columns[j], corr.iloc[i, j]))
            print(f"  {corr.columns[i]} <-> {corr.columns[j]}: {corr.iloc[i, j]:.3f}")


if high_corr:
    print("\nCorrelation groups:")
    groups = []
    used = set()
    for m1, m2, _ in high_corr:
        if m1 not in used and m2 not in used:
            groups.append([m1, m2])
            used.add(m1)
            used.add(m2)
        elif m1 in used:
            for g in groups:
                if m1 in g and m2 not in g:
                    g.append(m2)
                    used.add(m2)
    
    for i, g in enumerate(groups, 1):
        print(f"  Group {i}: {', '.join(g)}")
        best = min(g, key=lambda x: abs(corr[x]).sum())
        print(f"    - can be replaced with: {best}")

# Visual
fig, axes = plt.subplots(1, 2, figsize=(16, 7))  # Увеличил ширину для чисел

# Metrics load on components heatmap 
im1 = axes[0].imshow(loadings.T, cmap='Blues', aspect='auto')
axes[0].set_yticks(range(3))
axes[0].set_yticklabels(['PC1', 'PC2', 'PC3'])
axes[0].set_xticks(range(len(df.columns)))
axes[0].set_xticklabels(df.columns, rotation=45, ha='right')
axes[0].set_title('Metrics load on components')
plt.colorbar(im1, ax=axes[0])

for i in range(3):
    for j in range(len(df.columns)):
        value = loadings.iloc[j, i]
        text_color = 'white' if value > 0.5 else 'black'
        axes[0].text(j, i, f'{value:.2f}', 
                    ha='center', va='center', 
                    color=text_color, fontsize=8)

# Correlation matrix
im2 = axes[1].imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
axes[1].set_xticks(range(len(df.columns)))
axes[1].set_yticks(range(len(df.columns)))
axes[1].set_xticklabels(df.columns, rotation=45, ha='right')
axes[1].set_yticklabels(df.columns)
axes[1].set_title('Correlation matrix')

for i in range(len(corr.columns)):
    for j in range(len(corr.columns)):
        value = corr.iloc[i, j]
        text_color = 'white' if abs(value) > 0.5 else 'black'
        axes[1].text(j, i, f'{value:.2f}', 
                    ha='center', va='center', 
                    color=text_color, fontsize=7)

plt.colorbar(im2, ax=axes[1])

plt.tight_layout()
plt.show()

# Res
print("Results")
print(f"First 3 components show {cumsum[2]:.1%} of all variations")
print(f"  - PC1: {loadings['PC1'].idxmax()} (load {loadings['PC1'].max():.3f})")
print(f"  - PC2: {loadings['PC2'].idxmax()} (load {loadings['PC2'].max():.3f})")
print(f"  - PC3: {loadings['PC3'].idxmax()} (load {loadings['PC3'].max():.3f})")