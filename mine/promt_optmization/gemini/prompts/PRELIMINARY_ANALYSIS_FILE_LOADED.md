<!--
filename: PRELIMINARY_ANALYSIS_FILE_LOADED.md
-->
# Loaded Analysis Documents

The following requirement analysis documents have been loaded into your context through previous `process()` calls with `type: "getAnalysisFiles"`.

These materials are now available for you to reference. Use them to understand user requirements, business logic, and feature specifications when designing your solution.

> **Note**: These documents are already in your conversation history. Reference them directly without calling `process()` again for the same files.

## Project Prefix

The project prefix is a short identifier used consistently across all generated artifacts including database table names, API function names, and DTO type names. For example, if the prefix is "shopping", tables might be named `shopping_customers` and DTOs might be named `IShoppingCartCommodity`.

proxmoxPaywall

## Actors

Actors represent the different user types and roles that interact with the system. Each actor has a specific permission level (guest, member, or admin) that determines their access to various API endpoints and system features. Use these actor definitions to understand authorization requirements and user-specific functionality.

```json
[{"name":"admin","kind":"admin","description":"System administrators with full control over user management, lease provisioning, container lifecycle management, and system settings."},{"name":"user","kind":"member","description":"Authenticated users who lease containers and manage their own leases, including viewing container specs and lease status."}]
```

## Analysis Files

```json
{}
```