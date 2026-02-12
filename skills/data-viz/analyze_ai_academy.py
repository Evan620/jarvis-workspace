#!/usr/bin/env python3
"""
Create a detailed analysis report from AI Academy Readiness data
"""

import pandas as pd

# Load data
df = pd.read_csv('/home/evan/clawd/skills/data-viz/ai_academy_readiness.csv')

print("AI Academy Readiness Analysis\n")
print("=" * 80)
print(f"\nTotal cities analyzed: {len(df)}\n")

print("TOP 10 CITIES BY TOTAL SCORE:")
print("-" * 80)
top10 = df.nlargest(10, 'total_score')
for idx, row in top10.iterrows():
    print(f"{idx+1}. {row['location']:20s} - Score: {row['total_score']:5.1f} | {row['country']}")
    print(f"   → English: {row['english_proficiency_0_100']:3}/100 | Experts: {row['local_ai_experts_0_100']:3}/100 | Partnerships: {row['university_partnerships_0_100']:3}/100")
    print(f"   → Cloud: {row['cloud_provider_presence_0_100']:3}/100 | Affordability: {row['cost_of_living_affordability_0_100']:3}/100 | Policy: {row['government_ai_policy_support_0_100']:3}/100")
    print(f"   → Compute cost: ${row['compute_costs_student_usd_month']}/month")
    print()

print("\nKEY INSIGHTS:")
print("-" * 80)

print("\n1. ENGLISH PROFICIENCY LEADERBOARD:")
top_english = df.nlargest(5, 'english_proficiency_0_100')
for idx, row in top_english.iterrows():
    print(f"   {row['location']:20s} - {row['english_proficiency_0_100']}/100")

print("\n2. LOCAL AI EXPERTS LEADERBOARD:")
top_experts = df.nlargest(5, 'local_ai_experts_0_100')
for idx, row in top_experts.iterrows():
    print(f"   {row['location']:20s} - {row['local_ai_experts_0_100']}/100 (est. {row['local_ai_experts_0_100'] * 2}+ engineers)")

print("\n3. MOST AFFORDABLE (Lowest cost of living):")
most_affordable = df.nlargest(5, 'cost_of_living_affordability_0_100')
for idx, row in most_affordable.iterrows():
    print(f"   {row['location']:20s} - Affordability: {row['cost_of_living_affordability_0_100']}/100")

print("\n4. LOWEST COMPUTE COSTS:")
lowest_compute = df.nsmallest(5, 'compute_costs_student_usd_month')
for idx, row in lowest_compute.iterrows():
    print(f"   {row['location']:20s} - ${row['compute_costs_student_usd_month']}/month")

print("\n5. BEST GOVERNMENT AI POLICY SUPPORT:")
best_policy = df.nlargest(5, 'government_ai_policy_support_0_100')
for idx, row in best_policy.iterrows():
    print(f"   {row['location']:20s} - {row['government_ai_policy_support_0_100']}/100")

print("\nCRITICAL INSIGHTS:")
print("-" * 80)

print("\n❌ DEALBREAKERS (Where AI Academies Fail):")
dealbreakers = df[
    (df['english_proficiency_0_100'] < 70) |  # Can't access learning resources
    (df['local_ai_experts_0_100'] < 40) |  # Must import all instructors
    (df['compute_costs_student_usd_month'] > 150) |  # Too expensive for students
    (df['cost_of_living_affordability_0_100'] < 50)  # Students can't afford to study
]
print(f"\n   Cities with critical flaws ({len(dealbreakers)}):")
for idx, row in dealbreakers.iterrows():
    issues = []
    if row['english_proficiency_0_100'] < 70:
        issues.append("Low English proficiency")
    if row['local_ai_experts_0_100'] < 40:
        issues.append("No local experts (must import)")
    if row['compute_costs_student_usd_month'] > 150:
        issues.append("High compute costs")
    if row['cost_of_living_affordability_0_100'] < 50:
        issues.append("Unaffordable for students")
    print(f"   • {row['location']:20s} - {', '.join(issues)}")

print("\n✅ WINNERS (Where AI Academies Thrive):")
winners = df[
    (df['english_proficiency_0_100'] >= 90) &
    (df['local_ai_experts_0_100'] >= 80) &
    (df['cloud_provider_presence_0_100'] >= 70) &
    (df['cost_of_living_affordability_0_100'] >= 60)
]
print(f"\n   Cities passing all key metrics ({len(winners)}):")
for idx, row in winners.iterrows():
    print(f"   • {row['location']:20s} - Score: {row['total_score']:5.1f} | Strong English, Local Experts, Cloud Presence, Affordable")

print("\nRECOMMENDATIONS:")
print("-" * 80)

print("\n🎯 TIER 1: IMMEDIATE INVESTMENT (Ready Now)")
tier1 = df[df['total_score'] >= 90]
for idx, row in tier1.iterrows():
    print(f"\n   {row['location']} ({row['country']}) - Score: {row['total_score']}")
    print(f"   → Why: High English proficiency ({row['english_proficiency_0_100']})")
    print(f"   → Local experts: {row['local_ai_experts_0_100']}/100 (est. {row['local_ai_experts_0_100'] * 2}+ engineers)")
    print(f"   → University partnerships: {row['university_partnerships_0_100']}/100")
    print(f"   → Compute cost: ${row['compute_costs_student_usd_month']}/month (affordable)")
    print(f"   → Investment: Scale existing ecosystem, partner with local universities")

print("\n🎯 TIER 2: STRATEGIC DEVELOPMENT (2-5 years)")
tier2 = df[(df['total_score'] >= 75) & (df['total_score'] < 90)]
for idx, row in tier2.iterrows():
    print(f"\n   {row['location']} ({row['country']}) - Score: {row['total_score']}")
    print(f"   → Gap: {'English' if row['english_proficiency_0_100'] < 85 else 'Compute' if row['compute_costs_student_usd_month'] > 70 else 'Affordability'}")
    print(f"   → Investment: Fix specific bottleneck, then scale")

print("\n🎯 TIER 3: FUTURE POTENTIAL (5+ years)")
tier3 = df[(df['total_score'] >= 65) & (df['total_score'] < 75)]
for idx, row in tier3.iterrows():
    print(f"\n   {row['location']} ({row['country']}) - Score: {row['total_score']}")
    print(f"   → Status: Needs infrastructure or ecosystem development")
    print(f"   → Investment: Long-term play, not immediate")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE\n")
