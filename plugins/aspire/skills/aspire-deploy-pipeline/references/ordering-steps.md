# Ordering steps with `WithPipelineConfiguration`

`WithPipelineConfiguration` runs after all step factories have been called, so you can safely look up dynamically-named steps by name. Use it whenever static `dependsOn`/`requiredBy` on `WithPipelineStepFactory` is not enough — for example, when the step you need to depend on is registered by another integration and its name isn't known at factory registration time.

```csharp
#pragma warning disable ASPIREPIPELINES001
using Aspire.Hosting.Pipelines;

string myStepName = "my-infra-step";

builder.WithPipelineStepFactory(
    myStepName,
    context => MyStep.ExecuteAsync(context),
    dependsOn: [WellKnownPipelineSteps.DeployPrereq],
    requiredBy: [WellKnownPipelineSteps.Deploy],
    tags: [WellKnownPipelineTags.ProvisionInfrastructure]
);

builder.WithPipelineConfiguration(context =>
{
    var myStep = context.Steps.FirstOrDefault(s => s.Name == myStepName);
    if (myStep is null) return;

    // Depend on a step registered by another integration, guarded by existence check
    string otherStep = "other-integration-setup";
    if (context.Steps.Any(s => s.Name == otherStep))
        myStep.DependsOn(otherStep);
});
```

## Rules

- Only add `DependsOn` for step names you confirmed exist — the pipeline throws if a step depends on an unknown name. Always guard with `context.Steps.Any(s => s.Name == name)`.
- `context.Steps` is `IReadOnlyList<PipelineStep>` but `PipelineStep.DependsOnSteps` is a mutable `List<string>` — call `.DependsOn(name)` directly on the step object.
- Both `DependsOn` and `RequiredBySteps` are valid inside the configuration callback; validation runs after it returns.
- Async overload: `WithPipelineConfiguration(async context => { ... })`.

## Removing a built-in step

When your integration replaces a compute integration's deploy step with its own, remove the original from all dependency references so the pipeline doesn't wait for a step that won't run:

```csharp
builder.WithPipelineConfiguration(context =>
{
    string stepToReplace = "integration-deploy-step";
    foreach (var step in context.Steps)
    {
        step.DependsOnSteps.Remove(stepToReplace);
        step.RequiredBySteps.Remove(stepToReplace);
    }
    // Wire in the replacement
    context.Steps.FirstOrDefault(s => s.Name == WellKnownPipelineSteps.Deploy)
        ?.DependsOn("my-replacement-deploy-step");
});
```

**Docker Compose example**: replacing `docker-compose-up-{env}` with an SSH remote-deploy step:

```csharp
builder.WithPipelineConfiguration(context =>
{
    string composeUp = $"docker-compose-up-{envName}"; // only present with AddDockerComposeEnvironment
    foreach (var step in context.Steps)
    {
        step.DependsOnSteps.Remove(composeUp);
        step.RequiredBySteps.Remove(composeUp);
    }
    context.Steps.FirstOrDefault(s => s.Name == WellKnownPipelineSteps.Deploy)
        ?.DependsOn("remote-docker-deploy-myenv");
});
```

## Inserting between Docker Compose steps (only with `AddDockerComposeEnvironment`)

Use when your step must run after `prepare-{env}` writes the env file but before `docker-compose-up-{env}` starts the stack — for example, to patch values the prepare step left blank. Wire: `prepare-{env}` → your step → `docker-compose-up-{env}`.

```csharp
#pragma warning disable ASPIREPIPELINES001
using Aspire.Hosting.ApplicationModel;
using Aspire.Hosting.Pipelines;

builder.WithPipelineConfiguration(context =>
{
    var myStep = context.Steps.FirstOrDefault(s => s.Name == myStepName);
    if (myStep is null) return;

    foreach (var computeEnv in context.Model.Resources.OfType<IComputeEnvironmentResource>())
    {
        string prepareStep = $"prepare-{computeEnv.Name}";
        string composeUpStep = $"docker-compose-up-{computeEnv.Name}";

        if (context.Steps.Any(s => s.Name == prepareStep))
            myStep.DependsOn(prepareStep);

        context.Steps.FirstOrDefault(s => s.Name == composeUpStep)?.DependsOn(myStepName);
    }
});
```

To *replace* `docker-compose-up-{env}` entirely instead, see [Removing a built-in step](#removing-a-built-in-step) above.

## Tag-based selection

When you want to depend on all steps of a category without naming them individually:

```csharp
builder.WithPipelineConfiguration(context =>
{
    var infraSteps = context.GetSteps(WellKnownPipelineTags.ProvisionInfrastructure);
    var myStep = context.Steps.FirstOrDefault(s => s.Name == "my-step");
    myStep?.DependsOnSteps.AddRange(infraSteps.Select(s => s.Name));

    // Narrow to a specific resource
    var buildSteps = context.GetSteps(myResource, WellKnownPipelineTags.BuildCompute);
});
```
