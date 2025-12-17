# Fiordispino TUI 🖥️🎮

Fiordispino TUI is a **Text User Interface (TUI)** client designed to interact with the **Fiordispino REST API**.  
It provides a fast, keyboard-driven way to manage your video game backlog and completed games directly from the terminal.

The TUI acts as a **thin client**, delegating all business logic, validation, and state consistency to the Fiordispino backend.

---

## ✨ Features

### 🔐 Authentication
- User registration and login
- Token-based authentication
- Secure token storage for persistent sessions

---

### 🎮 Game Catalogue Browsing
- Browse the global game catalogue
- View detailed game information:
  - Title
  - Description
  - Genres
  - PEGI rating
  - Release date
  - Global rating
- Discover games via **random selection**

---

### 🕹️ Backlog Management
- View your **Games to Play** list
- Add games from the catalogue to your backlog
- Remove games from the backlog
- Backend-enforced integrity:
  - completed games cannot be re-added unless moved back explicitly

---

### 🏆 Played Games Diary
- View your **Played Games** list
- Move games from backlog to played
- Assign a **mandatory personal rating (1–10)**
- Move played games back to the backlog for replay

---

### 🔄 Game Workflow
The TUI exposes the backend workflow in a clear and guided way:

- **Backlog → Played** (rating required)
- **Played → Backlog** (optional replay)

Illegal state transitions are prevented by the backend and surfaced as user-friendly error messages.

---

### 👥 Social Exploration
- Inspect other users’ public libraries
- View:
  - their backlog
  - their played games
- Access via username-based navigation

---

## ⌨️ User Experience

- Fully keyboard-driven interface
- Clear navigation between views
- Context-aware actions and prompts
- Immediate feedback on API errors or validation failures

Designed for speed, clarity, and minimal distractions.

---

## 🧠 Architecture

- **TUI Client**: presentation layer only
- **Fiordispino API**: business logic, validation, persistence

This strict separation ensures:
- consistency of game states
- single source of truth
- easy client extensibility (CLI, mobile, web)

---

## 🛠️ Tech Stack

- **Python**
- Terminal UI framework (e.g. `Textual`, `urwid`, or similar)
- HTTP client for REST interaction
- Token-based authentication

---

## 🚀 Getting Started

1. Ensure the **Fiordispino backend** is running.
2. Configure the API base URL.
3. Launch the TUI application.
4. Register or log in.
5. Start managing your game library from the terminal.

---

## 📌 Use Cases

- Terminal-first users
- Remote or low-bandwidth environments
- Fast backlog management without a browser
- Power users who prefer keyboard navigation

---

## 🧾 Summary

Fiordispino TUI brings the full power of the Fiordispino backend to the terminal, offering a lightweight yet complete interface for tracking, rating, and discovering video games — all while preserving strict workflow and data integrity.
