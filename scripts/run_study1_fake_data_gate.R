#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(brms)
  library(dplyr)
  library(readr)
  library(tibble)
})

args <- commandArgs(trailingOnly = TRUE)

parse_args <- function(args) {
  out <- list(
    pilot_key = NULL,
    annotated_pilot = NULL,
    output_dir = NULL,
    simulations = 200L,
    quota_per_corpus = 120L,
    seed = 20260320L,
    algorithm = "meanfield",
    chains = 2L,
    iter = 2000L,
    warmup = 1000L
  )

  i <- 1L
  while (i <= length(args)) {
    key <- args[[i]]
    if (i == length(args)) {
      stop("Missing value for argument: ", key, call. = FALSE)
    }
    value <- args[[i + 1L]]
    if (key == "--pilot-key") out$pilot_key <- value
    else if (key == "--annotated-pilot") out$annotated_pilot <- value
    else if (key == "--output-dir") out$output_dir <- value
    else if (key == "--simulations") out$simulations <- as.integer(value)
    else if (key == "--quota-per-corpus") out$quota_per_corpus <- as.integer(value)
    else if (key == "--seed") out$seed <- as.integer(value)
    else if (key == "--algorithm") out$algorithm <- value
    else if (key == "--chains") out$chains <- as.integer(value)
    else if (key == "--iter") out$iter <- as.integer(value)
    else if (key == "--warmup") out$warmup <- as.integer(value)
    else stop("Unknown argument: ", key, call. = FALSE)
    i <- i + 2L
  }

  required <- c("pilot_key", "annotated_pilot", "output_dir")
  missing <- required[vapply(required, function(x) is.null(out[[x]]), logical(1))]
  if (length(missing)) {
    stop("Missing required arguments: ", paste(missing, collapse = ", "), call. = FALSE)
  }
  out
}

opts <- parse_args(args)
set.seed(opts$seed)
dir.create(opts$output_dir, recursive = TRUE, showWarnings = FALSE)

reference_levels <- list(
  auxiliary_type = "none-other",
  participial_predicate = "no",
  agent_realization = "none",
  promotion_type = "none-unclear",
  eventive_stative = "stative",
  syntactic_environment = "nonfinite-or-reduced",
  subject_role_profile = "unclear-other"
)

factor_levels <- list(
  auxiliary_type = c("none-other", "be", "get"),
  participial_predicate = c("no", "yes"),
  agent_realization = c("none", "by-phrase", "other-overt-agentive"),
  promotion_type = c("none-unclear", "direct-object-promotion", "oblique-stranding-promotion"),
  eventive_stative = c("stative", "eventive", "ambiguous"),
  syntactic_environment = c("nonfinite-or-reduced", "finite-clause"),
  subject_role_profile = c("unclear-other", "patient-theme-like", "locative-oblique-like")
)

norm_value <- function(x) {
  x <- trimws(tolower(x))
  x <- gsub("_", "-", x, fixed = TRUE)
  x
}

strict_checklist <- function(df) {
  aux <- norm_value(df$auxiliary_type)
  participial <- norm_value(df$participial_predicate)
  nsubj_pass <- trimws(df$has_nsubj_pass)
  promotion <- norm_value(df$promotion_type)
  promoted <- ifelse(
    nsubj_pass %in% c("0", "1"),
    nsubj_pass == "1",
    promotion %in% c("direct-object-promotion", "oblique-stranding-promotion")
  )
  as.integer(aux %in% c("be", "get") & participial == "yes" & promoted)
}

stronger_rule <- function(df) {
  strict <- strict_checklist(df)
  eventive <- norm_value(df$eventive_stative)
  as.integer(strict == 1L & eventive != "stative")
}

prepare_pilot_data <- function(key_path, annotation_path) {
  key <- read_csv(key_path, show_col_types = FALSE)
  ann <- read_csv(annotation_path, show_col_types = FALSE)
  if (!"pilot_item_id" %in% names(ann)) {
    stop("Annotated pilot must include pilot_item_id", call. = FALSE)
  }

  merged <- key %>%
    inner_join(
      ann %>% select(pilot_item_id, family_status, peripheral_subtype, auxiliary_type,
                     participial_predicate, agent_realization, promotion_type,
                     eventive_stative, syntactic_environment, subject_role_profile, notes),
      by = "pilot_item_id",
      suffix = c("_key", "")
    ) %>%
    mutate(
      passive_family_binary = case_when(
        family_status == "core" ~ 1,
        family_status == "foil" ~ 0,
        TRUE ~ NA_real_
      )
    )

  merged$strict_checklist <- strict_checklist(merged)
  merged$stronger_rule <- stronger_rule(merged)

  merged <- merged %>%
    filter(!is.na(passive_family_binary))

  if (!nrow(merged)) {
    stop("No core/foil rows available after merging pilot annotations", call. = FALSE)
  }

  for (field in names(factor_levels)) {
    merged[[field]] <- factor(norm_value(merged[[field]]), levels = factor_levels[[field]])
    merged[[field]] <- stats::relevel(merged[[field]], ref = reference_levels[[field]])
  }
  merged$corpus <- factor(merged$corpus, levels = c("ewt", "gum"))
  merged
}

