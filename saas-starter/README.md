# SaaS Starter - Educational Multi-Tenant Architecture

A minimal, type-safe SaaS boilerplate designed for **bottom-up learning**. This project demonstrates how multi-tenancy and data isolation work at the code level using modern full-stack technologies.

## Purpose

This is a learning resource that shows:
- How to implement **organization-scoped data isolation** in a SaaS application
- The critical path: **Data Request → API Endpoint → DB Query → UI Render**
- Modern async patterns with FastAPI and React Query
- Type-safe development with Pydantic V2 and TypeScript

## Tech Stack

### Backend
- **FastAPI** - High-performance async Python framework
- **SQLAlchemy 2.0** - Modern ORM with type hints
- **Pydantic V2** - Data validation and serialization
- **SQLite** - Portable database for development

### Frontend
- **React 18** - Modern UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **TanStack Query (React Query)** - Powerful async state management
- **Vite** - Fast build tool

## Architecture Overview

### The SaaS "Golden Rule"

**Every piece of data belongs to an Organization, not just a user.**

This is implemented at three layers:

1. **Database Layer** (`backend/main.py:38-44`)
   - Every `Task` has an `organization_id` foreign key
   - Physical data isolation at the schema level

2. **API Layer** (`backend/main.py:91-104`)
   - `get_current_org()` dependency validates ownership before route execution
   - Security: Organization ID comes from validated context, never user input
   - Logical isolation through dependency injection

3. **UI Layer** (`frontend/src/App.tsx:34-42`)
   - `activeOrgId` drives React Query's cache keys
   - Switching organizations triggers automatic data refetch
   - Context-aware state management

## Project Structure

```
/saas-starter
├── /backend
│   ├── main.py          # Single-file backend: models, schemas, routes, and DB
│   └── requirements.txt # Python dependencies
├── /frontend
│   ├── src/
│   │   ├── App.tsx      # Main UI with organization switcher and tasks
│   │   ├── main.tsx     # React entry point
│   │   └── index.css    # Tailwind directives
│   ├── index.html       # Vite entry point
│   ├── package.json     # Node dependencies
│   ├── vite.config.ts   # Vite configuration
│   ├── tsconfig.json    # TypeScript configuration
│   ├── tailwind.config.js
│   └── postcss.config.js
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### 1. Start the Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API will run at `http://localhost:8000`

### 2. Start the Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The UI will run at `http://localhost:5173`

### 3. Try It Out

1. Open `http://localhost:5173` in your browser
2. Click "Create Org" to create your first organization
3. Select the organization from the sidebar
4. Add tasks to see organization-scoped data isolation in action
5. Create another organization and switch between them to see data isolation

## Educational Deep Dive

### How Multi-Tenancy Works

#### 1. User Authentication (Mock)
```python
# backend/main.py:76-84
def get_current_user(x_user_id: int = Header(...), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == x_user_id))
    if not user:
        # Auto-create user for demo simplicity
        user = User(id=x_user_id, email=f"user{x_user_id}@example.com")
        db.add(user)
        db.commit()
    return user
```

In production, replace this with JWT validation:
- Decode JWT token from `Authorization` header
- Extract user ID from token claims
- Validate signature and expiration

#### 2. Organization Context Validation
```python
# backend/main.py:91-104
def get_current_org(
    x_org_id: Optional[int] = Header(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not x_org_id:
        return None
    org = db.scalar(select(Organization).where(
        Organization.id == x_org_id,
        Organization.owner_id == user.id  # ← Security: Validate ownership
    ))
    if not org:
        raise HTTPException(status_code=403, detail="Access to Organization denied")
    return org
```

This dependency:
- Runs **before** the route handler
- Validates that the user owns the organization
- Returns 403 if validation fails
- Provides type-safe `Organization` object to the route

#### 3. Scoped Database Queries
```python
# backend/main.py:143-145
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(org: Organization = Depends(get_current_org), db: Session = Depends(get_db)):
    return db.scalars(select(Task).where(Task.organization_id == org.id)).all()
```

Notice:
- `org.id` comes from the validated dependency, **never from user input**
- Query is automatically scoped to the organization
- Impossible to access another organization's data

