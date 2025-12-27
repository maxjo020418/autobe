# Requirement Analysis for Paywall Middleware in Proxmox VE Container Leasing

## 1. Introduction

### 1.1 Purpose of the Document

This document defines the comprehensive set of requirements and constraints for developing a paywall middleware system that manages container leasing on a Proxmox VE infrastructure.

### 1.2 Scope of the System

The system is designed to authenticate users, manage leases for containers with detailed system specs, and directly interact with Proxmox VE API to provision and control container lifecycle. It enforces leasing rules such as lease expirations denying user access.

## 2. Actors and Roles

### 2.1 Admin

* System administrators with full control over user management, lease provisioning, container lifecycle management, and system settings.

### 2.2 User

* Authenticated users who lease containers and manage their own leases, including viewing container specs and lease status.

### 2.3 Authentication Mechanisms

* Basic authentication tying users to leased containers.

## 3. Functional Requirements

### 3.1 User Registration and Authentication

* Support for basic user authentication with role-based access control (admin, user).

### 3.2 Container Leasing Management

* Lease Creation: Ability for users/admin to request a new container lease. System obtains next available VMID from Proxmox VE and provisions container.
* Lease Renewal: Users can renew leases before or after expiry; middleware verifies container status and starts container if stopped.
* Lease Expiry: Automatic detection and denial of access if the lease has expired. System stops container if required.

### 3.3 Container Lifecycle Management

* Direct interaction with Proxmox VE API endpoints for cluster operations including create, start, stop, exec, vncproxy, and task status.

### 3.4 API Endpoints and Actions

* POST /lease/container: Create Lease
* POST /lease/{ctid}/renew: Renew Lease
* GET /management/list: List User Containers
* POST /management/exec/{ctid}: Run Command
* POST /management/console/{ctid}: Get Console URL

## 4. Business Rules

### 4.1 Lease Expiration

* Access denied to users on expired leases.

### 4.2 Resource Specifications

* Lease records must include lease end date, RAM, CPU, disk info associated with containers.

### 4.3 Permissions

* Admins have full control; users have restricted control limited to their own leases.

## 5. Integration with Proxmox VE

### 5.1 API Endpoint Interactions

* Utilize provided Proxmox endpoints for cluster next ID, LXC creation, status management, command execution, VNC access, and task monitoring.

### 5.2 Environment Variables

* Required .env variables include PVE_HOST, PVE_TOKEN_ID, PVE_TOKEN_SECRET, PVE_NODE, PVE_STORAGE, PVE_OS_TEMPLATE, PVE_ROOT_PASSWORD, PVE_VERIFY_SSL.

### 5.3 API Permissions

* Token must have permissions like PVEVMAdmin, Datastore.AllocateSpace.

## 6. Security Considerations

### 6.1 Authentication Security

* Secure basic auth and token validation.

### 6.2 Authorization

* Role-based access controls.

## 7. API Details

* Detailed API routes with methods and respective proxmox API mappings.

## 8. Future Expansion

* Placeholder for implementing x402 payment protocol for actual payments and enforcement.

## 9. Appendices

* Glossary of terms
* References to Proxmox VE documentation and API specs

---

This requirement analysis reflects all provided inputs and adheres to the purpose of guiding backend developers in building the middleware.