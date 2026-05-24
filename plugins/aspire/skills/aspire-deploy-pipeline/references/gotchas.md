# Gotchas

- **`RequiredBySteps` validation is strict**: if your step lists a `requiredBy` that names a step which doesn't exist in the pipeline, the pipeline throws `InvalidOperationException`. Use `WithPipelineConfiguration` to add those dependencies safely after all steps are collected, where you can guard with `context.Steps.Any(s => s.Name == name)`.

- **Steps with the same dependency set run in parallel**: two steps that both depend on the same predecessor run concurrently. If one must finish before the other, add an explicit `DependsOn` in `WithPipelineConfiguration`.

- **`DependsOnSteps` rejects unknown names**: `Step 'X' depends on unknown step 'Y'` at pipeline startup. Always guard with `context.Steps.Any(s => s.Name == name)` before calling `.DependsOn(name)`.

- **`WithPipelineStepFactory` runs only in publish/deploy mode**: the step factory callback is not invoked in run mode. Guard run-mode behavior separately via `OnInitializeResource` or `OnBeforeStart`.

- **`section.SaveAsync()` does not exist**: the correct API is `stateManager.SaveSectionAsync(section, cancellationToken)` on `IDeploymentStateManager`, not a method on the section object.

- **`#pragma warning disable ASPIREPIPELINES001`** is required for any file that references `WellKnownPipelineSteps`, `WellKnownPipelineTags`, `PipelineStepContext`, `PipelineConfigurationContext`, or `WithPipelineStepFactory`/`WithPipelineConfiguration`.

- **`#pragma warning disable ASPIREPIPELINES004`** is required for `IPipelineOutputService`.

- **`#pragma warning disable ASPIREPIPELINES002`** is required for `IDeploymentStateManager`.

## Docker Compose-specific (only with `AddDockerComposeEnvironment`)

- **Concurrent infra and prepare steps**: `prepare-{env}` and any custom infra step that both depend on `Publish` run at the same time. If one must finish before the other, add an explicit `DependsOn` in `WithPipelineConfiguration` — see [ordering-steps.md](ordering-steps.md).
