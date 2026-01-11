/**
 * Shared TypeScript types for the frontend application.
 */

export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  user_id: string;
  title: string;
  completed: boolean;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthContext {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface TasksResponse {
  tasks: Task[];
  total: number;
}

export interface APIError {
  detail: string;
  code?: string;
  status?: number;
}
