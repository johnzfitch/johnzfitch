# What

> Independent research on transformer internals and the mathematical structures they implicitly compute on.

*by John Zachary Fitch*

## The Transporter program

I run the Transporter program, where I study the geometry inside transformers and build model architectures from the exceptional Jordan algebra (the 27-dimensional Albert algebra). I take constructions from algebra and geometry, turn them into models I can actually run, and test them. The questions I keep coming back to: what does a model hold on to, how does it change as it learns, and can its structure show us better ways to learn?

- I built the Albert Engine (private repo), a tested numerical runtime for the Albert algebra. I use it to prototype sequence models, memory mechanisms, optimizers, and diagnostics that work with that geometry.
- I study transformer representations and how optimizers behave numerically, and I run causal interventions on pretrained open models to see which geometric structure they actually depend on.
- I test ideas with numerical checks and head-to-head comparisons under controlled conditions.
- I write down my predictions before an experiment, mark each claim as proved, measured, or conjectured, and report the limits and the negative results next to the positive ones.

## Typed embeddings

Tokens don't just relate in pairs. Language has clauses with structure of their own, and the embedding space should know about it. That's an algebra question, not a feature-engineering one. Active work.

## The harmonic Maass form framework

Different teams build different transformers (Mistral, Qwen, Pythia), and they converge on the same internal shape. The framework is one way of saying *why*: what they're all approximating belongs to a specific kind of mathematical object. Its structural predictions hold across models.

## Shadow-Line Helical Transformer (Transformer²)

Softmax is *soft*. It never actually chooses; it just biases the average. This architecture replaces it with hard structure that still moves: two interlinked helices in a curved space, where the geometry says where you are without forcing a choice.

## Papers, code, and write-ups

- **The Barnes–Gindikin Symbol at Fractional Rank: Continuation Without a Determinant Carrier, Positivity Without a Cone.** [PDF](papers/gindikin-rank.pdf). Its exact-arithmetic verification code is archived on Zenodo, along with the earlier revision. [DOI 10.5281/zenodo.21713316](https://doi.org/10.5281/zenodo.21713316) / [gindikin-rank](https://github.com/johnzfitch/gindikin-rank)
- **Softmax Beyond the Simplex: Gibbs Charts and Polar Transport on Euclidean Jordan Algebras.** Softmax is the normalized exponential of the simplest Euclidean Jordan algebra. This paper builds the same map on every one of them and works out what the extra frame directions carry. The numerical verification scripts, and transcripts of their runs, are on GitHub. [PDF](papers/gibbs-chart.pdf) / [gibbs-chart](https://github.com/johnzfitch/gibbs-chart)
- **Reading the Residual.** Uses the geometry of symmetric cones to give an exact, computable error certificate for the inverse square roots that Kronecker-factored optimizers like Shampoo, SOAP, and K-FAC compute in low precision. [kl-shampoo-gindikin-bridge](https://github.com/johnzfitch/kl-shampoo-gindikin-bridge)
- **Communication transport experiments.** Complete outputs, with null and control runs, from transport experiments on Pythia-70M, Pythia-160M, and GPT-2. [communication-transport](https://github.com/johnzfitch/communication-transport)
- **Who Steers the User? Analyzing Claude Code and Codex Runtimes.** In two coding agents the user role carries text that no user typed, and the model isn't told which text that is. Evidence from Codex rollout logs and Claude Code's prompt history, and a proposed fix. A 24-hour research project, presented at Dev Day office hours, revised in September 2026. [PDF](papers/who-steers-the-user.pdf)
- **Inherit All of Nothing.** From September 2025 to January 2026, release builds of the OpenAI Codex CLI stripped the dynamic-linker variables from every command the agent ran. I traced it and reported it in #8945, and the fix shipped with credit. This paper covers the bug and the runtime code around it, then rechecks everything I claimed about it between March and May 2026 against the upstream history, the code and my probe data, and says what holds, what I withdraw, and what cannot be known from outside. It replaces the earlier Parts I to III. [PDF](papers/inherit-all-of-nothing.pdf)

## Where the question came from

The research question goes back to two pages of notes I wrote in a linear algebra class at SRJC in 2019. If two brains do the same things in different places, is there a map that sends each one onto shared functional pieces, where the difference becomes readable? Now I'm asking the same question about transformers.

## Working together

I'm looking for researchers, labs, and engineering teams to work with on model architecture, learning algorithms, interpretability, and agent infrastructure, especially where a hard research question needs a working implementation and a clean experiment.

- Email: [zack@internetuniverse.org](mailto:zack@internetuniverse.org)
- ORCID: [0009-0007-7953-1531](https://orcid.org/0009-0007-7953-1531)
- Resume: [resume.md](resume.md)
