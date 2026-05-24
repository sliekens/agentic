# Multi-step factory and keyed DI

## Multi-step factory

When a single resource needs a chain of ordered steps, return them all from one `PipelineStepAnnotation` factory:

```csharp
#pragma warning disable ASPIREPIPELINES001
using Aspire.Hosting.Pipelines;

builder.WithPipelineStepFactory(async factoryContext =>
{
    var resource = (MyResource)factoryContext.Resource;
    string n = resource.Name;

    // Step 1: pre-build setup — runs before any Docker build
    var prereqStep = new PipelineStep
    {
        Name = $"my-prereq-{n}",
        Description = "Verify connectivity and gather credentials",
        Action = ctx => MyHelper.VerifyAsync(ctx),
        RequiredBySteps = [WellKnownPipelineSteps.BuildPrereq],
        Resource = resource
    };

    // Step 2: configure deployment — depends on step 1
    var configStep = new PipelineStep
    {
        Name = $"my-configure-{n}",
        Action = ctx => MyHelper.ConfigureAsync(ctx),
        DependsOnSteps = [$"my-prereq-{n}"],
        RequiredBySteps = [WellKnownPipelineSteps.BuildPrereq],
        Resource = resource
    };

    // Step 3: actual deploy — runs after Push, required by Deploy
    var deployStep = new PipelineStep
    {
        Name = $"my-deploy-{n}",
        Action = ctx => MyHelper.DeployAsync(ctx),
        DependsOnSteps = [$"my-configure-{n}", WellKnownPipelineSteps.Push],
        RequiredBySteps = [WellKnownPipelineSteps.Deploy],
        Tags = [WellKnownPipelineTags.DeployCompute],
        Resource = resource
    };

    return new[] { prereqStep, configStep, deployStep };
});
```

## Keyed DI for resource-scoped services

Register a pipeline object as a keyed singleton so both the factory and the configuration callback share state without passing data through closure:

```csharp
// Registration (in AddMyIntegration extension or similar)
builder.ApplicationBuilder.Services.AddKeyedSingleton<MyPipeline>(resource, (sp, _) =>
    new MyPipeline(resource, sp));

// In factory
builder.WithPipelineStepFactory(ctx =>
{
    var pipeline = ctx.PipelineContext.Services.GetRequiredKeyedService<MyPipeline>(resource);
    return pipeline.CreateSteps(ctx);
});

// In configuration
builder.WithPipelineConfiguration(ctx =>
{
    var pipeline = ctx.Services.GetRequiredKeyedService<MyPipeline>(resource);
    pipeline.ConfigurePipeline(ctx);
});
```
