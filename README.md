# The-Demographics-of-Faerun
### A fictional dataset for the dungeons and dragons world of Faerun
![git title image](https://github.com/jbloewencolon/The-Demographics-of-Faerun/blob/main/Images/git%20title.png)
By Jordan Loewen-Colón 2023

### Objective
This project aims to craft a captivating, dynamic dataset derived from the enthralling world of Faerun in Dungeons and Dragons (D&D). The primary goal is to offer an engaging, imaginative resource for budding data scientists to hone their skills, diverging from conventional, mundane datasets. The dataset serves as an innovative educational tool and is envisioned as a dynamic, living record of Faerun’s economy and demographics, with potential for continuous updates and enhancements by the global D&D Adventurers League community.

### Insights
This imaginative dataset reveals intriguing insights into the fictional world’s demographics, economics, and politics, providing a comprehensive view of various regions and settlements within Faerun. It offers a glimpse into the diverse species, their average ages, economic activities, and even factors like crime rates and magical climates, painting a vivid picture of life in this enchanting universe.

### Data Understanding
Creating this dataset required a blend of familiarity with the D&D universe and fundamental data analysis skills. The dataset encompasses over 27 columns (including settlements, populations, economies, and mythical elements) and 650 entries with a mix of validated data from the handbooks and randomized data. The result is a dataset that allows users to navigate through a mix of numerical, categorical, and text data, all woven with the rich tapestry of D&D lore.


1. **settlement**: Name of the settlement.
2. **region_kingdom**: The kingdom or region to which the settlement belongs.
3. **capital**: Indicates which settlement is the capital of its region.
4. **settlement_population**: Population count of the settlement.
5. **settlement_economy**: Economic wealth of the settlement.
6. **rumored_treasure_value**: Estimated value of rumored treasures in the settlement.
7. **demographic_breakdown**: Breakdown of settlement population by demographics.
8. **average_age**: Average age of the settlement's residents.
9. **most_likely_cause_of_death**: The most likely cause of death in the settlement.
10. **government_type**: Type of government governing the settlement.
11. **class_density**: Density or distribution of social classes in the settlement.
12. **tax_rate**: Tax rate imposed in the settlement.
13. **exports**: Goods or items exported by the settlement.
14. **imports**: Goods or items imported by the settlement.
15. **ruler**: Name or title of the ruler governing the settlement.
16. **military**: Information about the settlement's military.
17. **magic_academy**: Presence or absence of a magic academy in the settlement.
18. **languages**: Languages spoken in the settlement.
19. **religions**: Religions practiced in the settlement.
20. **region_population**: Population count of the region to which the settlement belongs.
21. **region_economy**: Economic wealth of the region or kingdom.
22. **area**: Land area of the settlement (if available).
23. **average_temperature**: Average temperature in the settlement's region.
24. **annual_rainfall**: Annual rainfall in the settlement's region.
25. **magical_climate**:The activity or force of the "Thread" in the settlement and nearby area.
26. **dragon_sightings**: Number of dragon sightings in the settlement.
27. **sources**: Sources or references for the data (if available).

### Data Preparation
The preparation process involved meticulous collection and compilation of data from D&D manuals and online sources. The list of sources can be found in the [Source](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/tree/main/Sources) folder. Real-world economic principles were ingeniously integrated with the fictional data to craft a dataset that is not only fantastical but also grounded in reality. Data cleansing, transformation, and integration were performed to ensure consistency, accuracy, and usability. Given the scarcity of accurate population and economic numbers, elements of the dataset needed to be randomized. To get a general sense of the economy, we relied on the lifestyle costs from the players' handbook and then spoke to economists to get a rough estimate on lifestyle ranges depending on the size of the city.

![economy_calculation](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/Images/economy.JPG)

We then created a function that would randomize the class_density of lifestyles within a small range and then multiply by 365 and the lifestyle cost per lifestyle type. The result was a varied but realistic gold economy per city depending on size. 

### Data Engineering
Data engineering efforts were concentrated on generating novel features that would resonate with the D&D narrative while providing valuable learning resources for data science enthusiasts. Features like rumored treasure value, magical climate, and dragon sightings were ingeniously crafted, with each calculation based on a concoction of existing features and imaginative assumptions. We created two different datasets, one with hidden features that would affect the visible dataset made available to the public. This would allow models to avoid overfitting the data. On the hidden dataset, we included features measuring things like:

![hidden_economy](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/Images/hidden%20data.JPG)

### Data Modeling
Data modeling in this context is not about predicting outcomes but rather about constructing a believable, internally consistent representation of the D&D world. The modeling process involved creating relationships between different entities, making assumptions where necessary, and meticulously tweaking parameters to align the dataset with the rich lore of Faerun.

![heat_matrix](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/Images/heat%20matrix.png)

![class_density](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/Images/class%20aristocrat.png)

![poisson](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/Images/Poisson.JPG)

### Data Evaluation
The dataset’s evaluation isn't centered on predictive accuracy but rather on its ability to engage users and accurately reflect the D&D universe’s complexities. It’s imperative to assess whether the dataset offers valuable insights, encourages exploration, and provides a faithful, engaging representation of the captivating world of Faerun for both new and seasoned adventurers.

![economy_factors](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/Images/economy.png)

### Conclusions
This project successfully amalgamates the enchanting lore of Dungeons and Dragons with real-world economics, offering an engaging, educational tool for aspiring data scientists. With potential for further enhancement and community-driven dynamic updates, this dataset stands as a unique, imaginative resource poised to inspire and educate, while contributing to the ever-evolving narrative of the D&D universe.

We suggest that Wizards of the Coast should consider building on this for:

**Engagement & Education:** This dynamic dataset from Faerun enhances gameplay while serving as an engaging tool for aspiring data scientists.

**Community Collaboration:** Fans contribute to the evolving lore, fostering a deeper connection with the D&D universe.

**Innovation Leader:** Adopting this initiative positions Wizards of the Coast as a pioneer at the intersection of gaming and education, opening avenues for partnerships and innovation.

# Next Steps

I envision further datasets bringing to life the universes of Star Wars, Star Trek, Dune, and Discworld, each providing unique opportunities for engagement, education, and community collaboration.

# Questions?
Further questions? Contact Jordan Loewen-Colón @ jbloewen@syr.edu

**Notes:** title image created using Midjourney

## Repository Structure


├── [data](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/Demographics_of_Faerun_Dataset.xlsx) : data used for modeling
├── [images](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/tree/main/Images) : images used in README
├── [Sandbox](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/tree/main/Sandbox) : previous files from earlier drafts of project
├── [README.md](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/README.md) : project information and repository structure

