#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(rstan)
  library(tibble)
})

rstan_options(auto_write = TRUE)
options(mc.cores = max(1L, parallel::detectCores(logical = FALSE)))

args <- commandArgs(trailingOnly = TRUE)

parse_args <- function(args) {
  out <- list(
    pilot_key = NULL,
    annotated_pilot = NULL,
    supplement_key = NULL,
    supplement_annotated = NULL,
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
    else if (key == "--supplement-key") out$supplement_key <- value
    else if (key == "--supplement-annotated") out$supplement_annotated <- value
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
  participial_form = "none",
  licensing_marker = "absent-other",
  constructional_environment = "clausal-predication",
  local_subject_present = "no",
  by_pp_present = "no",
  stranded_preposition = "no",
  event_implied = "no",
  agent_implied = "no",
  predicand_as_undergoer = "no"
)

factor_levels <- list(
  participial_form = c("none", "past-participle", "gerund-participial"),
  licensing_marker = c(
    "absent-other", "be", "passive-get", "causative-get-have",
    "subordinator-or-adjunct", "modifier-position"
  ),
  constructional_environment = c(
    "clausal-predication", "bare-infinitival-complement",
    "to-infinitival-complement", "gerund-participial-clause",
    "adjunct-participial-clause", "object-predicative-complement",
    "reduced-modifier"
  ),
  local_subject_present = c("no", "yes"),
  by_pp_present = c("no", "yes"),
  stranded_preposition = c("no", "yes"),
  event_implied = c("no", "yes", "unclear"),
  agent_implied = c("no", "yes", "unclear"),
  predicand_as_undergoer = c("no", "yes", "unclear")
)

norm_value <- function(x) {
  x <- trimws(tolower(x))
  x <- gsub("_", "-", x, fixed = TRUE)
  x
}

has_surface_be_or_get <- function(df) {
  fields <- c("aux_pass_lemmas", "aux_lemmas", "cop_lemmas")
  out <- rep(FALSE, nrow(df))
  for (field in fields) {
    values <- norm_value(df[[field]])
    out <- out | grepl("(^|;)(be|get)($|;)", values)
  }
  out
}

strict_checklist <- function(df) {
  participial <- norm_value(df$participial_form)
  local_subject <- norm_value(df$local_subject_present)
  as.integer(
    participial == "past-participle" &
      has_surface_be_or_get(df) &
      local_subject == "yes"
  )
}

stronger_rule <- function(df) {
  strict <- strict_checklist(df)
  eventive <- norm_value(df$event_implied)
  as.integer(strict == 1L & eventive != "no")
}

prepare_pilot_data <- function(key_path, annotation_path) {
  key <- read_csv(key_path, show_col_types = FALSE)
  ann <- read_csv(annotation_path, show_col_types = FALSE)
  if (!"pilot_item_id" %in% names(ann)) {
    stop("Annotated pilot must include pilot_item_id", call. = FALSE)
  }

  merged <- key %>%
    inner_join(
      ann %>% select(
        pilot_item_id, participial_form, licensing_marker,
        constructional_environment, local_subject_present, by_pp_present,
        stranded_preposition, event_implied, agent_implied,
        predicand_as_undergoer, peripheral_subtype, family_status, notes
      ),
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

prepare_combined_pilot_data <- function(
  pilot_key_path,
  annotated_pilot_path,
  supplement_key_path = NULL,
  supplement_annotated_path = NULL
) {
  base <- prepare_pilot_data(pilot_key_path, annotated_pilot_path)
  if (!is.null(supplement_key_path) && !is.null(supplement_annotated_path)) {
    supplement <- prepare_pilot_data(supplement_key_path, supplement_annotated_path)
    base <- bind_rows(base, supplement)
  } else if (xor(is.null(supplement_key_path), is.null(supplement_annotated_path))) {
    stop("Supplement key and supplement annotation must be provided together", call. = FALSE)
  }
  base
}

design_formula <- as.formula(
  ~ participial_form + licensing_marker + constructional_environment +
    local_subject_present + by_pp_present + stranded_preposition +
    event_implied + agent_implied + predicand_as_undergoer
)

stan_logit_code <- "
data {
  int<lower=1> N;
  int<lower=1> K;
  matrix[N, K] X;
  int<lower=0, upper=1> y[N];
}
parameters {
  vector[K] beta;
}
model {
  beta ~ normal(0, 2.5);
  y ~ bernoulli_logit(X * beta);
}
generated quantities {
  vector[N] p = inv_logit(X * beta);
}
"

make_design <- function(data) {
  model.matrix(design_formula, data = data)
}

make_stan_data <- function(data) {
  x <- make_design(data)
  list(
    N = nrow(x),
    K = ncol(x),
    X = unname(x),
    y = as.integer(data$passive_family_binary)
  )
}

fit_model <- function(stan_model, data) {
  stan_data <- make_stan_data(data)
  if (opts$algorithm %in% c("meanfield", "fullrank")) {
    return(vb(
      object = stan_model,
      data = stan_data,
      algorithm = opts$algorithm,
      iter = opts$iter,
      output_samples = max(1000L, opts$iter - opts$warmup),
      seed = opts$seed,
      refresh = 0
    ))
  }
  if (opts$algorithm == "sampling") {
    return(sampling(
      object = stan_model,
      data = stan_data,
      chains = opts$chains,
      iter = opts$iter,
      warmup = opts$warmup,
      seed = opts$seed,
      refresh = 0
    ))
  }
  stop(
    "Unsupported --algorithm for rstan backend: ", opts$algorithm,
    ". Use meanfield, fullrank, or sampling.",
    call. = FALSE
  )
}

extract_beta_draws <- function(fit) {
  draws <- rstan::extract(fit, pars = "beta", permuted = TRUE)$beta
  if (is.null(dim(draws))) {
    matrix(draws, nrow = 1)
  } else {
    as.matrix(draws)
  }
}

brier_by_draw <- function(beta_draws, newdata, outcome) {
  x <- make_design(newdata)
  preds <- plogis(beta_draws %*% t(x))
  rowMeans((preds - matrix(outcome, nrow = nrow(preds), ncol = length(outcome), byrow = TRUE))^2)
}

criterion_summary <- function(delta_draws, threshold) {
  mean(delta_draws > threshold)
}

simulate_dataset <- function(pilot_data, generator_beta_draws, draw_id, quota_per_corpus) {
  pieces <- lapply(c("ewt", "gum"), function(corpus_name) {
    pool <- pilot_data %>% filter(corpus == corpus_name)
    if (!nrow(pool)) {
      stop("No pilot rows available for corpus ", corpus_name, call. = FALSE)
    }
    idx <- sample(seq_len(nrow(pool)), size = quota_per_corpus, replace = TRUE)
    sample_rows <- pool[idx, , drop = FALSE]
    x <- make_design(sample_rows)
    probs <- as.numeric(plogis(x %*% generator_beta_draws[draw_id, ]))
    sample_rows$passive_family_binary <- rbinom(length(probs), size = 1L, prob = probs)
    sample_rows
  })
  bind_rows(pieces)
}

evaluate_direction <- function(stan_model, train_data, test_data) {
  fit <- fit_model(stan_model, train_data)
  beta_draws <- extract_beta_draws(fit)
  brier_draws <- brier_by_draw(beta_draws, test_data, test_data$passive_family_binary)
  strict_brier <- mean((test_data$strict_checklist - test_data$passive_family_binary)^2)
  stronger_brier <- mean((test_data$stronger_rule - test_data$passive_family_binary)^2)
  tibble(
    strict_prob = criterion_summary(strict_brier - brier_draws, 0.01),
    stronger_prob = criterion_summary(stronger_brier - brier_draws, 0.005),
    strict_mean_delta = mean(strict_brier - brier_draws),
    stronger_mean_delta = mean(stronger_brier - brier_draws)
  )
}

pilot_data <- prepare_combined_pilot_data(
  opts$pilot_key,
  opts$annotated_pilot,
  opts$supplement_key,
  opts$supplement_annotated
)
compiled_model <- stan_model(
  model_code = stan_logit_code,
  model_name = "study1_fake_data_gate_logit"
)
generator_fit <- fit_model(compiled_model, pilot_data)
generator_beta_draws <- extract_beta_draws(generator_fit)

draw_count <- nrow(generator_beta_draws)
sim_results <- vector("list", opts$simulations)

for (sim_idx in seq_len(opts$simulations)) {
  draw_id <- sample.int(draw_count, size = 1L)
  sim_data <- simulate_dataset(pilot_data, generator_beta_draws, draw_id, opts$quota_per_corpus)
  dir_ewt_to_gum <- evaluate_direction(
    stan_model = compiled_model,
    train_data = sim_data %>% filter(corpus == "ewt"),
    test_data = sim_data %>% filter(corpus == "gum")
  )
  dir_gum_to_ewt <- evaluate_direction(
    stan_model = compiled_model,
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
