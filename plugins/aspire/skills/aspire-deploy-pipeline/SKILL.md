---
name: aspire-deploy-pipeline
description: Reference for adding and ordering Aspire deploy pipeline steps, tagging steps, parameterizing deployment with AddParameter, configuring per-environment values with WithEnvironment, and using PipelineStepContext services. Use when asked to add a pipeline step, order deploy steps, set up infrastructure provisioning, configure deployment, or wire up aspire deploy.
---

Pipeline APIs live under `Aspire.Hosting.Pipelines`. All files that reference them need `#pragma warning disable ASPIREPIPELINES001`.

## References

- [Adding steps](references/adding-steps.md) — `WithPipelineStepFactory`, `PipelineStepAnnotation`, direct `PipelineStep` construction
- [Well-known steps](references/well-known-steps.md) — the 14 `WellKnownPipelineSteps` constants, deploy order, Docker Compose dynamic step names, common placement patterns
- [Ordering steps](references/ordering-steps.md) — `WithPipelineConfiguration`, `DependsOn`, removing built-in steps, tag-based selection
- [Tagging steps](references/tagging-steps.md) — `WellKnownPipelineTags`, custom tags, `context.GetSteps(tag)`
- [Parameters and config](references/parameters-and-config.md) — `AddParameter`, `GetValueAsync`, publish vs run mode, per-environment values
- [Pipeline services](references/pipeline-services.md) — `IPipelineOutputService`, `IDeploymentStateManager`, `IHostEnvironment`, `context.Summary`
- [Multi-step factory and keyed DI](references/multi-step-factory.md) — returning multiple steps from one factory, resource-scoped DI
- [Gotchas](references/gotchas.md) — validation rules, concurrency traps, pragma requirements, env file patching
