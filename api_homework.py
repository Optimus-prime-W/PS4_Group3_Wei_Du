#%% 1. Import libraries

import requests
import pandas as pd
import matplotlib.pyplot as plt
import re
import matplotlib.ticker as ticker


#%% 2. API configuration

API_URL = "https://api.potterdb.com/v1/spells"

PARAMS = {
    "page[size]": 100
}

HEADERS = {
    "User-Agent": "Python API Assignment"
}

TIMEOUT_SECONDS = 15


#%% 3. Fetch all spells from API

def fetch_data(url, params=None):

    all_spells = []

    while url:

        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT_SECONDS
        )

        response.raise_for_status()

        data = response.json()

        all_spells.extend(data["data"])

        # Next page
        url = data.get("links", {}).get("next")

        if url and url.startswith("/"):
            url = requests.compat.urljoin(API_URL, url)

        params = None

    return all_spells


data = fetch_data(API_URL, PARAMS)

print("Total spells retrieved:", len(data))
#%% 4. Extract useful information

records = []

for item in data:

    attributes = item["attributes"]

    record = {
        "name": attributes.get("name"),
        "category": attributes.get("category"),
        "effect": attributes.get("effect")
    }

    records.append(record)

df = pd.DataFrame(records)

print(df.head())
print("Total records:", len(df))

#%% 5. Reclassify spells using category and effect


def classify_spell(row):

    name = str(row["name"] or "").lower()
    category = str(row["category"] or "").lower()
    effect = str(row["effect"] or "").lower()

    # Normalize text
    text = f"{name} {category} {effect}"
    text = re.sub(r"\s+", " ", text)

    def has_keywords(keywords):
        return any(word in text for word in keywords)

    # 1. Healing
    if has_keywords([
        "healing",
        "heal wounds",
        "heal injuries",
        "cure",
        "restore health",
        "mend bones",
        "close wounds"
    ]):
        return "Healing"

    # 2. Defensive
    if has_keywords([
        "shield",
        "protect",
        "protection",
        "defend",
        "deflect",
        "counter-curse",
        "counter-jinx",
        "counter-spell",
        "repel attacks",
        "block spells",
        "barrier"
    ]):
        return "Defensive"

    # 3. Offensive
    if has_keywords([
        "attack",
        "damage",
        "injure",
        "kill",
        "stun",
        "disarm",
        "torture",
        "explode",
        "burn",
        "paralyse",
        "paralyze",
        "knock back",
        "knock out",
        "curse",
        "hex",
        "jinx"
    ]):
        return "Offensive"

    # 4. Transfiguration
    if has_keywords([
        "transfiguration",
        "transform",
        "transfigure",
        "turn into",
        "change the form",
        "change the appearance"
    ]):
        return "Transfiguration"

    # 5. Utility
    if has_keywords([
        "charm",
        "summon",
        "levitate",
        "float",
        "move objects",
        "unlock",
        "light",
        "clean",
        "repair",
        "enlarge",
        "shrink",
        "transport",
        "reveal",
        "conceal",
        "open",
        "close"
    ]):
        return "Utility"

    return "Other / Unknown"


df["function_group"] = df.apply(
    classify_spell,
    axis=1
)

summary = (
    df["function_group"]
    .value_counts()
    .reset_index()
)

summary.columns = ["Function Group", "Count"]

print(summary.to_string(index=False))

#%% 6. Plot spell function distribution


# Sort categories by count
plot_df = summary.sort_values("Count", ascending=True).copy()

# Colors for each spell function
colors = {
    "Offensive": "#D95F59",
    "Defensive": "#4C78A8",
    "Healing": "#54A878",
    "Utility": "#E6A23C",
    "Transfiguration": "#9B79B8",
    "Other / Unknown": "#9CA3AF"
}

bar_colors = [
    colors.get(group, "#9CA3AF")
    for group in plot_df["Function Group"]
]

total = plot_df["Count"].sum()

# Figure
fig, ax = plt.subplots(figsize=(10, 5.8))

bars = ax.barh(
    plot_df["Function Group"],
    plot_df["Count"],
    color=bar_colors,
    height=0.65,
    edgecolor="none"
)

# Add counts and percentages
for bar, count in zip(bars, plot_df["Count"]):

    percentage = count / total * 100

    ax.text(
        bar.get_width() + total * 0.008,
        bar.get_y() + bar.get_height() / 2,
        f"{count}  ({percentage:.1f}%)",
        va="center",
        ha="left",
        fontsize=11,
        fontweight="medium"
    )

# Titles
ax.set_title(
    "Functional Distribution of Harry Potter Spells",
    fontsize=17,
    fontweight="bold",
    pad=20,
    loc="left"
)

ax.text(
    0, 1.02,
    f"PotterDB API  |  Total spells: {total}",
    transform=ax.transAxes,
    fontsize=10,
    color="#666666"
)

ax.set_xlabel(
    "Number of Spells",
    fontsize=12,
    labelpad=10
)

ax.set_ylabel("")

# Grid and axis styling
ax.set_axisbelow(True)
ax.xaxis.grid(
    True,
    linestyle="--",
    alpha=0.2
)

ax.xaxis.set_major_locator(
    ticker.MaxNLocator(integer=True)
)

ax.tick_params(
    axis="both",
    length=0,
    labelsize=11,
    pad=8
)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_xlim(
    0,
    max(plot_df["Count"].max() * 1.28, 1)
)

fig.patch.set_facecolor("white")
ax.set_facecolor("white")

plt.tight_layout()

plt.savefig(
    "spell_function_distribution.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.show()
# %%