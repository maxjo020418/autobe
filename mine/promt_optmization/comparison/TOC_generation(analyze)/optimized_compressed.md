# Claims (optimized)

1. The system is a paywall middleware for leasing Proxmox VE LXC containers.
2. The system has two roles: Admin and User.
3. Admin has full access, and User can access only their own leased containers.
4. All API endpoints use Basic Authentication.
5. The system enforces RBAC and binds each user to container IDs.
6. Invalid credentials return 401, and unauthorized or expired-lease access returns 403.
7. Lease creation fetches the next VMID, provisions an LXC via the Proxmox API, and starts it.
8. Each lease record includes user id, VMID, ISO 8601 start/end, and RAM/CPU/disk specs.
9. Lease renewal extends the end time and starts the container if stopped, and status can be running/stopped/expired.
10. The system exposes list/exec/VNC console/start/stop APIs, uses HTTPS, protects secrets, audits access, and supports pluggable payments (x402).
