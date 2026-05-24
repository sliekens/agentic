# Adding pipeline steps

All pipeline APIs require `#pragma warning disable ASPIREPIPELINES001` at the top of the file.

## `WithPipelineStepFactory` (simplest path)

Call it on any resource builder. Runs only in publish/deploy mode — not in run mode.

```csharp
#pragma warning disable ASPIREPIPELINES001
using Aspire.Hosting.Pipelines;

builder.WithPipelineStepFactory(
    "my-step",
    async context =>
    {
        context.Logger.LogInformation("Running my-step");
        context.Summary.Add("My Step", "completed");
        // DI: context.Services.GetRequiredService<T>()
        // Model: context.Model.Resources.OfType<MyResource>()
    },
    dependsOn: [WellKnownPipelineSteps.DeployPrereq],
    requiredBy: [WellKnownPipelineSteps.Deploy],
    tags: [WellKnownPipelineTags.ProvisionInfrastructure]
);
```

`WithPipelineStepFactory` is on `IResourceBuilder<T>` — call it on any existing resource builder, including `builder.AddResource(myResource)`.

## `PipelineStepAnnotation` (direct construction)

Use when adding a step from inside `WithAnnotation` rather than on a builder chain, or when returning multiple steps from one factory.

```csharp
builder.WithAnnotation(new PipelineStepAnnotation(context =>
{
    return new PipelineStep
    {
        Name = $"login-to-registry-{registry.Resource.Name}",
        Action = ctx => LoginAsync(registry, ctx),
        Tags = ["registry-login"],
        DependsOnSteps = [WellKnownPipelineSteps.ProcessParameters],
        RequiredBySteps = [WellKnownPipelineSteps.PushPrereq],
        Resource = registry.Resource
    };
}));
```

The async overload `Func<PipelineStepFactoryContext, Task<IEnumerable<PipelineStep>>>` returns multiple steps from one factory — see [multi-step-factory.md](multi-step-factory.md).
