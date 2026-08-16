# How to use AI on this project

Goal: move faster **without** outsourcing understanding. Alexander should be able to ask you about any file you committed and get a clear answer.

## Use AI for

- Explaining a paper section, then **quizzing you** / asking you to restate in your own words
- Turning reward definitions from the proposal into pseudocode and unit tests
- Building BibTeX, download scripts, dataset loaders, plots
- Critiquing your related-work matrix for missing differentiators
- Debugging reward edge cases (empty masks, touching components, zero points)
- Drafting experiment-card boilerplate you then fill with real numbers

## Do not use AI for

- “Summarize 20 papers so I do not have to read them”
- Generating experimental claims you did not run
- Blindly copying Seg-R1 / MedGround training code without tracing reward definitions
- Committing large opaque notebooks you cannot explain

## Repo-native session pattern

1. Put the [proposal digest](../proposal/PROPOSAL_DIGEST.md) + the relevant paper note in context.
2. Ask for help on **one artifact** (one note, one function, one table column).
3. Require the model to name which reward term / paper claim it is implementing.
4. End by writing 5–10 durable lines into `literature/notes/` or an experiment card.

## Prompt starters

**Paper reading**

> I am reading `{paper}` for S-Seg-RLVR. Quiz me on how their reward/loss differs from non-differentiable structural verifiers (count, separation, topology). Do not summarize the whole paper.

**Implementing a verifier**

> Implement `R_sep` from docs/proposal/PROPOSAL_DIGEST.md with NumPy/skimage. Include failing unit tests for: (1) two points in one component, (2) perfect 1:1 match, (3) empty prediction.

**Related work**

> Here is my matrix row for Seg-R1. Challenge it: is the reward overlap-only? Is there any structural term I missed?

**Harvard RC / debugging**

> Here is the error log from a GPU smoke test. Propose three hypotheses and the smallest command to test each.

## Trust checklist before committing AI-written code

- [ ] I can explain every function in one minute
- [ ] There is at least one test or dry-run output
- [ ] No fabricated metrics
- [ ] No dataset binaries or secrets
