# PipelineStepContext services

Available via `context.Services`:

| Service            | Type                                           | Notes                                                        |
| ------------------ | ---------------------------------------------- | ------------------------------------------------------------ |
| Output directories | `IPipelineOutputService` (ASPIREPIPELINES004)  | `.GetOutputDirectory()` / `.GetOutputDirectory(IResource)`   |
| Deployment state   | `IDeploymentStateManager` (ASPIREPIPELINES002) | Persistent JSON state across pipeline runs                   |
| Host environment   | `IHostEnvironment`                             | `.EnvironmentName` = `"Production"` for `aspire deploy`      |
| Configuration      | `IConfiguration`                               | App config including `AppHost:PathSha256`                    |
| Logging            | `context.Logger`                               | Writes to pipeline log                                       |
| Summary            | `context.Summary`                              | `context.Summary.Add("key", "value")` — shown after pipeline |

## `IPipelineOutputService` — output file paths

Returns the directory where the compute integration writes its artifacts (manifests, env files, etc.). What files exist there depends on which compute integration is used.

```csharp
#pragma warning disable ASPIREPIPELINES004
var outputService = context.Services.GetRequiredService<IPipelineOutputService>();

// Single compute environment: use root output path
string outDir = outputService.GetOutputDirectory();

// Multiple compute environments: use per-environment path
var computeEnvs = context.Model.Resources.OfType<IComputeEnvironmentResource>().ToList();
string outDir = computeEnvs.Count > 1
    ? outputService.GetOutputDirectory(computeEnv)
    : outputService.GetOutputDirectory();
```

**Docker Compose artifacts** (only with `AddDockerComposeEnvironment`):

```csharp
string envFile     = Path.Combine(outDir, $".env.{environmentName}");   // written by prepare-{env}
string composeFile = Path.Combine(outDir, "docker-compose.yaml");        // written by publish-{env}
```

## `IDeploymentStateManager` — persistent state

```csharp
#pragma warning disable ASPIREPIPELINES002
var stateManager = context.Services.GetRequiredService<IDeploymentStateManager>();
var section = await stateManager.AcquireSectionAsync("MyIntegration:resource-name", context.CancellationToken);
section.Data["ProjectId"] = projectId.ToString("D");
await stateManager.SaveSectionAsync(section, context.CancellationToken);
// Later runs: section.Data["ProjectId"]?.ToString()
```

`SaveSectionAsync` is on `IDeploymentStateManager`, not on the section object — `section.SaveAsync()` does not exist.
