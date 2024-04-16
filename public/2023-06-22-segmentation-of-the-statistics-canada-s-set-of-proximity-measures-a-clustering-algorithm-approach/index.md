# Segmentation of the Statistics Canada’s Set of Proximity Measures – A Clustering Algorithm Approach

**GitHub Repo** :- https://github.com/sahaavi/Segmentation-of-Proximity-Measures/tree/main

**Project Report** :- https://github.com/sahaavi/Segmentation-of-Proximity-Measures/blob/main/docs/final-report/PMS_finalreport.pdf

## Project Description

### Organization 
**Statistics Canada**
### Industry 
Data Exploration and Integration Lab – Centre for Special Business Project,
Statistics Canada
### Description 
The Data Exploration and Integration Lab (DEIL) at Statistics Canada is
creating a new set of granular measures that assess local access to a variety of
amenities such as libraries, parks, educational facilities, hospitals, and more. The
measures are generated out of a gravity model approach, where the cost of
transportation is weighted by the magnitude or importance of the entity they
travel to. The measures are calculated at the dissemination block level in
Canada. That is, around 500,000 unique geo-located units. The challenge for the
UBC Capstone students will be to implement a clustering algorithm
methodology for the segmentation of the measures.

Statistics Canada/DEIL literature about proximity measures:  

-Measuring proximity to services and amenities: An experimental set of indicators for neighborhoods and localities  
https://www150.statcan.gc.ca/n1/pub/18-001-x/18-001-x2020001-eng.pdf

-Measuring remoteness and accessibility - A set of indices for Canadian communities (2016)    
https://www150.statcan.gc.ca/n1/pub/18-001-x/18-001-x2017002-eng.pdf

-Index of Remoteness 2021: Update with 2021 census geographies and populations  
https://www150.statcan.gc.ca/n1/en/pub/17-26-0001/2020001/meta-doceng.pdf?st=JaM9ncSv

### Data Sources
-Proximity Measures Database  
https://www150.statcan.gc.ca/n1/pub/17-26-0002/172600022020001-eng.htm

-Index of Remoteness Database  
https://www150.statcan.gc.ca/n1/pub/17-26-0001/172600012020001-eng.htm




## Acknowledgements {#acknowledgements .unnumbered}

We want to express our gratitude to Jerome Blanchet, who served as our
industry advisor from Statistics Canada. We are also thankful to Dr.
Firas Moosvi and Dr. Irene Vrbik, who guided us as our capstone project
advisors. Additionally, we appreciate the support and feedback provided
by our Teaching Assistant, Jesse Ghashti. Their consistent guidance
helped us to successfully complete our Master's of Data Science Capstone
project within a tight two-month timeframe.

## Executive Summary

The Proximity Measure Database (PMD) developed by the Data Exploration
and Integration Lab (DEIL) at Statistics Canada serves to provide a
granular measure of proximity to services and amenities to inform
planning and policy questions (Alasia et al., 2021). The PMD contains
continuous measures for 10 amenities at a 'dissemination block' (DB)
level, the most granular area defined by Statistics Canada (2021). In an
urban area, a DB corresponds to a city block, whereas in rural areas
they are areas "bounded by roads or other natural features" (Alasia et
al., 2021). Our project aims to apply clustering algorithms to segment
proximity measures for various amenities as provided by Statistics
Canada. This clustering will allow the continuous PMD metrics to be
summarized as categorical variables, improving their usefulness in
interpretation and application. The insights gained from this
segmentation may help policymakers and urban planners to make better
decisions and plans for community development.

The analysis began with exploratory data analysis, examining missing
values, the distribution of proximity measures, outliers, and the impact
of log-transformation on proximity measures. Univariate clustering was
then conducted, applying clustering techniques to individual amenity
log-transformed proximity measures. Before clustering each amenity, a
clustering tendency check was performed to evaluate whether the data was
suitable for clustering, as clustering techniques can produce clusters
even when data is not inherently clusterable. Various clustering
techniques were applied, including density-based (HDBSCAN, OPTICS),
distribution-based (MixAll, MCLUST), and centroid-based (PAM) methods.
Several cluster validation metrics were utilized to determine the
appropriate number of clusters for each algorithm and assess the quality
of clustering results. Finally, cluster profiling investigated
additional variables such as the Index of Remoteness (IoR), number of
DBs, and DB population to gain insights about the clusters.

The results of the current investigation were mixed. Even after
log-transformation, assessment of clustering tendency demonstrated that
the PMD is not particularly clusterable. This lack of natural divisions
in the data led to inconsistent cluster cutoffs that were sensitive to
the algorithm used. Not only did different clustering algorithms find an
inconsistent number of clusters for the same amenity, but the location
of the cutoffs between clusters also varied. However, there were
instances where some cutoffs were relatively close to one another.
Cluster profiling revealed that, for most amenities, different clusters
have distinct characteristics. In most cases, as the proximity measure
increases, the median DB population also tends to increase while median
IoR decreases. This pattern suggests that areas with higher population
tend to be less remote and have higher proximity to amenities.

The most significant takeaway from the current investigation is the lack
of clear-cut segments in the PMD. While it is true that log-transforming
the proximity measures did reveal certain density-sparse regions, the
clustering algorithms utilized did not consistently identify these
regions. As a result, we observed a lack of stability in the clustering
results. This is also reflected by the lack of consensus suggested by
the cluster validation metrics. Certainly, this does not invalidate the
ability of the PMD to accurately judge proximity to amenities; rather,
it suggests that proximity to amenities across Canada is a relatively
smooth gradient without any obvious natural clusters.

## Introduction

Every individual lives somewhere and inhabits physical space. Unless one
lives completely removed from others, amenities such as schools, places
of employment, and healthcare facilities are usually present in the
built environment. As Alasia et al. (2021) outline, "having physical
access to basic services and amenities is a key determinant of social
inclusion, their capacity to meet basic needs, and their ability to
fully participate in social and economic development." These amenities
play a vital role in improving residents' quality of life, with their
distribution being a product of meticulous policy and planning by
governing bodies. In the context of urban development, accurately
predicting population movement relies on the accessibility of land for
the population. By utilizing accessibility measures at the
'dissemination block' (DB) level, it becomes possible to enhance the
accuracy of population movement predictions and make urban planning more
precise. Like people, amenities inhabit physical space, and not
everybody is equidistant from them. Therefore, it is imperative for
governing bodies to make deliberate, well-informed decisions as to the
location of new amenities and services.

The Proximity Measure Database (PMD) developed by the Data Exploration
and Integration Lab (DEIL) at Statistics Canada serves to provide a
granular measure of proximity to services and amenities across Canada to
inform planning and policy questions (Alasia et al., 2021). The PMD
contains continuous measures for 10 amenities at a DB level, the most
granular area defined by Statistics Canada (2021). In an urban area, a
DB corresponds to a city block, whereas in rural regions they are areas
"bounded by roads or other natural features" (Alasia et al., 2021).
Thus, DBs differ broadly in their size as well as in their proximity to
these amenities.

The aim of this project is to group the continuous proximity measures in
the Statistics Canada's PMD into distinct categories using different
clustering techniques. By doing so, we can create a more straightforward
and easier-to-understand measure. Categorizing the data means putting
similar values together in one group and dissimilar values in other
groups. This segmentation research helps to preprocess and clean the
dataset for use in future research, as a highly detailed continuous
variable may sometimes offer too much information. Transforming it into
a categorical variable makes it easier to analyze with descriptive
statistics or regression models. Using categorical variables in
regression allows for better interpretation of coefficients and other
statistical results. This research aims to simplify the work of
researchers who may not have the time to preprocess their datasets.
Similar efforts have been made by Statistics Canada in the past to
transform continuous metrics into categorical ones (Subedi et al.,
2020). Improving the understanding and use cases of the PMD will enable
policymakers and urban planners to prioritize efforts effectively to
enhance accessibility and promote social and economic sustainability
within communities. In this report, we outline the methodologies used to
explore segmentation of the continuous proximity measures, the
robustness of the group boundaries, and the characteristics of the
groups. The two specific research questions we aimed to addressed in the
project are:

1.  What are the optimal cut-off values and cluster boundaries for each
    amenity proximity measure in the PMD determined by appropriate
    clustering algorithms?

2.  What distinctive characteristics define each cluster of
    dissemination blocks, and how do these features contribute to both
    heterogeneity between clusters and homogeneity within each cluster?
    (Characteristics include: proximity measures, Census Metropolitan
    Area type, DB population, Index of Remoteness (IoR), and provincial
    breakdown.)

## Background

