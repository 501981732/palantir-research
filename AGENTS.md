# Research Repository Guide

## Scope

This repository stores source-led research about Palantir products, platform capabilities, and engineering patterns. It is a research archive, not a copy of vendor documentation or a deployment project.

## Adding or revising research

1. Create `research/<topic>-<yyyy-mm>/` from `research/_templates/topic/`.
2. Prefer official announcements, documentation, API references, release notes, and public source repositories.
3. Put the answer first: definition, practical impact, limits, and open questions.
4. Separate verified facts from analysis. State the retrieval date for material claims.
5. Record every source in `sources.md`; record every stored image in `assets.md` with its original URL, source page, date, byte size, and SHA-256.
6. Do not commit credentials, customer data, copied paid content, or screenshots without an attributable source and a clear research purpose.

## Quality bar

- Links must be direct and publicly accessible when possible.
- Quotes should be short; paraphrase rather than reproduce long source passages.
- A research note should call out preview/Beta status, supported components, and meaningful exclusions.
- Verify links and image checksums before committing.

## Commit style

Use a concise imperative subject, for example: `docs: add SuperRepo research`.
