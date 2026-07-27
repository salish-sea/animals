# Definitions

**Audience: primarily the scientific reviewers.** This directory is the part of the
repository where domain expertise is required and software judgement is not.

These are normative. Where the glossary and a definition disagree, the definition wins.

## Why these matter more than the schema

A modelling error is usually recoverable — the raw data is preserved and a script can
fix it. A vague definition is not. Two curators apply the term differently, nobody
notices because both usages look reasonable, and the resulting inconsistency is
invisible in the data and cannot be repaired without re-examining every record by hand.

This is the one part of the design where prevention is much cheaper than cure, and it
is also the least enjoyable part to write. Do it anyway.

## Template

Every definition file has:

- **Working definition** — one or two sentences. It may be provisional. It may not be
  absent.
- **Source** — where it came from. "Working definition, <name>, <date>" is acceptable;
  silence is not. The point is that an invented definition is visibly invented.
- **Scope notes** — how to apply it in edge cases.
- **What it is not** — the distinctions most likely to be confused.
- **Status** — `working` (usable, unratified) or `agreed`.
- **Open questions**

## Status

| Term | Status | Needs |
|---|---|---|
| [ecotype](ecotype.md) | working | Expert confirmation |
| [community](community.md) | working | Q1 — may be redundant with ecotype |
| [clan](clan.md) | working | Q2 — may not be a useful rank at all |
| [pod](pod.md) | working | Expert confirmation |
| [matriline](matriline.md) | working | Expert confirmation |
| [membership](membership.md) | working | The most consequential one; see ADR-0005 |
