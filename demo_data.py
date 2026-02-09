import polars as pl
import numpy as np
import uuid

rng = np.random.default_rng(42)
n = 100
waves = [2023, 2024, 2025]

targets = {
    "age_bracket": {"21-34": 0.26, "35-54": 0.34, "55+": 0.40},
    "gender": {"Male": 0.50, "Female": 0.50},
    "region": {"Northeast": 0.20, "Midwest": 0.20, "South": 0.40, "West": 0.20},
}

dfs = []

for wave in waves:
    age_brackets = rng.choice(["21-34", "35-54", "55+"], size=n, p=[0.3, 0.4, 0.3])

    ages = np.where(
        age_brackets == "21-34", rng.integers(21, 35, size=n),
        np.where(age_brackets == "35-54", rng.integers(35, 55, size=n),
                 rng.integers(55, 76, size=n))
    )

    wave_df = pl.DataFrame({
        "uuid": [str(uuid.uuid4()) for _ in range(n)],
        "wave": [wave] * n,
        "age": ages,
        "age_bracket": age_brackets,
        "gender": rng.choice(["Male", "Female"], size=n, p=[0.6, 0.4]),
        "region": rng.choice(["Northeast", "Midwest", "South", "West"], size=n, p=[0.18, 0.21, 0.38, 0.23]),
        "income": rng.choice(["Under $30K", "$30K-$50K", "$50K-$75K", "$75K-$100K", "$100K+"], size=n, p=[0.15, 0.25, 0.25, 0.20, 0.15]),
    })

    # Rim weighting per wave
    weights = np.ones(n)
    for _ in range(50):
        for var, target_dist in targets.items():
            col = wave_df[var].to_numpy()
            for category, target_prop in target_dist.items():
                mask = col == category
                current_weighted = weights[mask].sum() / weights.sum()
                if current_weighted > 0:
                    weights[mask] *= target_prop / current_weighted

    weights = weights / weights.mean()
    wave_df = wave_df.with_columns(pl.Series("weight", np.round(weights, 4)))
    dfs.append(wave_df)

df = pl.concat(dfs)
df.write_parquet("survey_data.parquet")

print(df)
print(f"\nShape: {df.shape}")
print(f"\nWave counts:\n{df['wave'].value_counts().sort('wave')}")