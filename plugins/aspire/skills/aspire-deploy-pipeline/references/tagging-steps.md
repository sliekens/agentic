# Tagging pipeline steps

Tags categorize steps. They are plain strings — use well-known constants or define your own.

## Well-known tags

| Constant                                        | Tag value                | Used for                                              |
| ----------------------------------------------- | ------------------------ | ----------------------------------------------------- |
| `WellKnownPipelineTags.ProvisionInfrastructure` | `"provision-infra"`      | Creating cloud resources, secrets managers, databases |
| `WellKnownPipelineTags.BuildCompute`            | `"build-compute"`        | Building container images                             |
| `WellKnownPipelineTags.PushContainerImage`      | `"push-container-image"` | Pushing images to a registry                          |
| `WellKnownPipelineTags.DeployCompute`           | `"deploy-compute"`       | Deploying to compute targets                          |

## Assigning tags

```csharp
builder.WithPipelineStepFactory(
    "my-step",
    context => Task.CompletedTask,
    tags: ["my-custom-tag", WellKnownPipelineTags.ProvisionInfrastructure]
);
```

Or directly on a `PipelineStep`:

```csharp
var step = new PipelineStep
{
    Name = "my-step",
    Tags = [WellKnownPipelineTags.DeployCompute, "my-custom-tag"],
    ...
};
```

## Selecting by tag in `WithPipelineConfiguration`

```csharp
builder.WithPipelineConfiguration(context =>
{
    // All steps with a given tag
    var infraSteps = context.GetSteps(WellKnownPipelineTags.ProvisionInfrastructure);

    // Steps with a given tag scoped to one resource
    var buildSteps = context.GetSteps(myResource, WellKnownPipelineTags.BuildCompute);
});
```

`context.GetSteps(resource, tag)` narrows by both resource and tag — useful when wiring cross-resource build dependencies.
