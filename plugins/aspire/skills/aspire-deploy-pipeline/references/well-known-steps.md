# Well-known pipeline steps and the deploy order

## Core steps (always present)

All constants live in `WellKnownPipelineSteps`. These steps are registered regardless of which compute integration is used:

```
ProcessParameters → DeployPrereq → ValidateComputeEnvironments
                                 → BuildPrereq → Build
                                 → PublishPrereq → Publish → PushPrereq → Push → Deploy
```

| Constant                      | Step name                       | Role                                                                       |
| ----------------------------- | ------------------------------- | -------------------------------------------------------------------------- |
| `ProcessParameters`           | `process-parameters`            | Prompts for parameter values; runs before Deploy/Build/Publish prereqs     |
| `DeployPrereq`                | `deploy-prereq`                 | Tags containers, initializes deploy state; all deploy steps flow from here |
| `ValidateComputeEnvironments` | `validate-compute-environments` | Checks all compute resources are assigned                                  |
| `BuildPrereq`                 | `build-prereq`                  | Runs before any build operations                                           |
| `CheckContainerRuntime`       | `check-container-runtime`       | Verifies Docker/Podman is running; build steps that need it depend on this |
| `Build`                       | `build`                         | Aggregation step — build steps are required by this                        |
| `PublishPrereq`               | `publish-prereq`                | Runs before publish operations                                             |
| `Publish`                     | `publish`                       | Aggregation step — publish steps are required by this                      |
| `PushPrereq`                  | `push-prereq`                   | Runs before push operations                                                |
| `Push`                        | `push`                          | Aggregation step — image-push steps are required by this                   |
| `Deploy`                      | `deploy`                        | Aggregation step — all deploy-completion steps are required by this        |
| `BeforeStart`                 | `before-start`                  | Runs before the app starts (run mode, not publish mode)                    |
| `Destroy`                     | `destroy`                       | Aggregation step for destroy operations                                    |
| `DestroyPrereq`               | `destroy-prereq`                | Runs before destroy operations                                             |

## Docker Compose dynamic steps (only present with `AddDockerComposeEnvironment`)

The Docker Compose integration registers additional steps named from the environment resource name. These do **not** exist in pipelines that use a different compute integration (e.g., Kubernetes, custom SSH deploy):

```
Publish + Build → prepare-{env} → docker-compose-up-{env} → Deploy
BeforeStart ← prepare-deployment-targets-{env}
```

| Step name                               | What it does                                                                           |
| --------------------------------------- | -------------------------------------------------------------------------------------- |
| `prepare-{env-name}`                    | Writes `.env.{EnvironmentName}` with parameter values; runs after `Build` + `Publish`  |
| `docker-compose-up-{env-name}`          | Runs `docker compose up`; depends on `prepare-{env-name}`, required by `Deploy`        |
| `publish-{env-name}`                    | Writes `docker-compose.yaml`; required by `Publish`                                    |
| `prepare-deployment-targets-{env-name}` | Prepares compute targets; required by `BeforeStart`                                    |

When depending on or removing these steps from `WithPipelineConfiguration`, always guard with `context.Steps.Any(s => s.Name == name)` — the steps won't be present if the environment resource isn't registered.

## Common placement patterns

- **Infrastructure provisioning** (secrets managers, databases): `dependsOn: [DeployPrereq]`, `requiredBy: [Deploy]`, tag `ProvisionInfrastructure`
- **Custom compute build**: `dependsOn: [BuildPrereq]`, `requiredBy: [Build]`, tag `BuildCompute`
- **Image push**: `dependsOn: [PushPrereq]`, `requiredBy: [Push]`, tag `PushContainerImage`
- **Pre-build setup** (SSH, registry login, credential check): `requiredBy: [BuildPrereq]` — no `dependsOn` needed; this makes the step run before any build begins
