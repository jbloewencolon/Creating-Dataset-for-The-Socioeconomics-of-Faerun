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

### Data Preparation
The preparation process involved meticulous collection and compilation of data from D&D manuals and online sources. The list of sources can be found in the [Source](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/tree/main/Sources) folder. Real-world economic principles were ingeniously integrated with the fictional data to craft a dataset that is not only fantastical but also grounded in reality. Data cleansing, transformation, and integration were performed to ensure consistency, accuracy, and usability. Given the scarcity of accurate population and economic numbers, elements of the dataset needed to be randomized. To get a general sense of the economy, we relied on the lifestyle costs from the players handbook and then spoke to economists to get a rough estimate on lifestyle ranges depending on the size of the city.

![economy_calculation](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/Images/economy.JPG)

We then created a function that would randomize the class_density of lifestyles within a small range and then mulitiply by 365 and the lifestyle cost per lifestyle type. The result was a variad but realistic gold-economy per city depending on size. 

### Data Engineering
Data engineering efforts were concentrated on generating novel features that would resonate with the D&D narrative while providing valuable learning resources for data science enthusiasts. Features like rumored treasure value, magical climate, and dragon sightings were ingeniously crafted, with each calculation based on a concoction of existing features and imaginative assumptions. We created two different datasets, one with hidden features that would effect the visible dataset made available to the public. This would allow models to avoid overfitting the data. On the hidden dataset, we included features measuring things like:

![hidden_economy](https://github.com/jbloewencolon/Creating-Dataset-for-The-Demographics-of-Faerun/blob/main/Images/hidden%20data.JPG)

### Data Modeling
Data modeling in this context is not about predicting outcomes but rather about constructing a believable, internally consistent representation of the D&D world. The modeling process involved creating relationships between different entities, making assumptions where necessary, and meticulously tweaking parameters to align the dataset with the rich lore of Faerun.

### Data Evaluation
The dataset’s evaluation isn't centered on predictive accuracy but rather its ability to engage users and accurately reflect the D&D universe’s complexities. It’s imperative to assess whether the dataset offers valuable insights, encourages exploration, and provides a faithful, engaging representation of the captivating world of Faerun for both new and seasoned adventurers.

### Conclusions
This project successfully amalgamates the enchanting lore of Dungeons and Dragons with real-world economics, offering an engaging, educational tool for aspiring data scientists. With potential for further enhancement and community-driven dynamic updates, this dataset stands as a unique, imaginative resource poised to inspire and educate, while contributing to the ever-evolving narrative of the D&D universe.

Wizard;s of the Coast should consider building on this for:
**Engagement & Education:** Our dynamic dataset from Faerun enhances gameplay while serving as an engaging tool for aspiring data scientists.
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

