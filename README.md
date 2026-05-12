Alfred is a local AI assistant project built for learning LLM and tooling around them.

## Goal

Build a local AI assistant that can:

- understand speech
- process user queries using a local LLaMA-based model
- use tools to perform useful tasks
- maintain useful memory/context
- respond with both text and voice
- expose everything through a sleek Svelte frontend
- home automation at some point (controlling lights, TVs, thermostat)

## Main Learning Areas

### LLM / AI Assistant Architecture

I want to learn how applications interact with LLMs and how LLMs works in practice:

- how to send prompts/messages to an LLM
- how chat history affects responses
- how much previous conversation should be passed in
- when to pass full history vs relevant history only
- how to compact/summarize older context
- how memory changes the assistant’s usefulness
- how tool-calling lets the model perform real tasks
- how context quality affects output quality

I believe the next big progress is around tooling rather then model improvement. Personally I think a model like `qwen3.5-9B` should be plenty fine for daily tasks. Tooling is the way to make it shine.

### Postgres

I mainly come from a SQL Server background, so this project is also a way to learn PostgreSQL:

- PostgreSQL syntax
- schemas/tables/indexes
- JSON support
- full-text search
- migrations
- storing chat history, memories, tool calls, and metadata

Also since PostgreSQL supports vector storage through pgvector, at some point I would like to explore:
- store embeddings for memories/documents
- retrieve relevant information semantically
- search previous conversations by meaning instead of keywords
- inject only relevant context into the LLM

### FastAPI

Since I mainly work with C#/.NET, Alfred is also a way to learn FastAPI:

- building Python APIs
- async endpoints
- request/response models (pydantic ...)
- getting more familiar with python in general

### Svelte

Since I mainly use React, this project is a way to learn Svelte:

- Svelte component structure
- state management
- streaming responses
- audio input/output controls
- creating a clean mobile friendly assistant-style frontend 

### Speech / Voice

- speech-to-text for user input
- text-to-speech for assistant responses
- possibly streaming audio later

### Nginx

Use Nginx to better understand how modern applications are exposed and routed in production environments.

Main goals:

- reverse proxying
- serving frontend + backend together
- routing API traffic
- handling websocket/streaming connections
- SSL/TLS termination later on
- understanding production deployment flow

### Docker

I also want to get more familiar with docker so I am planning to use it for both development and production workflows:

- local development containers (Postgres, FastAPI, Svelte, Nginx)
- production-style Docker Compose setup
- environment variables and volumes