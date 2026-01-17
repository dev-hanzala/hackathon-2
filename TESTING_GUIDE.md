# Testing Guide: Todo Evolution App

## Quick Start (TL;DR)

```bash
# Terminal 1 - Start Backend
cd /home/hanza/hackathon-2/backend
uv run uvicorn src.main:app --reload

# Terminal 2 - Start Frontend
cd /home/hanza/hackathon-2/frontend
pnpm dev

# Open browser: http://localhost:3000
```

---

## Prerequisites Check

Before testing, ensure you have:
- [X] Python 3.11+ installed
- [X] Node.js 18+ installed
- [X] uv installed (backend package manager)
- [X] pnpm installed (frontend package manager)
- [X] PostgreSQL database (local or Neon cloud)

### Install Missing Tools

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install pnpm (if not installed)
npm install -g pnpm

# Verify installations
uv --version
pnpm --version
node --version
python --version
```

---

## Step 1: Setup Backend

### 1.1 Navigate to Backend Directory
```bash
cd /home/hanza/hackathon-2/backend
```

### 1.2 Install Dependencies
```bash
uv sync
```

### 1.3 Configure Environment
```bash
# Check if .env file exists
ls -la .env

# If not, copy from example
cp .env.example .env
```

**Edit `.env` file** (if needed):
```bash
# Minimal configuration for local testing
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long-for-testing-12345
DEBUG=true
ENVIRONMENT=development
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

### 1.4 Start Backend Server
```bash
uv run uvicorn src.main:app --reload
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/home/hanza/hackathon-2/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Backend is ready when you see:**
- ✅ "Application startup complete"
- ✅ Running on http://127.0.0.1:8000

**Test Backend API:**
Open browser to http://localhost:8000/health - should see:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "database": "connected"
}
```

---

## Step 2: Setup Frontend

### 2.1 Open New Terminal
Keep backend running, open a new terminal window/tab

### 2.2 Navigate to Frontend Directory
```bash
cd /home/hanza/hackathon-2/frontend
```

### 2.3 Install Dependencies
```bash
pnpm install
```

### 2.4 Configure Environment
```bash
# Check if .env.local file exists
ls -la .env.local

# If not, create it
cat > .env.local <<'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_DEBUG=true
EOF
```

### 2.5 Start Frontend Development Server
```bash
pnpm dev
```

**Expected Output:**
```
  ▲ Next.js 16.1.2
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 2.3s
```

**Frontend is ready when you see:**
- ✅ "Ready in X.Xs"
- ✅ Local: http://localhost:3000

---

## Step 3: Test the New Landing Page

### 3.1 Open Browser
Navigate to: **http://localhost:3000**

### 3.2 Landing Page Checklist

**Visual Verification:**
- [ ] See header with "Todo Evolution" title and theme toggle button
- [ ] See large "Todo Evolution" heading in hero section
- [ ] See tagline: "Your personal productivity companion"
- [ ] See two CTA buttons: "Get Started" (blue) and "Sign In" (outlined)
- [ ] See "Why Choose Todo Evolution?" section
- [ ] See 3 feature cards:
  - Quick Task Creation (with checkmark icon)
  - Task Organization (with list icon)
  - Progress Tracking (with trending up icon)
- [ ] See footer CTA: "Ready to boost your productivity?"
- [ ] See copyright footer

### 3.3 Test Dark Mode Toggle

**In header, click the sun/moon icon:**
1. Click theme toggle button (sun icon in light mode)
2. Page should instantly switch to dark theme
3. Click again - should switch back to light theme
4. Refresh page (Ctrl+R or Cmd+R)
5. Theme preference should persist (stays dark if you left it dark)

**Expected Behavior:**
- ✅ Toggle switches theme in <200ms (instant feel)
- ✅ Colors change smoothly across all sections
- ✅ Icons change (sun ↔ moon)
- ✅ Preference persists after page refresh

### 3.4 Test Navigation

**Click "Get Started" button:**
- Should navigate to: http://localhost:3000/auth/signup
- Should see signup form

**Click "Sign In" button:**
- Should navigate to: http://localhost:3000/auth/signin
- Should see signin form

---

## Step 4: Test Full User Flow

### 4.1 Create Account
1. From landing page, click **"Get Started"**
2. Fill in signup form:
   - Email: `test@example.com`
   - Password: `TestPassword123!`
   - Confirm Password: `TestPassword123!`
3. Click **"Sign Up"**
4. Should automatically sign you in and redirect to `/tasks`

### 4.2 Create Tasks
1. On tasks page, find the task creation form
2. Enter task title: "Buy groceries"
3. Click "Add Task" or press Enter
4. Task should appear in the list below

### 4.3 Manage Tasks
- [ ] **Mark Complete**: Click checkbox next to task
- [ ] **Edit Task**: Click edit icon, modify title
- [ ] **Delete Task**: Click delete/trash icon
- [ ] **View All Tasks**: Should see all your tasks in a list

