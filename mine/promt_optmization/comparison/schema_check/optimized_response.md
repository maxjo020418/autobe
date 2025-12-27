Review provided API operations to check for security, schema alignment, logic consistency, and path parameter usage. Operations cover Proxmox tasks listing and detail retrieval for user and admin actors. Detailed Prisma schema for proxmox_paywall_proxmox_tasks is loaded to verify fields and types.

---

1. **Security:** Operations enforce authorization actors correctly (user/admin), no sensitive data exposed in response descriptions, no login/join or refresh auth types as expected.
2. **Prisma Schema Alignment:** All operations reference `proxmox_paywall_proxmox_tasks` model, path parameters match UUID field for `at` operations, request/response bodies use consistent types.
3. **Semantic Consistency:** PATCH method used reasonably for index operations with complex search/filtering, GET methods correctly for single entity retrieval.
4. **Path/Params:** Parameters are well-defined and used, no unused or ambiguous parameters.
5. **Naming and Uniqueness:** Operation names 'index' for list and 'at' for single are standard and accessor uniqueness maintained by actor differentiation in path.
6. **Authorization Consistency:** `authorizationActor` and `authorizationActors` set appropriately.

No critical or high issues found. No improvements required. All operations meet AutoBE standards.

---

No improvements required. All operations comply with security, Prisma schema alignment, and semantic rules.