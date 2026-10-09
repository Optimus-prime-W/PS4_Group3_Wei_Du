# PS4_Group3_Wei_Du
API Homework — Harry Potter Spell Analysis

This project uses the PotterDB API to retrieve information about spells from the Harry Potter universe and analyze their functional categories using Python.

Contributor: Wei Du

Data Source

API: PotterDB

Endpoint: https://api.potterdb.com/v1/spells

Retrieved attributes: Spell name, category, and effect

Project Description

The Python script retrieves spell data from the PotterDB API, including multiple pages of results. The retrieved information is processed using Pandas.

Spells are then classified into six functional groups based on their original categories and effect descriptions:

Offensive: Spells used for attacking or causing harm.

Defensive: Spells used for protection or countering attacks.

Healing: Spells used for healing or recovery.

Utility: Spells used for general purposes and everyday tasks.

Transfiguration: Spells that transform objects or living beings.

Other / Unknown: Spells that cannot be classified using the defined rules.

The classification is rule-based and is not an official PotterDB classification.

Data Visualization

The script generates a horizontal bar chart showing the number and percentage of spells in each functional group.