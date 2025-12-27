<!-- filename: PRELIMINARY_PRISMA_SCHEMA.md -->
 # preliminary loading rules (prisma schemas)

 - do not request already-loaded prisma schemas.
 - only request schema names listed under "not yet loaded".
 - if you need fields/relations/constraints, request the actual schema; do not guess.

 not yet loaded (available on request):
 Name | Stance | Summary
-----|--------|---------
proxmox_paywall_configurations | primary | System-wide configuration settings for the proxmox paywall system
proxmox_paywall_system_events | snapshot | Audit and system event logs capturing significant actions and changes within the proxmox paywall system
proxmox_paywall_admins | primary | System administrators with full control over user management, lease provisioning, container lifecycle management, and system settings
proxmox_paywall_admin_sessions | subsidiary | Authentication sessions for system administrators
proxmox_paywall_users | primary | Authenticated users who lease containers and manage their own leases
proxmox_paywall_user_sessions | subsidiary | Authentication sessions for authenticated users
proxmox_paywall_leases | primary | Core lease information for containers provisioned through Proxmox VE
proxmox_paywall_lease_renewals | snapshot | Historical records of lease renewal requests for Proxmox container leases
proxmox_paywall_container_statuses | primary | Operational statuses of provisioned containers managed via Proxmox VE
proxmox_paywall_vnc_proxy_sessions | primary | VNC proxy session records for Proxmox VE containers
