# Security Policy

## Reporting a vulnerability

If you believe you have found a security issue in this repository — for
example a credential leak in committed code, a workflow that grants
unintended permissions, or a vulnerability in a feeder's runtime
dependencies — please **do not open a public issue**.

Instead, report it privately via GitHub's
[security advisory form](https://github.com/clemensv/real-time-sources/security/advisories/new).

You can also email the maintainer listed in the repository profile.

Please include:

- A description of the issue and its potential impact
- Steps to reproduce, ideally with a minimal example
- The commit SHA and branch where the issue is present
- Your suggested remediation, if you have one

We'll acknowledge receipt within **5 business days** and aim to provide
an initial assessment within **15 business days**.

## Scope

This repository contains:

- **Feeder code** that polls public APIs and forwards data to message
  brokers. We are interested in reports about credential handling,
  dependency vulnerabilities, container image hygiene, and any way a
  feeder could be coerced into emitting fabricated or modified events.
- **Deployment scripts** (PowerShell, Bicep, ARM, Terraform-equivalent
  ARM templates) that provision Azure resources. We are interested in
  reports about overly permissive role assignments, hard-coded
  identifiers, or insecure defaults.
- **GitHub Actions workflows**. We are interested in reports about
  workflow injection vectors, untrusted-input handling, or excessive
  token scopes.

We are **not** responsible for vulnerabilities in the upstream public
data sources themselves.

## Disclosure

We follow coordinated disclosure. Once a fix is in place we will
publish a security advisory crediting the reporter (unless you ask to
remain anonymous).