The methodology used to generate the PMD is presented in *Measuring
proximity to services and amenities*, by Alasia et al. with Statistics
Canada (2021). Accompanying this report is the Proximity Measures Data
Viewer, an online mapping application that allows users to view
proximity measures by DB for a selected amenity (Statistics Canada,
2020a). The continuous measure is segmented by quintiles and assigned a
colour, as shown in Figure [1](#pmdviewer), giving a user a rough idea of proximity
differences between DBs. For this reason, we used the 'quintile method'
as our base model in this project.

![Statistics Canada's Proximity Measures Data Viewer showing the proximity to the primary education amenity in Vancouver (top left), Edmonton (top right), Toronto (bottom left), and Calgary (bottom right).](https://raw.githubusercontent.com/sahaavi/Segmentation-of-Proximity-Measures/main/assets/final_plots/PMD_viewer/pmd_viewer2.png)(#pmdviewer)

**Figure 1:** Statistics Canada's Proximity Measures Data Viewer showing the proximity to the primary education amenity in Vancouver (top left), Edmonton (top right), Toronto (bottom left), and Calgary (bottom right).

A 'sister' measure to the PMD is the Index of Remoteness (IoR),
presented in *Measuring remoteness and accessibility* by Alasia et al.
(2017). They outline how a key factor affecting socioeconomic and health
outcomes is geographic proximity to population and service centers. As a
result, remoteness is relevant when analyzing and implementing policies
and programmes. The distance to all the population centers as well as
their population size are taken into account when calculating the index
for each census subdivision (CSD).
Figure [2](#iorspatial){reference-type="ref" reference="iorspatial"}
from the 2023 update of the publication summarizes their results. This
index was generated as a continuous measure, which was then partitioned
into categories as outlined in *Developing Meaningful Categories for
Distinguishing Levels of Remoteness in Canada* by Subedi et al. (2020).
The authors present five approaches to categorize the continuous
measure, which included methods like Jenks natural breaks, k-means, and
quintile classification. They aimed to examine various ways to group the
continuous remoteness index values of CSDs into meaningful categories
(Subedi et. al 2020). This is similar to our goal of categorizing the
continuous proximity measures of amenities in the PMD.

The Jenks natural breaks classification and k-means classification
techniques are examples of distribution and centroid based techniques,
respectively. Another type of clustering technique that may be
appropriate for our project are density based methods (De Smith et al.,
2021). As Kassambara, a Bioinformatics R&D Scientist at Veracytes,
outlines in his self-published book, the selection of an appropriate
clustering technique depends on the nature of the data under
investigation. He explains how before applying clustering techniques, it
is important to assess the clustering tendency to ensure meaningful
results, as clustering algorithms may identify clusters even in cases
where no clear clusters exist in the data. Additionally, determining the
optimal number of clusters is a necessary step in the process.
Kassambara outlines how once clustering techniques have been applied, it
is important to evaluate their performance using cluster validation
statistics such as the Silhouette Coefficient (Rousseeuw, 1987), Dunn
index (Dunn, 1974), and Davies Bouldin index (Davies & Bouldin, 1979).
These metrics assist in identifying the most suitable clustering
technique for the given data. By considering these factors, researchers
can make informed decisions and select the appropriate clustering
methodology for specific analysis (Kassambara, 2017).

![The spatial distribution of the 2021 Index of Remoteness over census
subdivisions in Canada. Source: DEIL
2023](./IoR/ior_spatial.png){#iorspatial width="\\textwidth"}

# Data

## Primary Dataset

The primary dataset for this study is the early release of the PMD,
available online and provided by the DEIL at Statistics Canada (2020b).
The updated PMD will be published online on the Statistics Canada
webpage on June 27th, 2023. The PMD contains continuous numerical
proximity measures for every DB in Canada within a select radius for 10
amenities: employment, grocery stores, pharmacies, health care, child
care, primary education, secondary education, public transit,
neighborhood parks, and libraries.

The proximity measures are based on a gravity model that accounts for
the distance between a reference DB and all the DBs within a given
travel distance in which the service is available. The proximity
measures also take into account the 'mass' of services within the given
distance, representing the number of services and their size. The
proximity measures are published as normalized index values, meaning
that the values resulting from computations were converted to a scale
from 0 to 1, where 0 indicates the lowest proximity value across Canada,
and 1 indicates the highest proximity value. The proximity level can be
seen as the quantity of service relative to the distance traveled
(Alasia et al., 2021). These measures are considered a reliable way to
assess local access to various amenities (OECD, 2018). The data
dictionary for this dataset can be found in
Figure [\[datadictionary\]](#datadictionary){reference-type="ref"
reference="datadictionary"} of
appendix [11.3](#extra){reference-type="ref" reference="extra"}.

## Data Limitations

Statistics Canada uses a specific convention for representing different
types of 'missing' values.
Table [1](#missingvalues){reference-type="ref"
reference="missingvalues"} shows the standard symbols that are used by
Statistics Canada. The symbols present in the PMD are '..' and 'F'.

::: {#missingvalues}
  **Symbol**   **Meaning**
  ------------ -----------------------------------------------
  .            not available for any reference period
  ..           not available for a specific reference period
  \...         not applicable
  F            too unreliable to be published

  : Missing value symbol convention from Statistics Canada.
:::

Values "too unreliable to be published" (F) are due to unavailability of
data in the many data sources used to construct the PMD. Data that is
'not available' (..) for a DB is the result of that DB being out of
scope: while producing the PMD, the authors considered a maximum travel
radius for each amenity, as a mean to reduce computational complexity as
well as to "reflect the fact that there is an upper limit to how far a
person will likely travel for most services" (Alasia et al., 2021). The
authors assigned ".." when no amenity was available within a given
travel radius for a select DB. As a result, not every DB has proximity
values for amenities.

In summary, data points may be unavailable either because the supporting
databases are incomplete, or because there is no access to the amenity
within the specified travel radius. The fact that a sizable portion of
DBs don't have an associated proximity measure is not a concern for this
project, as we want to segment the measures that are within the scope
set by the authors of the PMD.

## Other Data

We linked the IoR dataset to the PMD to add to the cluster profile
analysis. This dataset includes a continuous numeric remoteness score
for each CSD in Canada. The IoR is equal to zero for the least remote
CSD and equal to one for the most remote CSD. Details about the IoR were
outlined in section 3: Background of this report.

# Methods

The study began with an exploratory data analysis to gain familiarity
with the dataset and understand its characteristics. R and the
`tidyverse` package (Wickham et al., 2019) were used for data handling
and analysis. In parallel, clustering algorithms and validation metrics
were researched. The clustering tendencies of each amenity were
evaluated to assess the natural grouping potential of the data.
Different clustering algorithms and intuitive categorization methods,
such as quintiles and identifying minima, were applied to each amenity.
Computational constraints required clustering analyses to be performed
on a single 3% subsample of the dataset for feasibility. The
`ClusterCrit` package (Bernard, 2018) was used for cluster validation.
Profiling the resulting clusters for each technique provided insights
into their robustness and characteristics. The findings led to
conclusions and recommendations for future work.

## Data Preprocessing and Exploration

In order to better understand the structure of the data, we performed an
exploratory data analysis (EDA). We analyzed numerical variables (all
ten amenities plus DB population) in the PMD using summary statistics,
and we counted unique values for categorical variables. We also
visualized the distributions of each of the ten amenities using density
plots. The distributions showed a strong right skew. To see any
improvements, we also visualized the log-transformed proximity values of
the amenities. To avoid issues with infinite values during the log
transformation, we added a small value of 0.0001 to all the proximity
values. This adjustment was necessary because some proximity values were
zero. This small value was chosen as a practical compromise to allow the
log transformation of zero proximity values without significantly
altering the structure of the data or the relative order of the
observations. Importantly, this value is significantly smaller than the
lower bounds of our proximity measures, ensuring that they essentially
remain zero in the transformed scale, hence preserving the original
structure. Thus, it ensured the transformed data maintains its integrity
for further analysis. Finally, we identified outliers via boxplots,
validated them using Rosner's test, and counted them before and after
log-transformation.

Logarithmic transforms are a common way to normalize skewed data, as
well as to reduce the effect of outliers.
Figure [3](#logtransform){reference-type="ref" reference="logtransform"}
shows the curves of a few representative logarithm functions. The
natural (base $e$) logarithmic curve can be broken down into three main
sections: a segment near zero where the function is quite vertical, with
very large slope, a second segment to the left of 1, where the slope is
still very large but not as large as the segment near zero, and a third
segment that extends from 1 to infinity where the function becomes more
horizontal and behaves as a data compressor. This compressive property
is useful for transforming exponential trends into linear ones and
exponential seasonality into a linear seasonality. It is also important
to note that the log function is the inverse of the exponential
function. Therefore, any exponential behaviour in the data will be
offset by the log transform. Lastly, it is common to add a constant
value ("epsilon") to the data before log transformation in order to
prevent the creation of infinite values, which occurs when 0 is log
transformed.

![A line plot showing the log function with several different
bases.](./distributions/logtransform.png){#logtransform width="60%"}

## Preliminary Clustering Analysis

We evaluated the clustering tendency of each amenity via Visual
Assessment of Tendency (VAT) as well as sort plots. VAT works by
plotting the distance matrix between all observations in the dataset.
Sort plots highlight natural breaks in a continuous vector by sorting
the values and then plotting them by index. We used the `fviz_dist`
function from the `factoextra` package (Kassambara et al., 2020) to
produce the VAT plots.

The quintile method is chosen to reflect the current segmentation in the
Proximity Data Viewer (Statistics Canada, 2020a). In this method, data
are sorted, and then split into 5 groups, each with the same number of
observations. This approach is therefore "blind" to the data, since the
actual values are not used in the creation of clusters. We considered
this approach as the "base model" to which comparisons will be made.

As an intuitive method, we applied a 'minima identification'
segmentation technique, which functions by cutting the distribution at
select minima of the density distribution. Each minima in the density
curves that are flanked by maxima of higher density represent a density
sparse region, which may be a 'natural' break in the continuous
measures. We conducted this non-parametric approach mathematically on
the logged transformed data where minima are perceptible.

## Advanced Clustering Analysis and Profiling

We tried different clustering techniques like HDBSCAN, MixAll, PAM,
VarSelLCM, and OPTICS to find suitable cutoff values for the amenity
proximity measures. Among them, only the results from HDBSCAN, MixAll,
MCLUST, and PAM algorithms were useful. VarselLCM wasn't able to produce
results with individual amenity proximity measures, and OPTICS produced
clusters that overlapped and had subclusters within a cluster. Summaries
of the unsuccessful approaches can be found in
section [11.2](#appendix:unsuccessful){reference-type="ref"
reference="appendix:unsuccessful"} of the Appendix.

In many clustering techniques, the user is required to specify the
desired number of clusters ($k$) to be generated (Kassambara, 2017). To
determine the appropriate number of clusters for each clustering
technique, various metrics were employed, including the silhouette
coefficient, Dunn index, Calinski-Harabasz, and Davies-Bouldin.

The silhouette coefficient is the average of silhouette values for all
individual data points. The silhouette value is the difference between
the average distance to points within the same cluster and the average
distance to points in the nearest neighboring cluster, divided by the
largest of the two. The resulting value is bounded between -1 and 1,
where values nearer to 0 indicate poor distinction between clusters, and
values nearer -1 or 1 are the result of better separation between
clusters. Negative values indicate that some points within a cluster are
closer to points in a neighbouring cluster than its own, suggesting a
'wrong' assignment. This metric should be maximized. (Rousseeuw, 1987).

The Dunn index reflects the separation between clusters and the
distances between observations in the same cluster: it is the ratio of
the largest intra-cluster distance and the smallest inter-cluster
distances. It ranges from zero to infinity and should be maximized.
(Dunn, 1974).

The Davies-Bouldin index calculates, for every pair of clusters, the sum
of the within clusters scatter divided by the separation between the
clusters. This metric should be minimized: if a value is smaller, that
means that either the sum of the cluster scatters is small, and/or the
separation between the clusters is large. (Davies & Bouldin, 1979).

The Calinski-Harabasz index calculates the ratio of the variance between
clusters and the variance within clusters, where the variance is taken
as the difference between cluster centroids and the global centroid for
the former and the difference between points in a cluster and their
cluster centroid for the latter. This metric should be maximized: higher
values are indicative of denser, well separated clusters, since the
metric may only be increased by either increasing the distances between
a cluster centroid and that of the global centroid, or by decreasing the
distances between points in a cluster and its centroid. (Calinski &
Harabasz, 1974).

Figure [4](#numselect){reference-type="ref" reference="numselect"} is an
example of a set of internal evaluation schemes values per number of
clusters for the MixAll clustering technique applied on the Employment
proximity values. The number of clusters suggested by each metric is as
follows:

-   Silhouette coefficient: 2 clusters

-   Dunn index: 3 clusters

-   Calinski-Harabasz: 8 clusters

-   Davies-Bouldin: 8 clusters

To determine the final number of clusters, the majority recommendation
from these metrics was considered. As 8 clusters were suggested by the
majority of the metrics, this number was chosen.

![Number of clusters suggested by different metrics for employment
amenity in MixAll clustering algorithm. We want to maximize all the
metrics except for the Davies-Bouldin, which we want to
minimize.](./coefs_demo/coefs_demo.png){#numselect width="\\textwidth"}

Originally, we expected the metrics to provide insight into which
clustering method performed the 'best'. Due to the conflicting
recommendations from clustering validation metrics, such as silhouette
coefficients, Dunn index, Calinski-Harabasz, and Davies-Bouldin, it
became challenging to select a single clustering technique for profiling
purposes. In light of this challenge, a different approach was adopted.

Instead of relying on a single algorithm for cluster profiling, multiple
techniques that had proven effective in the univariate case and produced
satisfactory results were utilized. This approach allowed for a more
comprehensive exploration of the data and ensured that the clustering
results were robust, and not solely dependent on a single technique.

The success of several algorithms may also be compared intuitively by
looking at how the cutoff values divide the log-transformed density
plots for each amenity. Successful algorithms will find the cutoff
values to be near the "troughs" or "density sparse regions" in these
density plots, with the clusters themselves being the "peaks" or "dense
regions". Conversely, poorly performing algorithms will miss these
troughs by placing the cutoffs randomly or near the peaks.

Following the identification of clusters, an investigation was conducted
to examine the profiles of these clusters. This involved comparing
various factors, including the number of DBs, median DB population,
median IoR, the mode of Census Metropolitan Area type, top province,
mode of amenity density, median proximity measure of the clustered
amenity, and the corresponding cutoff values.

# Results

## Data Exploration

### Summary Statistics

The PMD contains 489,676 rows, each of which corresponds to a unique DB.
Each row contains information about DB population, the encompassing CSD
and province, an indicator of amenity density, whether or not the DB is
within a census metropolitan area (CMA), plus all of the ten proximity
measures. The amenity dense indicator is split into low, medium and high
density, with around 5,000 getting an 'F' for "too unreliable to be
published." CMA type is divided into four groups: a CMA, not a CMA, a
tracted census agglomeration (CA), or an untracted CA ('tracted' in this
case refers to whether or not the CA has been subdivided into smaller
sections for census purposes). In addition, there is an indicator for
each of the ten amenities that relates whether or not the amenity in
question resides in the same DB for which the proximity is being
calculated. Lastly, there is an indicator for whether or not a DB is
considered "amenity dense." We've outlined earlier reasons for which DBs
may not have proximity measures. Table 2 shows the amount of DBs that
have proximity values for each amenity: Employment has the greatest
coverage, at 86.5%, whereas Library has the least at 23%. It is assumed
that this is a result of the set travel radius for Employment being much
larger, as it covers 10 driving kilometers, whereas libraries are only
searched within 1.5 walking kilometers.

::: {#missingdata}
                         DBs with Data Available   Percentage
  --------------------- ------------------------- ------------
             Employment          423,602              86.5
               Pharmacy          178,521              36.5
              Childcare          243,964              49.8
             Healthcare          300,465              61.4
                Grocery          141,063              28.8
      Primary Education          225,359              46.0
    Secondary Education          141,213              28.8
                Library          112,655              23.0
                  Parks          234,068              47.8
                Transit          181,305              37.0
          DB Population          487,526              99.6

  : Counts and percentages of missing values of numerical variables in
  the PMD.
:::

Table [\[summary\]](#summary){reference-type="ref" reference="summary"}
shows the summary statistics for the numerical variables in the PMD,
while Table [3](#categorical){reference-type="ref"
reference="categorical"} shows the counts for each type of the
categorical variables. We see that the 90th percentile of the proximity
measures for all amenities are values that are much nearer the smaller
end of the domain; the largest value is in Primary Education, at 0.233.
This is not the only indicator that this measure is unbalanced: the skew
and kurtosis values are all relatively high.

::: {#categorical}
  **Variable**                      **Counts**
  --------------------------------- ------------
  DBs Per Province                  
  *Alberta*                         66,749
  *British Columbia*                52,850
  *Manitoba*                        30,669
  *New Brunswick*                   14,345
  *Newfoundland and Labrador*       8,756
  *Northwest Territories*           1,495
  *Nova Scotia*                     15,279
  *Nunavut*                         792
  *Ontario*                         133,214
  *Prince Edward Island*            3,639
  *Quebec*                          106,251
  *Saskatchewan*                    54,118
  *Yukon*                           1,519
  CMA Type                          
  *CMA (B)*                         206,709
  *Untracted CA (D)*                53,061
  *Tracted CA (K)*                  16,992
  *Not a CMA or CA*                 212,914
  Amenity Dense                     
  *Low Density (0)*                 442,179
  *Medium Density (1)*              37,303
  *High Density (2)*                4,827
  *Too unreliable to publish (F)*   5,367
  Suppressed                        
  *Not suppressed (0)*              484,309
  *Info. Suppressed (1)*            5,367

  : Summary statistics for categorical variables in the PMD.
:::

### Distributions

The distributions of the proximity scores for all amenities are heavily
right-skewed, with the majority of the values being grouped near zero,
as seen in Figure 3 (left). These distributions then appear to decay
smoothly. The strong right-skew results from a relatively small number
of high access outliers, which influences the distribution when the
measures are normalized. The presence of these outliers is further
demonstrated through the Interquartile Range (IQR), with values lying
beyond 1.5 times the IQR above the third quartile or below the first
quartile classified as outliers. However, in this paper, the outliers
are considered valid since they are not the result of measurement
errors. Figure [5](#comparedist){reference-type="ref"
reference="comparedist"} shows the comparison of the density
distributions before and after log-transformation.
Figures [40](#dendist){reference-type="ref" reference="dendist"} and
[41](#logdendist){reference-type="ref" reference="logdendist"} in
section [11.3](#extra){reference-type="ref" reference="extra"} of the
Appendix show these same distributions for all ten amenities. We can
already see that the log-transformed distributions are better because
the distribution of the proximity values are more normally distributed,
and density sparse regions are now visible. Box-Cox and Arcsine
transformations were also attempted, but did not yield distributions
that were as consistently normally-distributed as those that were
log-transformed. It is important to note that log-transforming the
proximity measures does not change the structure of the data. In other
words, a particular DB 'A' in the non-log-transformed data with less
proximity than another DB 'B' will still have less proximity in the
log-transformed data. Statistical summary
Table [\[summary\]](#summary){reference-type="ref" reference="summary"}
for the log-transformed data can be found in
section [11.3](#extra){reference-type="ref" reference="extra"} of the
Appendix as Table [\[logsummary\]](#logsummary){reference-type="ref"
reference="logsummary"}. In contrast, the skew and kurtosis values for
the logged data are much smaller, which proves that the
log-transformation was successful in reducing the extreme right skew of
these proximity values. Kurtosis is a statistical measure that
quantifies the shape of a distribution, specifically focusing on the
presence and extent of outliers or extreme values. Distributions with a
large kurtosis have more tail data than normally distributed data, which
appears to bring the tails in toward the mean. Distributions with low
kurtosis have fewer tail data, which appears to push the tails of the
bell curve away from the mean (Kenton, 2023).

![Distribution of the proximity measure to primary education services
before and after
log-transformation.](./distributions/compare_distributions.png){#comparedist
width="\\textwidth"}

In this paper, log-transforming the data is important to clustering
because of skewness of the data, and helps reveal the underlying
structure. Data points near zero in the non-transformed data are
"clumped" around particular values, as opposed to being smoothly
distributed. This preference for particular values is what creates the
miniature peaks that can be seen on the left hand side of the
log-transformed density distribution in the employment amenity in
Figure [41](#logdendist){reference-type="ref" reference="logdendist"} of
Appendix section [11.3](#extra){reference-type="ref" reference="extra"}.
These miniature peaks represent real clusters in the data, and are not
simply an artifact of the transformation itself.

Before log-transforming the data, the outliers present had a significant
effect on the skew of the data. Many clustering algorithms form clusters
based on the distance measure they employ. For instance, algorithms like
k-means utilize a squared Euclidean distance, leading to the formation
of circular, spherical, or hyperspherical clusters (MacQueen, 1967).
Outliers can significantly distort the centroids of these clusters,
thereby exerting a substantial influence on the overall shape of the
clusters. The number of outliers was significantly reduced by
log-transforming the data, as this reduced the relative distance between
points. The reduction in the number of outliers after log-transformation
can clearly be seen in
Table [\[outliercounts\]](#outliercounts){reference-type="ref"
reference="outliercounts"} (boxplots for visualizing outliers can be
found as Figures [38](#boxoutliers){reference-type="ref"
reference="boxoutliers"} and [39](#logboxoutliers){reference-type="ref"
reference="logboxoutliers"} in Appendix section
[11.3](#extra){reference-type="ref" reference="extra"}). In addition to
log-transforming the proximity measures to reduce the number of
outliers, statistical modeling techniques that are robust to outliers
were chosen for clustering. In the future, we can include outliers
(values that are much larger than the normal ones) in a single cluster
to see what happens when they are treated separately. This will allow us
to examine how clustering techniques perform when outliers are not
present in the data.

Due to the reduction in the number of outliers as well as the
improvement in distribution shape (high right skew to quasi-normal), the
following clustering analyses were performed on the individual
log-transformed measures as opposed to the original measures. For
clarity, it is also pertinent to mention that the proximity measures
were clustered individually as opposed to being clustered in concert
with other variables. This approach was chosen for its simplicity, but
other multivariate clustering approaches should be attempted in the
future.

## Clustering Tendency

The first of the two assessments of clustering tendency was the VAT. In
this test, highly clusterable data is visualized having clearly defined
rectangles that lie along the diagonal. In contrast, data with low
clustering tendency does not have clear rectangles lying along the
diagonal, but instead has a jumble of lines and inconsistent colouring.
In the VAT plots for the non-transformed data, consistent low clustering
tendency is observed. For the log-transformed data, it seems as though
the data is semi-clusterable, as there are rectangles, but they are
poorly defined and not as distinct as they could be. The VAT plots for
all log-transformed amenities in the PMD can be seen in
Figure [6](#allvat){reference-type="ref" reference="allvat"}.

![VAT plot results for all log-transformed proximity
measures.](./vat/vat_collage_labels.png){#allvat width="\\textwidth"}

The second of the two assessments of clustering tendency are sort plots.
If a unidimen- sional dataset is highly clusterable, then the sort plots
will show obvious discontinuous points and changes in slope which
separate the clusters. However, this is not observed, as is shown in
Figure [7](#sortplotcompare){reference-type="ref"
reference="sortplotcompare"}. The non-transformed and log-transformed
sort plots for the primary education amenity are shown here for an
example. Instead of showing obvious breaks, the lines are smooth. This
indicates that there are not any obvious clusters in either the
non-transformed or log-transformed data. This has implications for the
interpretability of our results, as the cutoff points identified between
clusters may be sensitive to changes in the data.

![Sort plots of the proximity measure to primary education services
before and after
log-transformation.](./sort_plot/sort_comparison.png){#sortplotcompare
width="\\textwidth"}

## Quintiles

While easy to understand, the quintile method is a "blind" algorithm,
and therefore fails to find good cutoff values. As seen in
Figure [8](#prieduccutoffs){reference-type="ref"
reference="prieduccutoffs"}, the cutoffs mostly miss the density sparse
regions, and are able to find them only in a few cases by mistake.

## Minima Identification

This method is the most intuitive: the minima of the kernel density
curves represent density sparse regions, which may be appropriate areas
to segment between naturally occurring groups. However, as seen in
Figure [8](#prieduccutoffs){reference-type="ref"
reference="prieduccutoffs"}, for many amenities there are large portions
of the curve that do not have local minima, resulting in some groups
being much larger than others. If choosing cutoff values fully manually,
one may choose a point where the curve plateaus or has a flatter slope.
Future work may include inflection points on the distribution curve as
potential cutoff values.

We used the `density` function in the `stats` package with the default
bandwidth and the default gaussian kernels to create the density curves.
Changing the bandwidth of the kernel density has an effect on the
results: smaller bandwidths result in more density sparse regions and
more minima, whereas greater bandwidths result in 'flatter' curves and
less minima. Future work should investigate how the size of the
bandwidth affects the resulting clusters.

There were many unexpected local minima in the density curves in areas
where the density was very small and flat. To retain only the minima
that represent density sparse regions amongst regions with higher
density, a limiting threshold of 0.001 was set for the difference
between neighbouring maxima and minima. Intuitively, if the difference
between a local maximum and a local minimum was very small, then the
minimum is not representative of a good segmentation point.

Given that the cutoff points selected in this method directly represent
density sparse regions, which we intuitively think of as 'gaps' between
groups, we expect the validation metrics to be better than those for the
'quintiles' method. We see in
Table [\[prieducmetrics\]](#prieducmetrics){reference-type="ref"
reference="prieducmetrics"} that, for example, in the case of the
Primary Education amenity, only some of the metrics are better, like the
silhouette coefficient and the Dunn index, whilst the Davies-Bouldin and
the Calinski-Harabasz actually perform worse. This incongruity is a
result of what each of these metrics calculates and represents.

## Clustering

### Comparison of Algorithms

We applied multiple clustering algorithms, with the specifics outlined
in Appendix [11.1](#appendix:successful){reference-type="ref"
reference="appendix:successful"}. Among these, MixAll, HDBSCAN, PAM, and
MCLUST emerged as successful. In this context, 'successful' refers to
the algorithms that were not only able to run with our univariate data
but also provided intuitive results in the form of distinct and
non-overlapping clusters.
Figure [8](#prieduccutoffs){reference-type="ref"
reference="prieduccutoffs"} shows the plots of the logged-transformed
density distributions with the resulting groups coloured for the
representative amenity of Primary Education, while
Table [\[numclusts\]](#numclusts){reference-type="ref"
reference="numclusts"} outlines specifically the number of clusters each
method suggested. We can already see how most of the time, the cutoff
values for the different methods don't align with each other: each
method finds different points where to segment the data. Even when some
methods find more groups than others, aggregating some of the smaller
groups doesn't necessarily result in the larger group of another method.

![Cutoff values from each segmentation approach displayed on the
log-transformed density distributions for the primary education
amenity.](./cutoffs/by_amenity/Primary Education_cutoffs.png){#prieduccutoffs
width="\\textwidth"}

### Cluster Profiles

Table [\[prieducprofile\]](#prieducprofile){reference-type="ref"
reference="prieducprofile"} shows the profiles of each of the clusters
defined by each of the successful univariate clustering algorithms for
the primary education amenity. We assigned numerical labels to the
clusters generated by each algorithm based on their proximity values.
The clusters with the lowest proximity were labeled as cluster 1, and
the clusters with higher proximity were assigned higher numbers. The
other summary variables seem to be roughly correlated with proximity to
primary education: as this proximity increases, DB population seems to
increase, median IoR seems to decrease, percentage of CMA DBs increases,
percentage of DBs in Ontario increases, and the percentage of low
amenity dense DBs decreases. All of these trends seem to indicate that
proximity to primary education is highest in densely populated cities.
Figure [9](#prieducbarplot){reference-type="ref"
reference="prieducbarplot"} summarizes these same clusters by showing
the number of DBs and number of people in each cluster for each
algorithm.

![Proportion of DBs and population in each cluster for all approaches
for the primary education
amenity.](./barplot_comparison/Primary Education_barplot.png){#prieducbarplot
width="\\textwidth"}

![Cutoff values compared for the primary education amenity for all
clustering
approaches.](./cutoff_ticks/Primary Education_ticks.png){#prieducticks
width="\\textwidth"}

# Analysis

In general, when analyzing various amenities and their clustering
results, a pattern emerges where the median proximity measure or cluster
range is directly related to the median DB population and median IoR. As
the proximity measure or range increases, the median DB population also
tends to increase and median IoR tends to decrease. This pattern
suggests that areas with higher population tend to be less remote and
have better access to amenities.

However, it's important to note that this pattern may not hold true for
every clustering technique in all amenities. In the case of amenities
like pharmacies, the clustering results obtained from MCLUST may not
precisely follow this pattern for the median DB population. This
discrepancy could be attributed to MCLUST identifying multiple clusters,
some of which may be relatively small in terms of no of observations
included in that cluster, resulting in a narrower range of data and
affecting the representation of the median.

Overall, while the general trend of increasing median DB population with
higher proximity measures holds across multiple amenities and clustering
techniques, there may be variations and exceptions in specific cases,
particularly when the clustering results include small clusters with
limited population.

Moreover, upon examining
Table [\[employmentprofiles\]](#employmentprofiles){reference-type="ref"
reference="employmentprofiles"} to
Table [\[transitprofiles\]](#transitprofiles){reference-type="ref"
reference="transitprofiles"}, it becomes evident that all amenities
demonstrate a low mode of amenity density for the entire population of
Canada. This observation holds true not only for the overall population
but also for the majority of individual clusters. This aligns with the
findings from the EDA, which indicated that approximately 90% of the DBs
in Canada exhibit a low level of amenity density.

## Employment

In Figures [11](#employmentbarplot){reference-type="ref"
reference="employmentbarplot"},
[12](#employmentcutoffs){reference-type="ref"
reference="employmentcutoffs"} and
[13](#employmentticks){reference-type="ref" reference="employmentticks"}
we can see that the methods provide mostly different numbers of groups
at different cutoff points. MCLUST has a lot more cutoffs, providing
nine almost balanced groups, in terms of number of DBs. The fourth
cutoff for MCLUST is close to the cutoffs for PAM and MixAll, but the
minima identification and the HBDSCAN methods do not find a cutoff at
that value. The HDBSCAN only settled on one cutoff, which is different
from all other methods: MCLUST's last cutoff comes the closest to it.
The minima identification cutoffs seem to all be concentrated almost
within the second group of MCLUST cutoffs. Whether they are
statistically equal or similar is a different question, whose answer
cannot be answered with a visual assessment. It makes sense that PAM and
MixAll find similar cutoffs, as the algorithms are similar.

Overall, we can see how the proportions of DBs and proportions of total
population in each cluster differs across methods. We see that MixAll
and PAM have similar proportions of both in their two clusters. We can
also see that in the Quintiles method, there are equal number of DBs per
cluster, as that is what the method is by definition. Despite that, we
see that the proportions of population are not equal, but each
subsequent cluster contains greater proportions of population. This is
not exactly the case for every amenity. This suggests that for
Employment, the DBs that have higher proximity values also have higher
populations on average than the DBs with lower proximity values to
employment. This trend is similar for all the methods: groups with
larger proximities hold generally a larger proportion of the population
than the proportion of DBs.

Table [\[employmentprofiles\]](#employmentprofiles){reference-type="ref"
reference="employmentprofiles"} shows the summary statistics for every
cluster. We see that the summary statistics differ across groups. For
the most part, the median population of each cluster increases as the
median proximity score increases, suggesting that areas with higher
employment proximity scores generally also have higher populations. The
median Index of Remoteness generally decreases as the median proximity
score increases.

Table [\[employmentvalid\]](#employmentvalid){reference-type="ref"
reference="employmentvalid"} shows the validation metric values for each
clustering approach. The best Silhouette coefficient is from the HDBSCAN
method, which also has the best Davies Bouldin index. The best Dunn
index is from the PAM (followed closely by the MixAll), and the best
Calinski Harabasz is from the MCLUST method.

Overall, it seems that for the employment amenity, the cutoff values are
not similar across methods and the validation metrics don't have a
consensus, suggesting that the proximity measures are not easily grouped
algorithmically. However, the groups are somewhat characteristically
distinct.

![Proportion of DBs and population in each cluster for all approaches
for the employment
amenity.](./barplot_comparison/Employment_barplot.png){#employmentbarplot
width="\\textwidth"}

![Cut-offs values shown on the log-transformed density plots for all
clustering approaches for the employment
amenity.](./cutoffs/by_amenity/Employment_cutoffs.png){#employmentcutoffs
width="\\textwidth"}

![Cutoff values compared for the employment amenity for all clustering
approaches.](./cutoff_ticks/Employment_ticks.png){#employmentticks
width="\\textwidth"}

## Pharmacy

In Figure [14](#pharmacybarplot){reference-type="ref"
reference="pharmacybarplot"},
[15](#pharmacycutoffs){reference-type="ref" reference="pharmacycutoffs"}
and [16](#pharmacyticks){reference-type="ref"
reference="pharmacyticks"}, we see again how for the most part, cutoff
values across methods do not align. It seems like the first minima
identification and HDBSCAN cutoffs are close with the third MCLUST
cutoff, which may indicate robustness. Again, the MixAll cutoff is
nearly identical to the PAM cutoff. HDBSCAN's second cutoff is somewhat
close to MCLUST's 6th cutoff. In this case, MCLUST settles on some very
small groups amongst other more equi-sized. We see that overall, the
proportions of population in each cluster are similar to the proportions
of DBs in each cluster.

In Table [\[pharmacyprofiles\]](#pharmacyprofiles){reference-type="ref"
reference="pharmacyprofiles"}, we see that the median IoR for each group
is more constant, especially relative to the Employment median IoR. The
case is similar for the median population. We also see that in every
group, the majority CMA type is CMA. This suggests that the proximity
measures for the Pharmacy amenity are not as correlated to the
populations or remoteness, and the groups are not characteristically
distinct from each other.

Table [\[pharmacyvalid\]](#pharmacyvalid){reference-type="ref"
reference="pharmacyvalid"} shows the validation metric values for each
clustering approach. The best Silhouette coefficient is tied amongst the
MixAll and the PAM methods. MixAll performs the best according to all
the other metrics, although the PAM values are pretty similar, which was
expected given the results from
Table [\[pharmacyprofiles\]](#pharmacyprofiles){reference-type="ref"
reference="pharmacyprofiles"} and
Figure [14](#pharmacybarplot){reference-type="ref"
reference="pharmacybarplot"}.

Overall, the cutoff values are not similar to each other apart from a
few and the groups are not characteristically distinct, suggesting that
the pharmacy proximity measures are not distinctly groupable. The method
with the best validation metrics is the MixAll algorithm, which only
provides 2 groups.

![Proportion of DBs and population in each cluster for all approaches
for the pharmacy
amenity.](./barplot_comparison/Pharmacy_barplot.png){#pharmacybarplot
width="\\textwidth"}

![Cut-offs values shown on the log-transformed density plots for all
clustering approaches for the pharmacy
amenity.](./cutoffs/by_amenity/Pharmacy_cutoffs.png){#pharmacycutoffs
width="\\textwidth"}

![Cutoff values compared for the pharmacy amenity for all clustering
approaches.](./cutoff_ticks/Pharmacy_ticks.png){#pharmacyticks
width="\\textwidth"}

## Child care

In Figure [17](#childcarebarplot){reference-type="ref"
reference="childcarebarplot"},
[18](#childcarecutoffs){reference-type="ref"
reference="childcarecutoffs"} and
[19](#childcareticks){reference-type="ref" reference="childcareticks"}
we see the proportion of DBs and population in each cluster for each
method. We again can observe that most cutoff values don't align with
each other. Again, the MixAll and the PAM are matching. The first HBSCAN
and minima identification cutoffs are otherwise the only ones somewhat
aligned. The MCLUST cutoff aligns with the third Quintile cutoff, but
since the Quintile method is blind to the data, it isn't of any
significance. We see that the proportions of population are somewhat
shifted relative to the proportion of DBs, suggesting that there may be
slight differences in populations correlated with differences in
proximity values.

Table [\[childcareprofiles\]](#childcareprofiles){reference-type="ref"
reference="childcareprofiles"} shows the summary statistics for each
method and cluster for the Childcare amenity. An anomaly lies in the
MCLUST C1: the median population is much larger. The number of DBs is
also very small; it may be indicative that other cluster's medians are
affected by a large number of DBs with very small populations.The median
IoR seem to be dissimilar in different groups as the median proximity
value increases. The CMA types of clusters with lower proximity values
are of majority type not CMA, whereas those with higher proximity values
in majority CMA types.

Table [\[childcarevalid\]](#childcarevalid){reference-type="ref"
reference="childcarevalid"} shows the validation metric values for each
clustering approach. MCLUST has the best Silhouette coefficient (MixAll
runner up) and the best Davies Bouldin index (MixAll runner up).
PAM-means has the best Dunn index (MixAll runner up), and MixAll the
best Calinski Harabasz value (PAM runner up). These results suggest that
since MixAll is consistently in the top 2 relative to the other methods,
it may be the best, even though it only finds 2 groups.

Overall, the cutoff values are mostly dissimilar from each other, but
the groups do hold different characteristics from each other, suggesting
that the proximity values may be clusterable using different methods
and/or in cohort with additional variables.

![Proportion of DBs and population in each cluster for all approaches
for the child care
amenity.](./barplot_comparison/Child care_barplot.png){#childcarebarplot
width="\\textwidth"}

![Cut-offs values shown on the log-transformed density plots for all
clustering approaches for the child care
amenity.](./cutoffs/by_amenity/Child care_cutoffs.png){#childcarecutoffs
width="\\textwidth"}

![Cutoff values compared for the child care amenity for all clustering
approaches.](./cutoff_ticks/Child care_ticks.png){#childcareticks
width="\\textwidth"}

## Healthcare

In Figure [20](#healthcarebarplot){reference-type="ref"
reference="healthcarebarplot"},
[21](#healthcarecutoffs){reference-type="ref"
reference="healthcarecutoffs"} and
[22](#healthcareticks){reference-type="ref" reference="healthcareticks"}
we see the proportion of DBs and population in each cluster for each
method for the Healthcare amenity. In this case, it seems like none of
the cutoffs align across methods: even the MixAll and PAM don't exactly
agree, although they are still close to each other. The minima
identification method finds most clusters at lower proximity values,
whereas the HDBSCAN's cutoff is at a high proximity value. It seems like
cutoffs for the population proportions are shifted left relative to the
proportions of DBs, suggesting a trend with the population values and
proximity values.

Table [\[healthcareprofiles\]](#healthcareprofiles){reference-type="ref"
reference="healthcareprofiles"} shows the summary statistics for each
cluster. In this case, there are many cases where the majority CMA type
is not CMA. The median population seem to differ across groups, as well
as the median IoR. The proportion of DBs within groups is not constant,
as we had seen in Figure [20](#healthcarebarplot){reference-type="ref"
reference="healthcarebarplot"}.

Table [\[healthcarevalid\]](#healthcarevalid){reference-type="ref"
reference="healthcarevalid"} shows the validation metric values for each
clustering approach. HDBSCAN has the best silhouette coefficient by over
9 points as well as the best Davies-Bouldin result. The PAM has the best
Dunn index, although the MixAll method's value follows closely. The
MCLUST algorithm has the best Calinski Harabasz measure.

Overall, the cutoff values are mostly dissimilar from each other and the
validation metrics mostly don't agree with each other, but the groups do
hold different characteristics from each other, suggesting that the
proximity values may be clusterable using different methods and/or in
cohort with additional variables.

![Proportion of DBs and population in each cluster for all approaches
for the health care
amenity.](./barplot_comparison/Health care_barplot.png){#healthcarebarplot
width="\\textwidth"}

![Cut-offs values shown on the log-transformed density plots for all
clustering approaches for the health care
amenity.](./cutoffs/by_amenity/Health care_cutoffs.png){#healthcarecutoffs
width="\\textwidth"}

![Cutoff values compared for the health care amenity for all clustering
approaches.](./cutoff_ticks/Health care_ticks.png){#healthcareticks
width="\\textwidth"}

## Grocery

Looking at the summary statistics in
Table [\[groceryprofiles\]](#groceryprofiles){reference-type="ref"
reference="groceryprofiles"},
Figure [24](#grocerycutoffs){reference-type="ref"
reference="grocerycutoffs"} and [25](#groceryticks){reference-type="ref"
reference="groceryticks"} for the grocery amenity, we observe that the
first cluster cutoffs are quite similar among the minima identification,
HDBSCAN, and PAM clustering approaches. The cutoffs range from 0 to
0.0121, 0 to 0.0124, and 0 to 0.0113, respectively. Consequently, these
clusters also exhibit similar numbers of DBs and DB population, as shown
in Figure [23](#grocerybarplot){reference-type="ref"
reference="grocerybarplot"}. However, these techniques do not agree on
the cutoffs for the remaining data.

On the other hand, the quintiles technique simply divides the data into
five equal parts, which does not align with the cutoffs obtained from
any other clustering techniques. Similarly, the MixAll clustering
cutoffs do not match with those of any other technique for any of the
clusters.

Table [\[groceryvalid\]](#groceryvalid){reference-type="ref"
reference="groceryvalid"} provides insights into the performance
metrics, such as the Silhouette coefficient and Calinski Harabasz.
Silhouette coefficient and Dunn index suggest that the MCLUST algorithm
clusters the grocery amenity data better, dividing it into three groups.
On the other hand, the Calinski Harabasz and Davies Bouldin indices
favor PAM as the better performer, clustering the grocery amenity into
eight groups. Interestingly, the first cluster identified by PAM is
further divided into two clusters by MCLUST, while the rest of the data,
where MCLUST identifies only one cluster, is separated into seven
clusters by PAM.

Based on this analysis, it strongly suggests that cluster 1 should have
a cutoff range of 0 to 0.0113, as suggested by the PAM technique. This
suggestion is supported by the validation from two metrics indicating
its better performance and also almost matches with the cutoff range of
the first cluster identified by the other two clustering techniques
(minima identification and HDBSCAN). However, for the remaining data,
none of the techniques agree on the cutoffs, indicating a lack of
consensus.

![Proportion of DBs and population in each cluster for all approaches
for the grocery
amenity.](./barplot_comparison/Grocery_barplot.png){#grocerybarplot
width="\\textwidth"}

![Cut-offs values shown on the log-transformed density plots for all
clustering approaches for the grocery
amenity.](./cutoffs/by_amenity/Grocery_cutoffs.png){#grocerycutoffs
width="\\textwidth"}

![Cutoff values compared for the grocery amenity for all clustering
approaches.](./cutoff_ticks/Grocery_ticks.png){#groceryticks
width="\\textwidth"}

## Primary Education

The number of clusters identified for the primary education amenity
varies considerably between algorithms. While MixAll and PAM find only
two clusters, MCLUST finds seven. While the majority of the cutoff
values also vary between algorithms, there is some consistency. For
example, the Minima identification method and HDBSCAN seem to agree as
to the cutoff value between clusters 1 and 2. Additionally, Minima
identification, MixAll and PAM are all able to find the density sparse
region around 0.082 (figure [8](#prieduccutoffs){reference-type="ref"
reference="prieduccutoffs"} and [10](#prieducticks){reference-type="ref"
reference="prieducticks"}). Despite the overall variation in cutoff
values between approaches, there is not one algorithm that clearly
outcompetes the others. This can be seen by comparing the different
approaches using common clustering validation metrics
(Table [\[prieducmetrics\]](#prieducmetrics){reference-type="ref"
reference="prieducmetrics"}). MixAll and PAM maximize the silhouette
coefficient, whereas MCLUST maximizes the Dunn and Calinski Harabasz
indices. Finally, the Minima identification method minimizes the Davies
Bouldin index. Therefore, it is unclear which algorithm produces the
'best' cutoff values.

Table [\[prieducprofile\]](#prieducprofile){reference-type="ref"
reference="prieducprofile"} shows that proximity to primary education is
highest in densely populated cities. This is supported by the fact that
clusters with higher proximity to primary education also have: a higher
percentage of DBs in CMAs, a lower percentage of low amenity dense DBs,
and a lower median IoR. Another interesting trend is that clusters with
increased proximity to primary education also have more DBs in Ontario.
This is likely because Ontario has a higher percentage of DBs in CMAs.

While the mode of the categorical variables remains the same for most
clusters, MCLUST is able to identify a unique cluster of DBs that does
not follow the consensus. MCLUST's cluster 1 seems to be finding a small
number of DBs that are rural (non-CMA), decently populated, and spread
out fairly evenly across all of Canada. 100% of these DBs have low
amenity density, and their proximity to primary education is the lowest
of any cluster identified. While this cluster consists of only a very
small percentage of the total number of DBs, the profile of this cluster
differs significantly enough to be considered a valid, unique cluster.
Additional cluster breakdown can be seen in
Figure [9](#prieducbarplot){reference-type="ref"
reference="prieducbarplot"}.

## Secondary Education

By analyzing the summary statistics in
Table [\[seceducprofiles\]](#seceducprofiles){reference-type="ref"
reference="seceducprofiles"},
Figure [27](#seceduccutoffs){reference-type="ref"
reference="seceduccutoffs"} and [28](#seceducticks){reference-type="ref"
reference="seceducticks"} for the secondary education amenity, we find
that HDBSCAN and PAM show similar cutoffs for cluster 1, ranging from 0
to 0.0576 and 0 to 0.0557, respectively. Consequently, both approaches
exhibit similar numbers of DBs and population in
Figure [26](#seceducbarplot){reference-type="ref"
reference="seceducbarplot"} for this cluster. However, for the remaining
data, the cutoffs do not align. While HDBSCAN identifies two additional
clusters, PAM finds three clusters, and the cutoffs for these clusters
are different.

Examining the performance metrics in
Table [\[seceducvalid\]](#seceducvalid){reference-type="ref"
reference="seceducvalid"} for this amenity, the Silhouette coefficient
suggests that the MixAll method performs better in clustering. However,
the Dunn index and Calinski Harabasz index favor PAM, while the Davies
Bouldin index suggests MCLUST.

Based on this analysis, it suggests that cluster 1 for the secondary
education amenity should have a cutoff range of approximately 0 to
0.0557, as suggested by PAM. This suggestion is supported by the
validation from two metrics and is also consistent with HDBSCAN.
However, for the remaining data, there is no consensus among the
techniques regarding the cutoffs.

![Proportion of DBs and population in each cluster for all approaches
for the secondary education
amenity.](./barplot_comparison/Secondary Education_barplot.png){#seceducbarplot
width="\\textwidth"}

![Cut-offs values shown on the log-transformed density plots for all
clustering approaches for the secondary education
amenity.](./cutoffs/by_amenity/Secondary Education_cutoffs.png){#seceduccutoffs
width="\\textwidth"}

![Cutoff values compared for the secondary education amenity for all
clustering
approaches.](./cutoff_ticks/Secondary Education_ticks.png){#seceducticks
width="\\textwidth"}

## Library

Analyzing the summary statistics in
Table [\[libraryprofiles\]](#libraryprofiles){reference-type="ref"
reference="libraryprofiles"},
Figure [30](#librarycutoffs){reference-type="ref"
reference="librarycutoffs"} and [31](#libraryticks){reference-type="ref"
reference="libraryticks"} for the library amenity, we observe that
MixAll and PAM have similar cutoffs for the first cluster, ranging from
0 to 0.0993 and 0 to 0.0943, respectively. Additionally, both clustering
techniques suggest the presence of 2 clusters, indicating a similar
cutoff for cluster 2 as well. On the other hand, HDBSCAN identifies the
first cluster in the range of 0 to 0.0546, which aligns with MCLUST if
we combine the first three clusters of MCLUST with a cutoff range of 0
to 0.0538. The fourth cluster from MCLUST is similar to HDBSCAN if we
combine HDBSCAN's cluster 2 and 3. For the remaining data, HDBSCAN
identifies only one cluster, while MCLUST finds 3 additional clusters.
Apart from MixAll and PAM, none of the other techniques agree with each
other in terms of the number of clusters. Furthermore, the cutoffs are
not the same, although some of them may be similar by default or when
combining multiple clusters into one for comparison with other
techniques.

Upon examining the validation metrics in
Table [\[libraryvalid\]](#libraryvalid){reference-type="ref"
reference="libraryvalid"}, we find that the Silhouette coefficient, Dunn
index, and Davies Bouldin index suggest that the Minima identification
algorithm performs better in clustering this amenity, dividing the data
into 2 groups. However, the Calinski Harabasz index suggests that MixAll
performs better, also clustering the data into 2 groups, but with
significantly different cutoffs compared to the Minima identification
algorithm.

Based on this analysis, it suggests that the cutoff for the first
cluster may be around 0.0538, and the cutoff for the second cluster may
be near 0.0682, as both MCLUST and HDBSCAN find cutoffs in close
proximity to these values. The cutoff for the third cluster may be near
0.0993, as PAM, MCLUST, and MixAll identify cutoffs in the vicinity of
this value.

![Proportion of DBs and population in each cluster for all approaches
for the library
amenity.](./barplot_comparison/Library_barplot.png){#librarybarplot
width="\\textwidth"}

![Cut-offs values shown on the log-transformed density plots for all
clustering approaches for the library
amenity.](./cutoffs/by_amenity/Library_cutoffs.png){#librarycutoffs
width="\\textwidth"}

![Cutoff values compared for the library amenity for all clustering
approaches.](./cutoff_ticks/Library_ticks.png){#libraryticks
width="\\textwidth"}

## Parks

Examining Table [\[parksprofiles\]](#parksprofiles){reference-type="ref"
reference="parksprofiles"},
Figure [33](#parkscutoffs){reference-type="ref"
reference="parkscutoffs"} and [34](#parksticks){reference-type="ref"
reference="parksticks"} for the parks amenity, we observe that MixAll
and PAM have similar cutoffs for the first cluster, ranging from 0 to
0.0447 and 0 to 0.0450, respectively. Additionally, both techniques find
only 2 clusters, indicating a similar result for cluster 2 as well.
MCLUST also identifies a cutoff near this range, but it consists of 3
clusters within the 0 to 0.0463 range. MCLUST further finds 5 other
clusters for the remaining data. Apart from these findings, none of the
other cutoffs match across all the approaches for the park's amenity.
Figure [32](#parksbarplot){reference-type="ref"
reference="parksbarplot"} demonstrates that the number of DBs and DB
population aligns with these cutoff combinations.

Analyzing the validation metrics in
Table [\[parksvalid\]](#parksvalid){reference-type="ref"
reference="parksvalid"} for clustering techniques applied to parks, we
find that the Silhouette coefficient and Davies Bouldin index suggest
that PAM performs better in clustering this amenity, while the Dunn
index favors MixAll and the Calinski Harabasz index suggests MCLUST.

Based on this analysis, we can conclude that although none of these
methods agree exactly on the cutoffs, and the validation metrics also do
not unanimously support one technique, the first cluster cutoff may be
around 0.0183, as three techniques (Minima identification, HDBSCAN, and
MCLUST) find cutoffs near this value. The second cluster cutoff may be
around 0.0450, as MixAll, MCLUST, and PAM identify a cutoff point close
to this value, MixAll and PAM supported by the validation metrics. The
remaining data may belong to a single cluster, as suggested by MixAll
and PAM.

![Proportion of DBs and population in each cluster for all approaches
for the parks
amenity.](./barplot_comparison/Parks_barplot.png){#parksbarplot
width="\\textwidth"}

![Cut-offs values shown on the log-transformed density plots for all
clustering approaches for the parks
amenity.](./cutoffs/by_amenity/Parks_cutoffs.png){#parkscutoffs
width="\\textwidth"}

![Cutoff values compared for the parks amenity for all clustering
approaches.](./cutoff_ticks/Parks_ticks.png){#parksticks
width="\\textwidth"}

## Transit

Examining
Table [\[transitprofiles\]](#transitprofiles){reference-type="ref"
reference="transitprofiles"},
Figure [36](#transitcutoffs){reference-type="ref"
reference="transitcutoffs"} and [37](#transitticks){reference-type="ref"
reference="transitticks"} for the transit amenity, we observe that
although the number of clusters matches in HDBSCAN, MixAll, and PAM,
none of the cutoffs align across all these clustering techniques. This
trend is also reflected in the number of DBs and DB population, as shown
in Figure [35](#transitbarplot){reference-type="ref"
reference="transitbarplot"}. While the combination of the first two
clusters from the quintile method matches the cutoff for the first
cluster in MixAll, we should not consider it since the quintile method
does not determine cutoffs based on the underlying data.

Analyzing the validation metrics in
Table [\[transitvalid\]](#transitvalid){reference-type="ref"
reference="transitvalid"} for clustering techniques applied to transit,
we find that MCLUST performs better in clustering the transit amenity,
as suggested by the Calinski Harabasz and Davies Bouldin indices.
However, the Dunn index favors MixAll, and the Silhouette index suggests
Minima identification as the better performers.

Based on this analysis, it is evident that different clustering
techniques yield different cutoffs, and the validation metrics also
suggest different techniques without any common cutoffs. Therefore, it
is not possible to emphasize any particular cutoffs for clustering in
this case.

![Proportion of DBs and population in each cluster for all approaches
for the transit
amenity.](./barplot_comparison/Transit_barplot.png){#transitbarplot
width="\\textwidth"}

![Cut-offs values shown on the log-transformed density plots for all
clustering approaches for the transit
amenity.](./cutoffs/by_amenity/Transit_cutoffs.png){#transitcutoffs
width="\\textwidth"}

![Cutoff values compared for the transit amenity for all clustering
approaches.](./cutoff_ticks/Transit_ticks.png){#transitticks
width="\\textwidth"}

# Discussion

The most significant takeaway from the current investigation is the lack
of clear-cut segments in the early release of the PMD. While it is true
that log-transforming the proximity measures did reveal certain
density-sparse regions, the clustering algorithms utilized were not able
to consistently identify these regions. As a result, we observed a lack
of stability in the clustering results. This is also reflected by the
lack of consensus suggested by the cluster validation metrics.
Certainly, this does not invalidate the ability of the PMD to accurately
judge proximity to amenities; rather, it suggests that proximity to
amenities in Canada is a relatively smooth gradient without any obvious
clusters.

Not only were results inconsistent between approaches for the same
amenity, but results between amenities using the same algorithm were not
always comparable. For example, the PAM algorithm consistently found a
very low number of clusters, except for the grocery amenity, for which
it found many more. The MCLUST algorithm demonstrates a similar
inconsistency: for the transit amenity it only finds three clusters, but
for the employment amenity it finds nine. There are two explanations for
this behaviour. The first is that these inconsistencies are due to the
same underlying problem that causes inconsistencies between algorithms
for the same amenity: namely that the data is not particularly
clusterable. Therefore, the algorithms are dividing the measures
somewhat arbitrarily at chance fluctuations. The second reason is that
the 'true' number of clusters likely differs significantly between
amenities. Therefore, the number and type of clusters for one amenity
would not be expected to appear similar to another amenity. In other
words, this explanation suggests that just because a DB can be easily
classified as either low or high access to amenity A, this does not mean
that this same DB can be easily classified into one of only two
categories for amenity B. Instead, one amenity may be distributed very
simply, while others may be distributed in a more complex manner.

The current investigation is an informative first glance into the
clusterability of the early release of the PMD. We were able to attempt
many different clustering algorithms, which reinforces our finding that
PMD segments are not robust and reproducible, but are instead sensitive
to a variety of factors. This broad scope of approaches will help to
guide and refine the endeavors of future researchers. While we did take
extensive care to ensure the validity and reproducibility of our
results, we were constrained in some aspects of our methodology. The
most major concern is that of computational constraints. Due to the
complexity of several of the algorithms we implemented, subsampling was
required in order to avoid running out memory. 3% subsampling was most
commonly used. In the future, researchers not subjected to similar
computational restraints should seek to run their algorithms on the
entire dataset, rather than a subsample. Additionally, it is worth
noting that since the PMD was only recently released as "experimental
statistics", it is possible that better, more comprehensive ways of
calculating the proximity index using additional/different data sources
may be developed in the future, which may render our methodology
obsolete.

There are many other potential avenues for future research in the
clustering of the PMD. These include: setting the number of clusters to
be the same between all algorithms, trying different combinations of
variables in multidimensional clustering (as opposed to clustering only
on the proximity measure in question), trying additional clustering
algorithms, clustering on different data transformations, attempting
sub-clustering (ie. some way of dealing with outliers aside from
selective models), as well as soft assignments (i.e., using overlapping
ranges where the cut-off is not a single point but, ideally, a narrow
continuous interval).

# Conclusion

The current project aimed to explore segmentation of continuous
proximity measures in the Proximity Measure Database (PMD) developed by
Statistics Canada. The goal was to create intuitive and understandable
categorical measures for amenities, which could inform decision making
processes for policymakers and urban planners. By categorizing the
proximity measures, it becomes easier to prioritize efforts in enhancing
access and promoting social and economic sustainability within
communities.

The project employed various clustering methods, including minima
identification, HDBSCAN, MixAll, MCLUST, and PAM algorithms to determine
optimal cutoff values and cluster boundaries for each amenity.
Additionally, cluster validation metrics such as the Silhouette
coefficient, Dunn index, Calinski-Harabasz, and Davies-Bouldin were used
to evaluate the performance of each clustering technique and determine
the appropriate number of clusters.

The results showed that the PMD had a low clustering tendency, even
after log-transformation. Clustering techniques produced diverse
outcomes, and there was no single algorithm that consistently
outperformed others. The overall lack of consistency serves to
demonstrate the lack of obvious clusters within the proximity measures
of the PMD.

Although there was some overlap between algorithms, cluster profiling
revealed that the clusters identified by different algorithms were
mostly distinct. One common trend that held true for the majority of
clusters was that as amenity proximity increases, median IoR decreases,
population increases, percentage of CMA DBs increases, and the
percentage of low amenity dense DBs decreases.

Overall, this project explored a variety of clustering methods in
segmenting continuous proximity measures and generating meaningful
categorical measures. In light of our original research goal to find the
optimal cut-off values and cluster boundaries, these findings were not
conclusive. The overall lack of clustering consistency and distinct
characteristics of clusters identified by different algorithms within
this limited data underscore the need for further refinement and
exploration. We theorize that an "exhaustive" PMD which is not limited
by travel radii will have more identifiable groups, and so the methods
outlined in this report will be useful to determine the clusters. Future
research can build upon these findings to refine the clustering
techniques and explore additional factors that contribute to the
definition of clusters in the PMD.

# References

**1** Alasia, A., Bédard, F., Bélanger, J., Guimond, E., & Penney, C.
(2017). *Measuring remoteness and accessibility: A set of indices for
Canadian communities.* Reports on Special Business Projects, Statistics
Canada.
<https://www150.statcan.gc.ca/n1/pub/18-001-x/18-001-x2017002-eng.htm>.\
**2** Alasia, A., Newstead, N., Kuchar, J., & Radulescu, M. (2021,
February 15). *Measuring Proximity to Services and Amenities: An
Experimental Set of Indicators for Neighbourhoods and Localities*.
Reports on Special Business Projects, Statistics Canada. Retrieved May
4, 2023, from
<https://www150.statcan.gc.ca/n1/pub/18-001-x/18-001-x2020001-eng.htm>.\
**3** Bernard, D. (2018). Clustering Indices.
<https://cran.r-hub.io/web/packages/clusterCrit/clusterCrit.pdf> 1.2.7.\
**4** Caliński, T., & Harabasz, J. (1974). *A Dendrite Method for
Cluster Analysis*. Communications in Statistics-theory and Methods 3:
1-27. doi:[10.1080/03610927408827101](10.1080/03610927408827101){.uri}.\
**5** De Smith, M. J., Goodchild, M. F., Longley, P. A., & Colleagues.
(2021). *Geospatial Analysis* 6th Edition, 2021 update. Retrieved June
12, 2023, from <https://www.spatialanalysisonline.com/HTML/index.html>.\
**6** Data Exploration and Integration Lab (DEIL), Statistics Canada
(2023). *Index of Remoteness 2021: Update with 2021 census geographies
and populations*.
<https://www150.statcan.gc.ca/n1/pub/17-26-0001/2020001/meta-doc-eng.htm>.\
**7** Davies, D.L. & Bouldin, D.W. (1979). *A Cluster Separation
Measure*. IEEE Transactions on Pattern Analysis and Machine
Intelligence. PAMI-1 (2): 224--227.
doi:[10.1109/TPAMI.1979.4766909](10.1109/TPAMI.1979.4766909){.uri}.\
**8** Dunn, J. C. (1974). *Well-Separated Clusters and Optimal Fuzzy
Partitions*. Journal of Cybernetics. 4 (1): 95--104.
doi:[10.1080/01969727408546059](10.1080/01969727408546059){.uri}.\
**9** Hashmi, F. (2021, November 27). *Data Science Interview Questions
for IT Industry Part-4: Unsupervised ML - Thinking Neuron*. Thinking
Neuron.
<https://thinkingneuron.com/data-science-interview-questions-for-it-industry-part-4-unsupervised-ml/#DBSCAN>.\
**10** Hahsler, M., Piekenbrock, M., & Doran, D. (2019). *dbscan: Fast
Density-Based Clustering with R*. Journal of Statistical Software,
91(1), <https://doi.org/10.18637/jss.v091.i01>.\
**11** Iovleff, S. (2019, September 12). *MixAll: Clustering Mixed data
with Missing Values*. Retrieved June 12, 2023, from
<https://cran.r-project.org/web/packages/MixAll/vignettes/Introduction-Mixtures.pdf>.\
**12** *Jenks Natural Breaks Classification* - GIS Wiki \| The GIS
Encyclopedia (2018). Retrieved June 12, 2023, from
<http://wiki.gis.com/wiki/index.php/Jenks_Natural_Breaks_Classification>.\
**13** Kassambara, A. (2017). *Practical Guide to Cluster Analysis in R:
Unsupervised Machine Learning*. STHDA.\
**14** Kassambara, A. (2018). *K-Medoids in R: Algorithm and Practical
Examples*. Retrieved June 12, 2023, from
<https://www.datanovia.com/en/lessons/k-medoids-in-r-algorithm-and-practical-examples/>.\
**15** Kassambara A, Mundt F (2020). factoextra: Extract and Visualize
the Results of Multivariate Data Analyses. R package version 1.0.7,
<https://CRAN.R-project.org/package=factoextra>.\
**16** Kenton, W. (2023). *Kurtosis Definition, Types, and Importance*.
Investopedia. <https://www.investopedia.com/terms/k/kurtosis.asp>.\
**17** MacQueen, J. B. (1967). *Some Methods for classification and
Analysis of Multivariate Observations*. Proceedings of 5th Berkeley
Symposium on Mathematical Statistics and Probability. Vol. 1. University
of California Press. pp. 281--297.\
**18** Marbac, M. M., & Sedki, M. S. (2017). *Variable Selection for
Model-Based Clustering of Continuous, Count, Categorical or Mixed-Type
Data Set with Missing Values* \[Software\]. In CRAN (2.0.1).
[ http://cran.nexr.com/web/packages/VarSelLCM/]( http://cran.nexr.com/web/packages/VarSelLCM/){.uri}.\
**19** OECD, Statistics Canada. (2018). *Workshop on Modernising
Statistical Systems for Better Data on Regions and Cities*. Retrieved
May 4, 2023, from
<https://www.oecd.org/cfe/regionaldevelopment/modernising-statistical-systems.htm>.\
**20** Rousseeuw, P.J. (1987) *Silhouettes: A graphical aid to the
interpretation and validation of cluster analysis*. Journal of
Computational and Applied Mathematics, Volume 20, Pages 53-65,ISSN
0377-0427. <https://doi.org/10.1016/0377-0427(87)90125-7>.\
**21** Scrucca, L., Fop, M., Murphy, T. B., & Raftery, A. E. (2016).
*MCLUST 5: clustering, classification, and density estimation using
Gaussian finite mixture models*. The R Journal, 8(1), 289-317.
<https://doi.org/10.32614/RJ-2016-021>.\
**22** Statistics Canada (2020a). *Proximity Measures Data Viewer*.
<https://www150.statcan.gc.ca/n1/pub/71-607-x/71-607-x2020011-eng.htm>.\
**23** Statistics Canada (2020b). *Proximity Measures Database -- Early
release*.
<https://www150.statcan.gc.ca/n1/pub/17-26-0002/172600022020001-eng.htm>.\
**24** Statistics Canada. (2021). *Dictionary, Census of Population,
2021 Dissemination block (DB)*.
<https://www12.statcan.gc.ca/census-recensement/2021/ref/dict/az/definition-eng.cfm>.\
**25** Subedi,R., Roshanafshar, S., & Greenberg, T.L. (2020).
*Developing Meaningful Categories for Distinguishing Levels of
Remoteness in Canada*. Analytical Studies: Methods and References,
Statistics Canada.
<https://www150.statcan.gc.ca/n1/pub/11-633-x/11-633-x2020002-eng.htm>.\
**26** Wickham, H., Averick, M., Bryan, J., Chang, W. W., et al. (2019).
Welcome to the Tidyverse. Journal of Open Source Software, 4(43), 1686.
<https://doi.org/10.21105/joss.01686>.\

# Appendix

## Successful Methods {#appendix:successful}

### PAM (Partitioning Around Medoids - PAM)

K-means is a clustering algorithm that aims to partition a dataset into
K clusters, where each data point belongs to the group with the closest
mean. The Partitioning Around Medoids (PAM) variation replaces the
concept of mean with medoids to handle noise and outliers more
effectively (Kaufman and Rousseeuw 1990).

The PAM algorithm, an evolution of the K-means clustering method,
operates by selecting K representative objects, or medoids, among the
observations of the dataset. These medoids are the most centrally
located data points in a cluster, which means the average dissimilarity
between a medoid and all other objects within the same cluster is
minimized. In contrast to the K-means algorithm, which uses means as
cluster centers, PAM's utilization of medoids makes it a robust
alternative, less sensitive to noise and outliers.

The PAM algorithm works in two phases: the 'build phase' and the 'swap
phase'. During the build phase, K objects are selected to be the
medoids, the dissimilarity matrix is calculated, and every object is
assigned to its closest medoid. The swap phase attempts to improve the
clustering quality by exchanging selected objects (medoids) and
non-selected objects. If the sum of the dissimilarities of all objects
to their nearest medoid (the objective function) can be reduced by this
swapping, then the swap is carried out. The process continues until the
objective function can no longer be decreased, resulting in a set of K
representative objects which minimize the sum of the dissimilarities of
the observations to their nearest representative object (Kaufman and
Rousseeuw 1990).

Since PAM is an extension of the K-means algorithm, it operates under
similar assumptions but with additional robustness due to the use of
medoids. The following are the fundamental assumptions it makes about
the data:

-   Globular clusters: It assumes that the natural grouping of data
    forms globular or spherical clusters. This assumption helps separate
    clusters effectively when the algorithm operates on the data
    (Perceptive Analytics, 2017).

-   Clusters of similar size: The algorithm works under the assumption
    that clusters contain approximately the same number of data points.
    It determines the boundaries of the cluster based on this assumption
    (Perceptive Analytics, 2017).

-   Distance Measures: The algorithm employs distance measures, such as
    Euclidean distance, to compute similarity. This assumes that
    'straight-line' distance is the appropriate measure of similarity,
    which may not hold true in all contexts (Perceptive Analytics, 2017)

We selected the PAM algorithm for its robustness to outliers, an
attribute particularly beneficial given the nature of our dataset that
comprises 10 distinct amenities. Emphasizing a univariate approach, we
individually clustered each amenity to preserve their unique
characteristics and to align with the algorithm's cluster homogeneity
assumption. Although our proximity data was already normalized between 0
and 1, we further refined the distribution of each amenity through log
transformation. This transformation was not a direct requirement of the
algorithm, but it was implemented to create more normally distributed
data and reduce outliers.

### Gaussian Mixture Models (MCLUST)

MCLUST is an R package that provides a comprehensive approach to finite
mixture models, providing functions for model-based clustering,
classification, and density estimation based on Gaussian Mixture Models
(GMMs). GMMs are probabilistic models assuming that the data points in a
given dataset are generated from a mixture of Gaussian distributions,
with each Gaussian component representing a distinct cluster (Scrucca et
al., 2016).

MCLUST uses the Expectation-Maximization (EM) algorithm for estimating
the parameters. The EM algorithm operates iteratively in two steps:

1.  Expectation (E) Step: Expected values of the component memberships
    are calculated based on the current parameters.

2.  Maximization (M) Step: The log-likelihood function is maximized to
    update the parameter estimates based on these expected values.

The process is repeated until convergence, providing the parameter
estimates for the mixture model. Furthermore, MCLUST automatically
computes and selects the best model as per the Bayesian Information
Criterion (BIC), considering different numbers of clusters and different
parameterizations of the covariance matrix (Scrucca et al., 2016).

The Gaussian Mixture Models (MCLUST) operate on several assumptions.
Firstly, MCLUST is formulated on the belief that the data is generated
from a mixture of Gaussian distributions. This assumption provides a
statistical framework that guides how the algorithm processes the
dataset (Scrucca et al., 2016).

Another key presumption is that the variables within each component are
normally distributed and independent. This is a common assumption in
many statistical techniques and it impacts how the algorithm assesses
relationships within the data.

Lastly, MCLUST relies on maximum likelihood estimation, which is
influenced by initial values and can potentially converge to local,
instead of global, maxima. This characteristic points to the algorithm's
optimization strategy and its approach to finding the most probable
parameters for the Gaussian distributions (Scrucca et al., 2016).

Gaussian Mixture Models (MCLUST) proved to be an effective choice for
our project due to its robustness and flexibility in handling
model-based clustering. With our dataset's characteristics - univariate
proximity measures for ten different amenities, the capability of MCLUST
to handle different Gaussian components was an instrumental feature for
identifying unique clusters.

Prior to implementing MCLUST, we took strategic steps in our data
preprocessing, such as applying appropriate transformations when
necessary. While it's important to clarify that these transformations
weren't specifically carried out for MCLUST, they naturally helped our
data to align more closely with the Gaussian distribution, an assumption
inherent in the model. This approach enhanced the performance potential
of the algorithm, making it a more suitable fit for our data.

Another particularly appealing feature of MCLUST was its ability to
autonomously compute the optimal model, taking into account varying
numbers of clusters and different configurations of the covariance
matrix. This made the algorithm more robust and efficient in managing
the complexities inherent in our dataset, consequently improving the
overall quality of the clustering results.

### MixAll

MixAll is a clustering model that functions on the premise of mixture
models. These models assume that data is generated from a combination of
probability distributions, which is ideal for handling datasets with
diverse distributions or missing values.

The MixAll model is basically a mixture model. Mixture models assume
data is generated from a combination of probability distributions.
Parameter estimation is achieved by maximizing the observed
log-likelihood or integrated log-likelihood for data with missing
values. Estimation algorithms like expectation-maximization (EM), SEM,
and CEM are used and the default is EM which is highlighted below,
involving steps such as imputation, conditional prob- ability
calculation, and parameter updates. The EM algorithm iteratively
performs these steps until convergence (Iovleff, 2019).

The EM algorithm consists of several iterative steps:

1.  I step: Impute the missing values $x^{m}_{i}$ using the current MAP
    value provided by the current parameter $\theta^{m-1}$.

2.  E step: Compute the current conditional probabilities $t^{m}_{ik}$
    for $i = 1, \ldots, n$ and $k = 1, \ldots, K$ using the current
    parameter $\theta^{m-1}$.

3.  M step: Update the maximum likelihood estimate $\theta^{m}$ of
    $\theta$ using the conditional probabilities $t^{m}_{ik}$ as
    conditional mixing weights, aiming to maximize the log-likelihood
    function, where
    $t^{m} = (t^{m}_{ik}, i = 1, \ldots, n, k = 1, \ldots, K)$.

4.  Parameter update: The updated expression of mixture proportions
    $p^{m}_{k}$ for $k = 1, \ldots, K$ are computed. Detailed formulas
    for updating the parameters $\lambda_{k}$ and $\alpha$ depend on the
    component parameterization (Iovleff, 2019).

It's important to note that the notation and steps described above are
derived from the article "MixAll: Clustering Mixed data with Missing
Values" by Serge Iovleff.

The MixAll algorithm operates based on several assumptions that could
influence the implementation and results of the model. One such
assumption pertains to the use of the `clusterDiagGaussian` function.
This function is designed to work with multivariate data, treating each
variable as independent during the clustering process. Given that our
data is univariate, this aspect of the algorithm may offer results
unique to our dataset.

Another assumption built into MixAll is that the data arises from a
Gaussian mixture. This suggests that the model expects the underlying
distribution of the data to resemble a blend of Gaussian distributions.
Lastly, a third assumption pertains to the standard deviations within
each component of the model, which the algorithm anticipates to be
varied (Iovleff, 2019).

Initially, we chose to employ the MixAll algorithm for its capacity to
effectively deal with missing data. However, this motivation was short
lived as we shifted our attention to clustering in the univariate case.
Furthermore, similar to MCLUST, MixAll's adeptness in handling a diverse
range of distributions added to its appeal for our project.

The algorithm's assumption of data arising from a Gaussian mixture
aligns well with the preprocessing measures we adopted for our data.
Specifically, as previously stated, we applied a log transformation to
our initially right-skewed data to achieve a distribution that more
closely approximates a Gaussian one. This transformation assisted in
leveraging MixAll's inherent strength in managing datasets with varied
distributions, thereby enhancing the effectiveness of the clustering
analysis.

### Hierarchical Denisity-Based Spatial Clustering of Applications with Noise (HDBSCAN)

Hierarchical Density-Based Spatial Clustering of Applications with Noise
(HDBSCAN) is a flexible clustering algorithm that extends DBSCAN by
converting it into a hierarchical clustering algorithm. The
density-based algorithm can find clusters of varying densities and is
designed to be more flexible than some of the other more prominent
clustering techniques. This feature allows it to recognize and work with
clusters of varying densities, adding to its versatility and
applicability across diverse datasets (McInnes, Healy, & Astels, 2016).

HDBSCAN works on the concept of density-based clustering (DBSCAN) but
goes a step further by introducing hierarchy, allowing it to discover
clusters of varying densities. This algorithm operates in two main
steps:

1.  Transform the space according to the density/sparsity. This
    transformation ensures that sparse areas are more distant. It
    utilizes the core distance (defined by parameter MinPts) and mutual
    reachability distance to create an undirected weighted graph, and
    then applies the single-linkage clustering to the graph (Campello et
    al., 2015).

2.  Create a hierarchy of clusters. The hierarchy produced by
    single-linkage clustering is then simplified by transforming it into
    a tree, which is then condensed by pruning branches not representing
    a cluster. The pruning process is guided by the stability of
    clusters, which is computed based on their persistence over the
    distance (Campello et al., 2015).

HDBSCAN, like other density-based clustering algorithms, assumes that
clusters are dense regions in the data space, separated by regions of
lower density. It does not require the clusters to be of a particular
geometric shape, making it versatile for different datasets. However, it
does expect the density within clusters to be relatively uniform, and it
may struggle with clusters of widely varying densities. It also assumes
that noise is present in the data, which it will not include in
clusters, instead treating it as 'background noise' (Campello et al.,
2015).

HDBSCAN was chosen because of its ability to detect clusters of varying
densities, offering flexibility that aligned with the nature of our
data. Additionally, HDBSCAN's assumption of density-based clusters
proved suitable for our project, particularly because the proximity
measures of the amenities in our dataset naturally lent themselves to
such a density-based analysis, as our goal was to detect density sparse
regions. Lastly, and probably the most enticing reason was the
algorithm's tendency to handle noise. The algorithm helped ensure a
robust clustering output, accommodating for potential outliers that were
present in the data.

### Multivariate - ClustImpute

ClustImpute algorithm on multi-dimensional, log-scaled proximity
measures. Other variables used for this clustering along with the one
amenity at a time include:

-   "CSD_AREA"

-   "PMS_CSDPOP"

-   "PMS_DBPOP"

-   "IOR_Index_of_remoteness"

These variables were scaled from 0-1 prior to clustering. This algorithm
"draws the missing values iteratively based on the current cluster
assignment so that correlations are considered on this level". Also,
"penalizing weights are imposed on imputed values and successively
decreased (to zero) as the missing data imputation gets better". The
idea is that the missing value is imputed by those other observations
that are more similar to it (ie. in the same cluster).

Algorithm Steps:

1.  It replaces all NAs by random imputation, i.e., for each variable
    with missings, it draws from the marginal distribution of this
    variable not taking into account any correlations with other
    variables

2.  Weights $<$ 1 are used to adjust the scale of an observation that
    was generated in step 1. The weights are calculated by a (linear)
    weight function that starts near zero and converges to 1 at n_end.

3.  A k-medioids clustering is performed with a number of c_steps steps
    starting with a random initialization.

4.  The values from step 2 are replaced by new draws conditionally on
    the assigned cluster from step 3.

5.  Steps 2-4 are repeated nr_iter times in total. The k-medioids
    clustering in step 3 uses the previous cluster centroids for
    initialization.

6.  After the last draws a final k-medioids clustering is performed.

### Multivariate - VarSelLCM

The varselLCM (Variable Selection in Latent Class Models) clustering
algorithm is a method that combines latent class modeling with variable
selection techniques to identify meaningful clusters in data (Marbac &
Sedki, 2017). This method has been applied on all the amenity proximity
measures together.

Due to the significant presence of NA values in the dataset, it is
necessary to utilize an algorithm that can cluster the data without the
need for imputing these NA values. Imputing the NA values in this case
could have a substantial impact on the resulting clusters.

Moreover, it is not feasible to simply remove the NA values from all
columns in the dataset. This approach would lead to a significant
reduction in the amount of available data. Additionally, the presence of
missing values in one column can affect the available values in other
columns, making it impractical to remove NA values indiscriminately from
the dataset.

1.  Data Preparation: The algorithm takes as input a dataset consisting
    of categorical variables. It is assumed that the data is generated
    from an underlying latent class structure, where each observation
    belongs to a specific latent class.

2.  Model Initialization: The algorithm begins by randomly assigning
    observations to different latent classes. It initializes the model
    parameters, including the class probabilities and the conditional
    probabilities of each variable within each class.

3.  Expectation-Maximization (EM) Algorithm: The varselLCM algorithm
    employs an iterative process based on the EM algorithm. In the
    expectation step (E-step), the algorithm calculates the probability
    of each observation belonging to each class based on the current
    model parameters.

4.  Variable Selection: In the maximization step (M-step), the algorithm
    selects a subset of relevant variables that contribute to the
    clustering process. It employs a variable selection criterion, such
    as the Bayesian Information Criterion (BIC), to identify the most
    informative variables for clustering.

5.  Model Update: Once the relevant variables are selected, the
    algorithm updates the model parameters based on the observed data
    and the selected variables. It estimates the class probabilities and
    the conditional probabilities of the selected variables within each
    class.

6.  Iterative Process: Steps 3-5 are repeated iteratively until
    convergence is achieved. The algorithm continues updating the model
    parameters and selecting variables until the clustering solution
    stabilizes.

7.  Final Clustering Solution: Once convergence is reached, the
    algorithm assigns each observation to the latent class with the
    highest probability. The resulting clustering solution represents a
    partitioning of the data into distinct clusters based on the
    selected variables and their associated probabilities within each
    class (Marbac & Sedki, 2017).

Initially, VarselLCM was utilized for multivariate clustering. However,
upon observing distinct cluster patterns in the data through log
transformation, the focus shifted towards univariate clustering.
Unfortunately, attempts to apply VarselLCM for univariate clustering
were unsuccessful as it did not converge. Consequently, it was not
possible to proceed with the technique.

## Unsuccessful Methods {#appendix:unsuccessful}

### OPTICS

OPTICS stands for Ordering Points To Identify Clustering Structure. This
algorithm can be seen as a generalization of DBSCAN. A major issue with
DBSCAN is that it fails to find clusters of varying density due to fixed
$\epsilon$. This is solved in OPTICS by using an approach of finding
reachability of each point from the core points and then deciding the
clusters based on reachability plot (Hashmi, 2021).

Considering the log-transformed data, we observed multiple peaks and
troughs, suggesting that the clusters may have varying densities.
Therefore, aim to explore the applicability of OPTICS, a clustering
technique adept at accommodating varying densities (Hahsler et al.,
2019). Also there were a decent amount of outliers in the proximity
measures which OPTICS can handle (2.3. Clustering, n.d.).

Relevant terminologies for OPTICS:

-   $\epsilon$, epsilon (eps): is the Maximum distance between to points
    that can be considered to form a group/cluster.

-   MinPts: is the minimum number of points that must be present near
    each other within the epsilon ($\epsilon$) range in order for them
    to all form a group or cluster.

-   Core Point: A point in the data that has at least MinPts number of
    points nearby within the eps ($\epsilon$) range.

-   Border Point/Non-Core Point: A border point or non-core point is a
    data point in which there are fewer than the minimum number of
    points (MinPts) within reach of it (at a distance of eps).

-   Noise: A noise point is a data point in which there isn't a single
    point within eps of it.

-   Core Distance: Core distance can be less than the predetermined
    value of, epsilon ($\epsilon$), which is the maximum allowed
    distance to find MinPts. Core distance denotes the min- imum
    distance needed for a point to become a core point and denotes that
    the MinPts number of points can be found within this distance.

-   Reachability distance: Reachability Distance is the minimum distance
    from the cluster's extreme point if the point is outside the core
    distance, and the core distance is the distance necessary to reach
    the point from the cluster if it is inside the core distance
    (Hashmi, 2021).

Algorithm Steps:

1.  For the given values of MinPts and eps ($\epsilon$), find out if a
    point is close to MinPts number of points within a distance less
    than or equal to eps. Tag it as a Core Point. Update the
    reachability distance = core distance for all the points within the
    cluster.

2.  If it is not a core point then find out its density connected
    distance from the nearest cluster. Update the reachability distance.

3.  Arrange the data in increasing order of reachability distance for
    each cluster. The smallest distances come first and represent the
    dense sections of data and the largest distances come next
    representing the noise section. This is a special type of
    dendrogram.

4.  Find out the places where a sharp decline is happening in the
    reachability distance plot.

5.  "Cut" the plot in the y-axis by a suitable distance to get the
    clusters (Hashmi, 2021).

The clustering process was applied solely to the employment variable
without considering any supplementary explanatory variables. The
resulting clusters overlap and intersect with other clusters. This
overlapping and intersecting nature is not suitable for creating
distinct profiles. For this reason, the decision was made not to
continue with this technique.

### Jenks Natural Break Classification

The Jenks Natural Breaks Classification (or Optimization) system is a
data classification method designed to optimize the arrangement of a set
of values into "natural" classes. A Natural class is the most optimal
class range found "naturally" in a data set. Natural breaks are
determined with a frequency histogram. Class boundaries are identified
as troughs in the data. Many dataset will not have obvious natural
breaks which means that this method would tend to show breaks where none
really exists (Jenks Natural Breaks Classification - GIS Wiki - the GIS
Encyclopedia, 2018.)

By attempting to minimize the average deviation of each class from the
class mean while maximizing the average deviation of each class from the
means of the other classes, the Jenks Natural Breaks Classification
method attempts to reduce the variance within classes while enhancing
the variance between classes (Wikipedia contributors, 2023).

Jenks Natural Breaks is chosen for application due to the limitation of
proximity measures in representing data distribution, specifically when
the distribution is not normal. Jenks Natural Breaks, being a
non-parametric method, does not assume any specific data distribution
and can be applied to a wide range of data types and distributions. This
makes it a suitable choice in cases where the proximity measures'
distribution deviates from normality. By considering the inherent
characteristics of the data, Jenks Natural Breaks can identify natural
groupings based on the actual data distribution, enhancing the
clustering results. (Geospatial Analysis 6th Edition, 2021 Update - De
Smith, Goodchild, Longley and Colleagues, 2021)

Algorithm Steps:

1.  The user selects the attribute, x, to be classified and specifies
    the number of classes required, k.

2.  A set of k‑1 random or uniform values are generated in the range
    \[min{x},max{x}\]. These are used as initial class boundaries.

3.  The mean values for each initial class are computed and the sum of
    squared deviations of class members from the mean values is
    computed. The total sum of squared deviations (TSSD) is recorded

4.  Individual values in each class are then systematically assigned to
    adjacent classes by adjusting the class boundaries to see if the
    TSSD can be reduced. This is an iterative process, which ends when
    improvement in TSSD falls below a threshold level, i.e. when the
    within class variance is as small as possible and between class
    variance is as large as possible. True optimization is not assured.
    The entire process can be optionally repeated from Step 1 or 2 and
    TSSD values compared (Geospatial Analysis 6th Edition, 2021 Update -
    De Smith, Goodchild, Longley and Colleagues, 2021).

The results of the Jenks Natural Break classification are not useful for
several reasons. Firstly, when considering employment and childcare,
there were variations identified. However, for other amenities, the
algorithm consistently suggested 2 or 3 clusters. The problem arises
when we observe that the natural breaks for these clusters are within a
very narrow range. For example, the first cluster has a range from 0 to
0.0095, and the second cluster has a range from 0.0095 to 0.7452. The
remaining data points above this range are grouped into the third
cluster. When plotting these clusters on a kernel density plot, we
observe that only one cluster is visible. This is because the ranges for
the other two clusters are so small that they cannot be effectively
visualized. This lack of visibility hinders the usefulness of the
classification results. Moreover, these findings are not helpful for
profiling purposes as they ignore the variations in the larger range.
Focusing solely on the narrow ranges of the clusters neglects the
valuable information and differences present in the broader range of
data points.

## Extra Plots and Tables {#extra}

![Boxplots showing outliers for all ten amenities of the
PMD.](./outliers/boxplot.png){#boxoutliers width="\\textwidth"}

![ Boxplots showing outliers for all ten log-transformed amenities of
the PMD.](./outliers/logged_boxplot.png){#logboxoutliers
width="\\textwidth"}

![Density distributions for all ten amenities of the
PMD.](./distributions/distributions.png){#dendist width="\\textwidth"}

![ Log-transformed density distributions for all ten amenities of the
PMD.](./distributions/log_distributions.png){#logdendist
width="\\textwidth"}

![Sort plots for each amenity in the PMD.
](./sort_plot/sort_plot.png){#sortplots width="\\textwidth"}

![Log-transformed sort plots for each amenity in the PMD.
](./sort_plot/log_sort_plot.png){#logsortplots width="\\textwidth"}


$$