model_formula <- bf(
  passive_family_binary ~ auxiliary_type + participial_predicate + agent_realization +
    promotion_type + eventive_stative + syntactic_environment + subject_role_profile
)

model_priors <- c(
  prior(normal(0, 2.5), class = "Intercept"),
  prior(normal(0, 2.5), class = "b")
)

fit_model <- function(data) {
  brm(
    formula = model_formula,
    data = data,
    family = bernoulli(),
    prior = model_priors,
    seed = opts$seed,
    chains = opts$chains,
    iter = opts$iter,
    warmup = opts$warmup,
    backend = "rstan",
    algorithm = opts$algorithm,
    drop_unused_levels = FALSE,
    refresh = 0,
    silent = 2
  )
}

brier_by_draw <- function(fit, newdata, outcome) {
  preds <- posterior_epred(fit, newdata = newdata, re_formula = NA)
  rowMeans((preds - matrix(outcome, nrow = nrow(preds), ncol = length(outcome), byrow = TRUE))^2)
}

criterion_summary <- function(delta_draws, threshold) {
  mean(delta_draws > threshold)
}

simulate_dataset <- function(pilot_data, generator_fit, draw_id, quota_per_corpus) {
  pieces <- lapply(c("ewt", "gum"), function(corpus_name) {
    pool <- pilot_data %>% filter(corpus == corpus_name)
    if (!nrow(pool)) {
      stop("No pilot rows available for corpus ", corpus_name, call. = FALSE)
    }
    idx <- sample(seq_len(nrow(pool)), size = quota_per_corpus, replace = TRUE)
    sample_rows <- pool[idx, , drop = FALSE]
    probs <- as.numeric(posterior_epred(generator_fit, newdata = sample_rows, draw_ids = draw_id, re_formula = NA))
    sample_rows$passive_family_binary <- rbinom(length(probs), size = 1L, prob = probs)
    sample_rows
  })
  bind_rows(pieces)
}

evaluate_direction <- function(train_data, test_data) {
  fit <- fit_model(train_data)
  brier_draws <- brier_by_draw(fit, test_data, test_data$passive_family_binary)
  strict_brier <- mean((test_data$strict_checklist - test_data$passive_family_binary)^2)
  stronger_brier <- mean((test_data$stronger_rule - test_data$passive_family_binary)^2)
  tibble(
    strict_prob = criterion_summary(strict_brier - brier_draws, 0.01),
    stronger_prob = criterion_summary(stronger_brier - brier_draws, 0.005),
    strict_mean_delta = mean(strict_brier - brier_draws),
    stronger_mean_delta = mean(stronger_brier - brier_draws)
  )
}

pilot_data <- prepare_pilot_data(opts$pilot_key, opts$annotated_pilot)
generator_fit <- fit_model(pilot_data)

draw_count <- ndraws(generator_fit)
sim_results <- vector("list", opts$simulations)

for (sim_idx in seq_len(opts$simulations)) {
  draw_id <- sample.int(draw_count, size = 1L)
  sim_data <- simulate_dataset(pilot_data, generator_fit, draw_id, opts$quota_per_corpus)
  dir_ewt_to_gum <- evaluate_direction(
    train_data = sim_data %>% filter(corpus == "ewt"),
    test_data = sim_data %>% filter(corpus == "gum")
  )
  dir_gum_to_ewt <- evaluate_direction(
    train_data = sim_data %>% filter(corpus == "gum"),
    test_data = sim_data %>% filter(corpus == "ewt")
  )

  sim_results[[sim_idx]] <- tibble(
    simulation = sim_idx,
    ewt_to_gum_strict = dir_ewt_to_gum$strict_prob,
    ewt_to_gum_stronger = dir_ewt_to_gum$stronger_prob,
    gum_to_ewt_strict = dir_gum_to_ewt$strict_prob,
    gum_to_ewt_stronger = dir_gum_to_ewt$stronger_prob,
    strict_pass = dir_ewt_to_gum$strict_prob >= 0.90 && dir_gum_to_ewt$strict_prob >= 0.90,
    stronger_pass = dir_ewt_to_gum$stronger_prob >= 0.80 && dir_gum_to_ewt$stronger_prob >= 0.80
  )
}

sim_results <- bind_rows(sim_results)

summary_tbl <- tibble(
  simulations = opts$simulations,
  quota_per_corpus = opts$quota_per_corpus,
  strict_pass_rate = mean(sim_results$strict_pass),
  stronger_pass_rate = mean(sim_results$stronger_pass),
  strict_gate = mean(sim_results$strict_pass) >= 0.75,
  stronger_gate = mean(sim_results$stronger_pass) >= 0.60,
  overall_gate = mean(sim_results$strict_pass) >= 0.75 && mean(sim_results$stronger_pass) >= 0.60
)

write_csv(sim_results, file.path(opts$output_dir, "study1_fake_data_gate_simulations.csv"))
write_csv(summary_tbl, file.path(opts$output_dir, "study1_fake_data_gate_summary.csv"))
write_csv(
  pilot_data %>%
    count(corpus, family_status, name = "n"),
  file.path(opts$output_dir, "study1_fake_data_gate_pilot_counts.csv")
)

cat("Study 1 fake-data gate\n")
print(summary_tbl)
