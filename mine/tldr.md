# AutoBE - Project Overview (TL;DR)

**AutoBE** is an AI-powered system that autonomously generates production-ready backend applications from natural language descriptions. It acts as an "AI Backend Developer," handling everything from requirements analysis to code implementation and testing.

## 🚀 Core Value Proposition
*   **Text-to-Backend:** Converts chat conversations into full-stack backend code (NestJS, Prisma, TypeScript).
*   **100% Compilation Guarantee:** Unlike standard LLM code generation, AutoBE verifies all outputs against custom compilers, fixing errors iteratively until the code is valid.
*   **Type-Safety:** Generates end-to-end type-safe code, including database schemas, API contracts, and client SDKs.
*   **Self-Healing:** Uses a "Waterfall + Spiral" methodology where each phase (Analysis, DB Design, API, etc.) has an internal feedback loop to correct errors automatically.

## 🏗 Architecture
AutoBE is a **monorepo** managed with `pnpm`, organized into core packages and consumer applications.

### Key Packages (`/packages`)
1.  **`@autobe/agent`**: The "brain" of the operation. Orchestrates the 5-phase development pipeline, manages LLM context, and handles function calling via the **Agentica** framework.
2.  **`@autobe/compiler`**: The validation engine. Contains specialized compilers for:
    *   **Prisma**: Validates schemas and generates ERDs.
    *   **Interface (OpenAPI)**: Validates API specs and generates NestJS boilerplate.
    *   **TypeScript**: Verifies final code integrity.
3.  **`@autobe/interface`**: The foundation. Defines all shared types, events (`AutoBeEvent`), and contracts. It has *zero* dependencies, ensuring strict type propagation upwards.
4.  **`@autobe/rpc`**: Handles communication between the AI agents and clients (Web/VSCode) using WebSocket and `tgrid`.
5.  **`@autobe/filesystem`**: A virtual file system that allows agents to "write" and "read" code in memory before committing to disk.

### Applications (`/apps`)
*   **`playground-*`**: A web-based local environment to chat with AutoBE and visualize the generation process.
*   **`hackathon-*`**: A production-grade demonstration platform showcasing AutoBE's capabilities.
*   **`vscode-extension`**: Allows developers to use AutoBE directly within their IDE.

## 🔄 The 5-Phase Pipeline
AutoBE follows a strict sequence to ensure quality, but iterates internally:

1.  **Analyze**: Converts user chat -> Structured Requirement Docs (Actors, Use Cases).
2.  **Prisma**: Requirements -> Database Schema (Prisma) + ERD.
3.  **Interface**: Schema -> OpenAPI Specification (API Endpoints, DTOs).
4.  **Test**: OpenAPI -> E2E Test Suites (validating every endpoint).
5.  **Realize**: Test/Spec -> Actual NestJS Implementation (Controllers, Services).

## 🛠 Tech Stack
*   **Language**: TypeScript (Strict Mode)
*   **Runtime**: Node.js
*   **Framework**: NestJS (Server), React (UI)
*   **ORM**: Prisma
*   **Communication**: WebSocket (RPC via TGrid)
*   **AI/LLM**: Agentica (wrapping Claude/OpenAI/Gemini)
*   **Tools**: Typia (Runtime Validation), Nestia (SDK Generation)
