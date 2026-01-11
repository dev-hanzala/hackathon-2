/**
 * Auth hook for managing authentication state.
 */

import { useEffect, useState } from 'react';
import { User, AuthResponse, APIError } from '../types';
import { apiClient } from '../api-client';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  // Check for existing session on mount
  useEffect(() => {
    const checkSession = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        const userJSON = localStorage.getItem('auth_user');

        if (token && userJSON) {
          const user = JSON.parse(userJSON);
          setState({
            user,
            token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } else {
          setState((prev) => ({ ...prev, isLoading: false }));
        }
      } catch (error) {
        setState({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
          error: 'Failed to restore session',
        });
      }
    };

    checkSession();
  }, []);

  const signup = async (email: string, password: string) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await apiClient.post<AuthResponse>('/auth/register', {
        email,
        password,
      });

      apiClient.setToken(response.token);
      localStorage.setItem('auth_user', JSON.stringify(response.user));

      setState({
        user: response.user,
        token: response.token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });

      return response;
    } catch (error) {
      const apiError = error as APIError;
      const errorMsg = apiError.detail || 'Signup failed';

      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMsg,
      }));

      throw error;
    }
  };

  const signin = async (email: string, password: string) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await apiClient.post<AuthResponse>('/auth/signin', {
        email,
        password,
      });

      apiClient.setToken(response.token);
      localStorage.setItem('auth_user', JSON.stringify(response.user));

      setState({
        user: response.user,
        token: response.token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });

      return response;
    } catch (error) {
      const apiError = error as APIError;
      const errorMsg = apiError.detail || 'Sign in failed';

      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMsg,
      }));

      throw error;
    }
  };

  const logout = async () => {
    setState((prev) => ({ ...prev, isLoading: true }));

    try {
      await apiClient.post('/auth/logout', {});
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      apiClient.clearToken();
      localStorage.removeItem('auth_user');

      setState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    }
  };

  return {
    ...state,
    signup,
    signin,
    logout,
  };
}