### 4.4 Test Authenticated Landing Page Redirect
1. While signed in, navigate to http://localhost:3000
2. Should automatically redirect to http://localhost:3000/tasks
3. Should NOT see landing page (you're already signed in)

### 4.5 Test Sign Out
1. Find "Sign Out" button (usually in header/nav)
2. Click "Sign Out"
3. Should redirect back to landing page
4. Should see landing page content again (not tasks)

---

## Step 5: Test Responsive Design

### 5.1 Desktop View (Default)
- Landing page should have good spacing
- Features should be in 3 columns side-by-side
- CTAs should be horizontal

### 5.2 Mobile View
**Resize browser window to ~375px wide OR use DevTools:**
1. Open DevTools (F12 or Cmd+Option+I)
2. Click device toolbar icon (toggle device toolbar)
3. Select "iPhone SE" or "iPhone 12 Pro"
4. Verify:
   - [ ] Header fits properly
   - [ ] Hero text is readable
   - [ ] CTA buttons stack vertically
   - [ ] Features stack in single column
   - [ ] All text is readable (not cut off)
   - [ ] Theme toggle still works

---

## Step 6: Test API Documentation

### 6.1 Interactive API Docs
Navigate to: **http://localhost:8000/api/v1/docs**

**You should see:**
- Swagger UI with all API endpoints
- Authentication endpoints (register, signin, logout)
- Tasks endpoints (create, read, update, delete, complete)

**Try an endpoint:**
1. Expand `POST /api/v1/auth/register`
2. Click "Try it out"
3. Fill in example data
4. Click "Execute"
5. Should see response with status code and data

---

## Troubleshooting

### Backend Issues

**"Database connection failed"**
```bash
# Check if PostgreSQL is running (if using local DB)
psql -U postgres -c "SELECT 1"

# Or use SQLite for testing (edit .env):
DATABASE_URL=sqlite:///./todo.db
```

**"Module not found"**
```bash
# Reinstall dependencies
cd backend
rm -rf .venv
uv sync
```

**"Port 8000 already in use"**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uv run uvicorn src.main:app --reload --port 8001
# Update frontend .env.local: NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Frontend Issues

**"Cannot connect to API"**
```bash
# Check .env.local has correct backend URL
cat frontend/.env.local

# Should show:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Verify backend is running:
curl http://localhost:8000/health
```

**"Port 3000 already in use"**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
pnpm dev -- --port 3001
```

**"Module not found" or build errors**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules .next
pnpm install
pnpm dev
```

### Theme Not Persisting

**Clear browser data:**
1. Open DevTools (F12)
2. Go to Application tab
3. Expand Local Storage
4. Find http://localhost:3000
5. Clear all items
6. Refresh page

---

## Testing Checklist Summary

### Must-Test Features ✅

**Landing Page (US1):**
- [X] Landing page loads at http://localhost:3000
- [X] Theme toggle switches light/dark modes
- [X] Theme preference persists after refresh
- [X] "Get Started" navigates to /auth/signup
- [X] "Sign In" navigates to /auth/signin
- [X] 3 feature cards display correctly
- [X] Responsive on mobile/tablet/desktop
- [X] Authenticated users redirect to /tasks

**Dark Mode (US2):**
- [X] Theme toggle in header
- [X] Colors change across entire page
- [X] Sun/moon icons animate
- [X] Preference saved in localStorage
- [X] Works on all pages

**Authentication:**
- [X] Can register new account
- [X] Can sign in with existing account
- [X] Can sign out
- [X] Protected routes redirect to signin

**Task Management:**
- [X] Can create tasks
- [X] Can view task list
- [X] Can mark tasks complete
- [X] Can edit tasks
- [X] Can delete tasks

---

## Additional Testing Tools

### Run Tests

**Backend Tests:**
```bash
cd backend
uv run pytest tests/ -v
```

**Frontend Tests:**
```bash
cd frontend
pnpm test
```

### Type Checking

**Backend Type Check:**
```bash
cd backend
uv run mypy src/
```

**Frontend Type Check:**
```bash
cd frontend
pnpm run type-check
```

### Linting

**Backend Linting:**
```bash
cd backend
uv run ruff check .
```

**Frontend Linting:**
```bash
cd frontend
pnpm run lint
```

---

## What to Look For

### ✅ Success Indicators
- Landing page loads with modern design
- Theme toggle works instantly (<200ms)
- All navigation links work
- Feature cards display with icons
- Page is responsive on all screen sizes
- Dark mode persists after refresh
- No console errors in browser DevTools

### ❌ Potential Issues to Report
- Broken images or icons
- Console errors (check DevTools F12)
- Slow theme switching (>200ms)
- Layout breaks on mobile
- Navigation doesn't work
- Theme doesn't persist
- Text hard to read in dark mode

---

## Need Help?

**Check logs:**
- Backend logs: Terminal 1 (where uvicorn is running)
- Frontend logs: Terminal 2 (where pnpm dev is running)
- Browser logs: DevTools Console (F12)

**Common Commands:**
```bash
# Restart backend
# In Terminal 1: Ctrl+C, then:
uv run uvicorn src.main:app --reload

# Restart frontend
# In Terminal 2: Ctrl+C, then:
pnpm dev

# Check what's running on ports
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
```

---

**Happy Testing! 🎉**

The new landing page should look modern, professional, and work perfectly in both light and dark modes!
