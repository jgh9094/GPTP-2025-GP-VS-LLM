# responsibe for generating all figures for holdout approach

rm(list = ls())
setwd('~/Desktop/Repositories/GPTP-2025-LLM-VS-GP/')
cat("\014")

library(ggplot2)
library(cowplot)
library(dplyr)

# vars needed
data_dir <- './psb2_similarity.csv'
conditions <- c('PushGP', 'GPT-4o (D)','GPT-4o (D-T)','GPT-4o (T)')

all_data <- read.csv(data_dir, header = TRUE, stringsAsFactors = FALSE)
all_data$synthesizer <- factor(all_data$synthesizer, levels = conditions)
all_data <- filter(all_data, synthesizer != 'PushGP')

# 200 cases stats
data <- filter(all_data, case == 200)

# k_2
kruskal.test(k_2 ~ synthesizer, data = data)
pairwise.wilcox.test(x = data$k_2, g = data$synthesizer, p.adjust.method = "bonferroni",
                     paired = FALSE, conf.int = FALSE, alternative = 't')

# k_5
kruskal.test(k_5 ~ synthesizer, data = data)
pairwise.wilcox.test(x = data$k_5, g = data$synthesizer, p.adjust.method = "bonferroni",
                     paired = FALSE, conf.int = FALSE, alternative = 't')

# k_10
kruskal.test(k_10 ~ synthesizer, data = data)
pairwise.wilcox.test(x = data$k_10, g = data$synthesizer, p.adjust.method = "bonferroni",
                     paired = FALSE, conf.int = FALSE, alternative = 't')

# 50 cases stats
data <- filter(all_data, case == 50)

# k_2
kruskal.test(k_2 ~ synthesizer, data = data)

# k_5
kruskal.test(k_5 ~ synthesizer, data = data)

# k_10
kruskal.test(k_10 ~ synthesizer, data = data)