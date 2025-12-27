# Functional Requirements for proxmoxPaywall

## User Roles and Authentication

### 1. User Roles

- **Admin**: Has full control over the system, including managing users, leases, containers, and system configurations.
- **User**: Can lease containers, manage their leased containers, and interact with container resources subject to access controls.

### 2. Authentication

- The system SHALL implement Basic Authentication for all API endpoints.
- WHEN a user sends a request to an API endpoint, THE system SHALL validate the user's credentials via Basic Authentication.
- WHEN authentication fails, THE system SHALL reject the request with an appropriate HTTP 401 Unauthorized response.

### 3. Authorization and Access Control

- Users SHALL be tied to the containers they have leased.
- The system SHALL enforce that users can access only containers they have leased.
- Admins SHALL have unrestricted access to all containers and management functions.

## Lease Provisioning

### 1. Lease Creation

- WHEN a user requests to lease a new container, THE system SHALL assign the next available container VMID from Proxmox VE.
- The system SHALL provision a new LXC container on the configured node using the specified OS template, storage, and resource specifications.
- The lease record SHALL include:
    - The user identifier.
    - Container VMID.
    - Lease start date and time in ISO 8601 format.
    - Lease end date and time in ISO 8601 format.
    - Allocated resources (RAM in MB, CPU cores, disk size in GB).
- The system SHALL start the container after successful provisioning.

### 2. Lease Validity and Constraints

- Leased containers SHALL have a specific lease duration defined by a start and end date/time.
- When the lease end date/time is reached, THE system SHALL mark the lease as expired and deny access to the container.

## Lease Renewal

- WHEN a user requests to renew a lease before its expiration, THE system SHALL check the container status.
- IF the container is stopped, THE system SHALL start the container upon successful renewal.
- The system SHALL extend the lease end date/time according to the user's renewal request.

## Container Management

### 1. Container Status

- The system SHALL provide APIs to retrieve the status of leased containers:
    - Running
    - Stopped
    - Expired

### 2. Container Lifecycle Actions

- Users SHALL be able to execute commands inside their leased containers via API.
- Users SHALL be able to start and stop their leased containers if their lease is active.
- Admins SHALL be able to perform management operations on any container regardless of lease.

### 3. Console Access

- The system SHALL provide secure VNC proxy tunnels to leased containers.
- Access tokens for VNC proxies SHALL be generated securely per user session.

## Access Control and Paywall Logic

### 1. Access Denial

- WHEN a lease has expired, THE system SHALL deny all access to the associated container.
- THE system SHALL respond with HTTP 403 Forbidden for any attempts to access expired leases.

### 2. Payment Integration Roadmap

- The system SHALL be designed to support future integration of the x402 payment protocol.
- Payment enforcement logic SHALL be isolated as middleware components for easy replacement or upgrade.

## APIs and Functional Endpoints

### 1. Lease Management

- `POST /lease/container` : Create a new lease and provision container.
- `POST /lease/{ctid}/renew` : Renew an existing lease.
- `GET /management/list` : List leased containers for the authenticated user.

### 2. Container Management

- `POST /management/exec/{ctid}` : Execute commands inside container.
- `POST /management/console/{ctid}` : Obtain VNC proxy URL.
- `POST /management/start/{ctid}` : Start a leased container.
- `POST /management/stop/{ctid}` : Stop a leased container.

## Business Rules and Validations

- Leases SHALL NOT be extendable past administrative expiry limits.
- All container resource allocations (RAM, CPU, disk) SHALL respect configured maximums.
- Lease create and renew operations SHALL perform validation of user permissions.
- Access to container management APIs SHALL verify active lease status before proceeding.

## Error Handling

- WHEN authentication fails, THE system SHALL provide a 401 HTTP response.
- WHEN authorization fails, THE system SHALL provide a 403 HTTP response.
- WHEN operations are attempted on expired leases, THE system SHALL deny action with 403 HTTP response.
- Error responses SHALL contain clear messages suitable for client display.

## Security Considerations

- All API communications SHALL use HTTPS.
- API tokens and credentials SHALL be stored securely and encrypted.
- The system SHALL log authorization and authentication attempts for audit purposes.

---

## Mermaid Diagram of Workflow

```mermaid
flowchart TD
    A["User sends lease request"] --> B["System validates Basic Auth"]
    B --> C["System checks existing leases"]
    C --> D["System fetches next VMID from Proxmox"]
    D --> E["System provisions container"]
    E --> F["System starts container"]
    F --> G["Lease record created and stored"]
    G --> H["User accesses container based on lease"]
    H --> I{"Is lease active?"}
    I --|"No"--> J["Deny access with 403 Forbidden"]
    I --|"Yes"--> K["Allow access to container"]
    K --> L["User interacts with container APIs"]
    L --> M["User can renew lease"]
    M --> N["System validates renewal and restarts container if stopped"]
    N --> O["Lease end date extended"]

classDef userStyle fill:#f9f,stroke:#333,stroke-width:2px;
classDef systemStyle fill:#bbf,stroke:#f66,stroke-width:2px;
class A,B,C,D,E,F,G,H,K,L,M,N,O userStyle;
class I,J systemStyle;
```

---

This specification provides all functional requirements for the proxmoxPaywall middleware system, covering user roles, authentication, lease lifecycle, container management, and API interface expectations. It ensures that backend developers have a clear, complete, and implementation-ready blueprint, eliminating ambiguity and guiding future development phases.