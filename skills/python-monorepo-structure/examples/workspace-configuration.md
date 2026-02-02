# Workspace Configuration

UV workspace setup and configuration for Python monorepo.

---

## Virtual Workspace Root

```toml
# Root pyproject.toml
[project]
name = "ca-workspace"
version = "0.0.0"

[tool.uv]
package = false  # Virtual root - don't install

[tool.uv.workspace]
members = [
    "ca-lib",
    "ca-messaging",
    "ca-user-service",
]
```

## Service Configuration

```toml
# ca-user-service/pyproject.toml
[project]
name = "ca-user-service"
dependencies = ["django", "ca-lib"]

[tool.uv.sources]
ca-lib = { workspace = true }
```

---

*Related: See skill.md for complete patterns*
