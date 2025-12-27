# Table of Contents for ProxmoxPaywall Backend System

This document provides the comprehensive overview of all project documentation files for the ProxmoxPaywall backend middleware system implementing paywall and leasing functionality for Proxmox VE containers. It describes the structure and purpose of each document to assist backend developers in navigating the full product specification.

## Project Documentation Files

| Document Title | Filename | Purpose Overview |
| --- | --- | --- |
| Service Overview | 01-service-overview.md | Defines the business motivation, model, and core goals of the Paywall Middleware for Proxmox VE container leasing. |
| User Actors and Authentication | 02-user-actors.md | Defines user actors, authentication mechanisms, permissions, and roles for the system. |
| Functional Requirements | 03-functional-requirements.md | Describes all functional requirements including lease creation, renewal, listing, and container management. |
| Business Rules and Validation | 04-business-rules.md | Specifies core business rules and validation logic related to leasing conditions, expiration, and system restrictions. |
| User Scenarios | 05-user-scenarios.md | Illustrates primary and secondary user workflows including leasing, renewal, and error handling processes. |
| Error Handling and Recovery | 06-error-handling.md | Documents system behaviors on errors, expired leases, authentication failures, and access violations. |
| Performance Requirements | 07-performance-requirements.md | Outlines user experience and system responsiveness expectations for all main operations. |
| Security and Compliance | 08-security-compliance.md | Describes security requirements including authentication, authorization, data protection, and compliance. |
| External Integrations and API | 09-external-integrations.md | Describes the integration with Proxmox VE API and preparation for future payment protocol implementation. |
| Data Flow and Lifecycle | 10-data-flow.md | Explains how data flows through the paywall system from authentication to container provisioning and lease monitoring. |

## Notes

* This document provides business requirements only.
* All technical implementation decisions belong to developers.
* Developers have full autonomy over architecture, APIs, and database design.
* The document describes WHAT the system should do, not HOW to build it.

> *Developer Note: This document defines **business requirements only**. All technical implementations (architecture, APIs, database design, etc.) are at the discretion of the development team.*
