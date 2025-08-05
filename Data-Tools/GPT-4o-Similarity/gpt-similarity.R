# responsibe for generating all figures for holdout approach

rm(list = ls())
setwd('~/Desktop/Repositories/GPTP-2025-LLM-VS-GP/')
cat("\014")

library(ggplot2)
library(cowplot)
library(dplyr)
library(PupillometryR)
library(ggpubr)
library(tidyr)

SHAPE <- c(21, 21, 21, 21)
cb_palette <- c('#D81B60', '#1E88E5', '#FFC107', '#004D40')
TSIZE <- 17
REPLICATES <- 30
data_dir <- './psb2_similarity.csv'
conditions <- c('PushGP', 'GPT-4o (D)','GPT-4o (D-T)','GPT-4o (T)')

p_theme <- theme(
  plot.title = element_text(face = "bold", size = 24, hjust=0.5),
  panel.border = element_blank(),
  panel.grid.minor = element_blank(),
  legend.title=element_text(size=18),
  legend.text=element_text(size=18),
  axis.title = element_text(size=18),
  axis.text = element_text(size=15),
  axis.text.y = element_text(angle = 90, hjust = 0.5),
  legend.position="bottom",
  panel.background = element_rect(fill = "#f1f2f5",
                                  colour = "white",
                                  size = 0.5, linetype = "solid")
)

get_legend_35 <- function(plot, legend_number = 1) {
  # find all legend candidates
  legends <- get_plot_component(plot, "guide-box", return_all = TRUE)
  # find non-zero legends
  idx <- which(vapply(legends, \(x) !inherits(x, "zeroGrob"), TRUE))
  # return either the chosen or the first non-zero legend if it exists,
  # and otherwise the first element (which will be a zeroGrob)
  if (length(idx) >= legend_number) {
    return(legends[[idx[legend_number]]])
  } else if (length(idx) >= 0) {
    return(legends[[idx[1]]])
  } else {
    return(legends[[1]])
  }
}

# classification scores
data <- read.csv(data_dir, header = TRUE, stringsAsFactors = FALSE)
data$synthesizer <- factor(data$synthesizer, levels = conditions)
data <- filter(data, synthesizer != 'PushGP')

c200_k2_plot = filter(data, case == 200) %>%
  ggplot(., aes(x = synthesizer, y = k_2, color = synthesizer, fill = synthesizer, shape = synthesizer)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_x_discrete(
    name="Program synthesizer"
  )+
  scale_y_continuous(
    name = "Similarity Percentage",
    labels = scales::percent
  ) +
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle('k,w = 2')+
  p_theme + theme(axis.text.x = element_blank(), axis.title.x = element_blank(),
                  axis.ticks.x =element_blank(), rect = element_rect(fill = "transparent")) +
  guides(
    shape=guide_legend(nrow=1, title.position = "left", title = 'Program Synthesizer'),
    color=guide_legend(nrow=1, title.position = "left", title = 'Program Synthesizer'),
    fill=guide_legend(nrow=1, title.position = "left", title = 'Program Synthesizer')
  )


c200_k5_plot = filter(data, case == 200) %>%
  ggplot(., aes(x = synthesizer, y = k_5, color = synthesizer, fill = synthesizer, shape = synthesizer)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name = "Similarity",
    labels = scales::percent,
  ) +
  scale_x_discrete(
    name="Program synthesizer"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle('k,w = 5')+
  p_theme + theme(axis.text.x = element_blank(), axis.title.x = element_blank(),
                  axis.ticks.x =element_blank(), rect = element_rect(fill = "transparent")) +
  guides(
    shape=guide_legend(nrow=1, title.position = "left", title = 'Program Synthesizer'),
    color=guide_legend(nrow=1, title.position = "left", title = 'Program Synthesizer'),
    fill=guide_legend(nrow=1, title.position = "left", title = 'Program Synthesizer')
  )

c200_k10_plot = filter(data, case == 200) %>%
  ggplot(., aes(x = synthesizer, y = k_10, color = synthesizer, fill = synthesizer, shape = synthesizer)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name = "Similarity",
    labels = scales::percent,
  ) +
  scale_x_discrete(
    name="Program synthesizer"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle('k,w = 10')+
  p_theme + theme(axis.text.x = element_blank(), axis.title.x = element_blank(),
                  axis.ticks.x =element_blank(), rect = element_rect(fill = "transparent")) +
  guides(
    shape=guide_legend(nrow=1, title.position = "left", title = 'Program Synthesizer'),
    color=guide_legend(nrow=1, title.position = "left", title = 'Program Synthesizer'),
    fill=guide_legend(nrow=1, title.position = "left", title = 'Program Synthesizer')
  )

row_200 = plot_grid(
  c200_k2_plot +
    theme(legend.position = "none", axis.text.y = element_text(angle = 90, hjust = 0.5), axis.text.x = element_blank(),
          axis.title.x = element_blank(), axis.ticks.x = element_blank()),
  c200_k5_plot +
    theme(legend.position = "none", axis.text.y = element_text(angle = 90, hjust = 0.5), axis.title.y = element_blank()),
  c200_k10_plot +
    theme(legend.position = "none", axis.text.y = element_text(angle = 90, hjust = 0.5), axis.title.y = element_blank()),
  ncol=3,
  rel_widths = c(1.4,1.5),
  label_size = TSIZE
)

legend <- get_legend_35(c200_k2_plot)

all_sims = plot_grid(
  ggdraw() + draw_label("Similarity for GPT-4o with 200 training cases", fontface='bold', size = 24) + p_theme,
  row_200,
  legend,
  nrow = 3,
  label_size = TSIZE,
  rel_heights = c(.15,1.1,.1)
)

save_plot(
  filename ="gpt4o-similarity-200.pdf",
  all_sims,
  base_width=10,
  base_height=5
)