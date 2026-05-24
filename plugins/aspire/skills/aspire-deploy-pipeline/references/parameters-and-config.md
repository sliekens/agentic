# Parameters and per-environment configuration

## Declaring and reading parameters

Parameters declared with `AddParameter` work in both run mode and deploy mode — no need to branch on `IsRunMode`/`IsPublishMode`. In run mode the value is read from configuration (user secrets, `appsettings.Development.json`); in deploy mode it is prompted by `ProcessParameters` before `DeployPrereq` runs.

```csharp
// Program.cs — unconditional, works in all modes
var apiKey = builder.AddParameter("api-key", secret: true);
var region = builder.AddParameter("target-region");
resource.WithEnvironment("API_KEY", apiKey);
resource.WithEnvironment("REGION", region);
```

Read the resolved value inside a pipeline step via `GetValueAsync`:

```csharp
string? key = await apiKey.Resource.GetValueAsync(context.CancellationToken);
string? reg = await region.Resource.GetValueAsync(context.CancellationToken);
```

Pass the `ParameterResource` into your resource type so the step can find it:

```csharp
public class MyResource(string name, ParameterResource token) : Resource(name)
{
    public ParameterResource Token { get; } = token;
}

// In step:
var resource = context.Model.Resources.OfType<MyResource>().First();
string? token = await resource.Token.GetValueAsync(context.CancellationToken);
```

## Per-environment values

Set different parameter values per deployment target via configuration on the target host — no code change needed:

```csharp
// Program.cs
var cachePath = builder.AddParameter("cache-path");
resource.WithEnvironment("CACHE_PATH", cachePath);
// On the target: Parameters__cache-path=/vol/cache
```

## Environment name

The environment name matches `IHostEnvironment.EnvironmentName` and defaults to `"Production"` for `aspire deploy`:

```csharp
// In a pipeline step:
var hostEnv = context.Services.GetService<IHostEnvironment>();
string envName = hostEnv?.EnvironmentName ?? "Production";
// Used for .env.{envName} file naming, state keys, etc.
```