#### 4. UI State Management
```typescript
// frontend/src/App.tsx:34-42
const { data: tasks, isLoading: tasksLoading } = useQuery({
  queryKey: ['tasks', activeOrgId],  // ← Cache key includes org ID
  queryFn: async () => {
    if (!activeOrgId) return [];
    const res = await API.get<Task[]>('/tasks', {
      headers: { 'x-user-id': userId, 'x-org-id': activeOrgId }
    });
    return res.data;
  },
  enabled: !!activeOrgId,  // ← Only fetch if org is selected
});
```

When `activeOrgId` changes:
1. React Query invalidates the old cache
2. Automatically triggers a new fetch with updated headers
3. UI re-renders with organization-specific data

### Critical Path Walkthrough

Let's trace a request to create a task:

1. **User Action** (UI)
   ```typescript
   createTask.mutate(newTask)
   ```

2. **API Request** (Network)
   ```
   POST http://localhost:8000/tasks
   Headers: { x-user-id: 1, x-org-id: 2 }
   Body: { title: "Build feature X" }
   ```

3. **Dependency Chain** (Backend)
   ```
   get_db() → get_current_user() → get_current_org() → create_task()
   ```

4. **Security Validation** (Backend)
   - `get_current_user()`: Verify user exists
   - `get_current_org()`: Verify user owns org ID 2

5. **Database Insert** (Backend)
   ```python
   new_task = Task(
       title=task.title,
       organization_id=org.id  # From validated context!
   )
   ```

6. **Response** (Network)
   ```json
   { "id": 5, "title": "Build feature X", "status": "pending" }
   ```

7. **Cache Invalidation** (UI)
   ```typescript
   onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tasks'] })
   ```

8. **UI Update** (React)
   - Task list automatically refetches
   - New task appears in the UI

## Production Considerations

This is an educational starter. For production, add:

### Security
- [ ] Real JWT authentication (replace mock `x-user-id` header)
- [ ] HTTPS/TLS encryption
- [ ] Rate limiting
- [ ] Input sanitization
- [ ] CSRF protection
- [ ] Content Security Policy headers

### Database
- [ ] Switch to PostgreSQL
- [ ] Add database migrations (Alembic)
- [ ] Implement soft deletes
- [ ] Add indexes on foreign keys
- [ ] Connection pooling

### Multi-Tenancy Enhancements
- [ ] Role-Based Access Control (RBAC)
- [ ] Team members (not just owners)
- [ ] Audit logging
- [ ] Data export/import
- [ ] Organization billing

### Infrastructure
- [ ] Docker containers
- [ ] CI/CD pipeline
- [ ] Monitoring and logging
- [ ] Error tracking (Sentry)
- [ ] Backup strategy

## Learning Exercises

Try these to deepen your understanding:

1. **Add a new entity**
   - Create a `Project` model that belongs to an organization
   - Add API endpoints and UI for managing projects
   - Ensure proper data isolation

2. **Implement team members**
   - Create a `Membership` join table (User ↔ Organization)
   - Update `get_current_org()` to check membership, not just ownership
   - Add invite/remove member endpoints

3. **Add real JWT authentication**
   - Use `python-jose` to create and verify JWTs
   - Replace the `x-user-id` header with `Authorization: Bearer <token>`
   - Implement login/logout endpoints

4. **Upgrade to PostgreSQL**
   - Change `DATABASE_URL` to PostgreSQL connection string
   - Test that isolation still works with concurrent users

5. **Add RBAC**
   - Create a `Role` enum (Owner, Admin, Member, Viewer)
   - Add permission checks to routes
   - Update UI to show/hide actions based on role

## Key Takeaways

1. **Multi-tenancy is about isolation**: Every query must filter by organization ID
2. **Never trust user input**: Organization context comes from validated dependencies
3. **Type safety matters**: Pydantic and TypeScript catch errors at compile time
4. **State management is critical**: React Query handles caching and refetching automatically
5. **Simplicity first**: This starter favors readability over abstraction

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [TanStack Query Guide](https://tanstack.com/query/latest/docs/react/overview)
- [Multi-Tenancy Patterns](https://docs.microsoft.com/en-us/azure/architecture/guide/multitenant/overview)

## License

MIT - Feel free to use this for learning and building your own SaaS applications.

---

**Built for learners who want to understand SaaS architecture from the ground up.**
