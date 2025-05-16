# ======================
# A/B Testing for Bank Marketing Campaigns
# ======================
# Author: Laxman Yadav Musti
# Date: 05-15-2025
# Tools: Python, Pandas, SciPy, Matplotlib, Seaborn
# Dataset: UCI Bank Marketing Dataset
# ======================

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.proportion import proportions_ztest

# ===========================================
# 1. Data Loading and Initial Exploration
# ===========================================

# Load dataset
df = pd.read_csv('bank-full.csv', sep=';')

print("Initial Data Overview:")
print(f"Shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

# ===========================================
# 2. Data Cleaning and Preprocessing
# ===========================================

print("\n=== Data Cleaning ===")

# Convert target variable to binary
df['converted'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)

# Filter for first-time contacts (campaign = 1)
df = df[df['campaign'] == 1]

# Create simulated A/B groups (50/50 split)
np.random.seed(42)  # For reproducibility
df['group'] = np.random.choice(['A', 'B'], size=len(df), p=[0.5, 0.5])

# Check group distribution
print("\nGroup Distribution:")
print(df['group'].value_counts())

# ===========================================
# 3. Exploratory Data Analysis (EDA)
# ===========================================

print("\n=== Exploratory Data Analysis ===")

# Overall conversion rate
overall_conversion = df['converted'].mean()
print(f"\nOverall Conversion Rate: {overall_conversion:.2%}")

# Conversion by group
group_stats = df.groupby('group')['converted'].agg(['mean', 'count'])
group_stats.columns = ['conversion_rate', 'sample_size']
print("\nConversion by Group:")
print(group_stats)

# Demographic analysis
print("\nConversion by Age:")
print(df.groupby(pd.cut(df['age'], bins=5))['converted'].mean())

# Visualization 1: Conversion Rates
plt.figure(figsize=(10, 6))
sns.barplot(x='group', y='converted', data=df, ci=None)
plt.title('Conversion Rates by Group')
plt.ylabel('Conversion Rate')
plt.xlabel('Test Group')
plt.ylim(0, 0.2)
plt.savefig('conversion_rates.png')
plt.close()

# Visualization 2: Age Distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='age', hue='group', bins=20, kde=True, alpha=0.6)
plt.title('Age Distribution by Group')
plt.savefig('age_distribution.png')
plt.close()

# ===========================================
# 4. Statistical Testing
# ===========================================

print("\n=== Statistical Testing ===")

# Prepare data for testing
group_a = df[df['group'] == 'A']['converted']
group_b = df[df['group'] == 'B']['converted']

# Chi-square test
contingency_table = pd.crosstab(df['group'], df['converted'])
chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)

# Z-test for proportions
count = [group_b.sum(), group_a.sum()]
nobs = [len(group_b), len(group_a)]
z_stat, p_value_z = proportions_ztest(count, nobs, alternative='larger')

print(f"\nChi-square Test Results:")
print(f"Chi2: {chi2:.4f}, p-value: {p_value:.4f}")

print(f"\nZ-test Results:")
print(f"Z-statistic: {z_stat:.4f}, p-value: {p_value_z:.4f}")

# ===========================================
# 5. Business Impact Analysis
# ===========================================

print("\n=== Business Impact Analysis ===")

# Calculate uplift
conv_a = group_a.mean()
conv_b = group_b.mean()
uplift = (conv_b - conv_a) / conv_a

# Calculate potential financial impact
avg_customer_value = 100  # Assuming each conversion is worth $100
additional_conversions = (conv_b - conv_a) * len(df)
additional_revenue = additional_conversions * avg_customer_value

print(f"\nConversion Rate - Group A: {conv_a:.2%}")
print(f"Conversion Rate - Group B: {conv_b:.2%}")
print(f"Uplift: {uplift:.2%}")
print(f"\nAdditional Conversions (if scaled to 10,000 customers): {additional_conversions * 10:.0f}")
print(f"Potential Additional Revenue: ${additional_revenue * 10:,.0f}")

# ===========================================
# 6. Automated Reporting
# ===========================================

from datetime import datetime

# Create report
report = f"""
A/B TESTING REPORT - BANK MARKETING CAMPAIGN
Date: {datetime.now().strftime('%Y-%m-%d')}

1. TEST OVERVIEW
- Test Groups: A (Control) vs B (Treatment)
- Total Samples: {len(df):,}
- Group A Samples: {len(group_a):,}
- Group B Samples: {len(group_b):,}

2. KEY RESULTS
- Conversion Rate (A): {conv_a:.2%}
- Conversion Rate (B): {conv_b:.2%}
- Uplift: {uplift:.2%}
- Statistical Significance (p-value): {p_value_z:.4f}

3. BUSINESS IMPACT
- Additional Conversions per 10k: {additional_conversions * 10:.0f}
- Potential Revenue Gain: ${additional_revenue * 10:,.0f}

4. RECOMMENDATION
{"Recommend implementing Strategy B (significant improvement)" if p_value_z < 0.05 else "No significant difference found"}
"""

# Save report
with open('ab_test_report.txt', 'w') as f:
    f.write(report)

print("\n=== Report Generated ===")
print(report)

# ===========================================
# 7. Advanced Analysis (Optional)
# ===========================================

# Bayesian A/B Testing (Optional)
from bayesian_testing.experiments import BinaryDataTest

# Initialize test
bt = BinaryDataTest()

# Add samples
bt.add_variant_data("A", group_a.tolist())
bt.add_variant_data("B", group_b.tolist())

# Evaluate probabilities
evaluation_results = bt.evaluate(10000)

for result in evaluation_results:
    if result['variant'] == 'B':
        prob_b_better = result['prob_being_best']
        break

print(f"\nBayesian Probability that B is better: {prob_b_better:.2%}")

# ===========================================
# 8. Export Clean Data for Visualization Tools
# ===========================================

# Prepare data for Tableau/Power BI
df.to_csv('ab_test_results.csv', index=False)

print("\n=== Analysis Complete ===")