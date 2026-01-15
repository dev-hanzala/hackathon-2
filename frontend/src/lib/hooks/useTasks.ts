/**
 * React Query hooks for task operations.
 */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Task, APIError } from '../types';
import { apiClient } from '../api-client';

const TASKS_QUERY_KEY = ['tasks'];

export function useTasks() {
  const queryClient = useQueryClient();

  // Fetch tasks
  const listTasks = useQuery({
    queryKey: TASKS_QUERY_KEY,
    queryFn: async () => {
      // API returns array of tasks directly, not wrapped in object
      const response = await apiClient.get<Task[]>('/tasks');
      return response;
    },
    enabled: true, // Only enable when user is authenticated
  });

  // Create task
  const createTask = useMutation({
    mutationFn: async (title: string) => {
      return apiClient.post<Task>('/tasks', { title });
    },
    onSuccess: (newTask) => {
      queryClient.setQueryData(TASKS_QUERY_KEY, (old: Task[] | undefined) => {
        return [...(old || []), newTask];
      });
    },
    onError: (error: APIError) => {
      console.error('Failed to create task:', error);
    },
  });

  // Get single task
  const getTask = useQuery({
    queryKey: ['task', null],
    queryFn: async ({ queryKey }: { queryKey: any[] }) => {
      const taskId = queryKey[1];
      if (!taskId) return null;
      return apiClient.get<Task>(`/tasks/${taskId}`);
    },
    enabled: false,
  });

  // Update task
  const updateTask = useMutation({
    mutationFn: async ({ id, title }: { id: string; title: string }) => {
      return apiClient.put<Task>(`/tasks/${id}`, { title });
    },
    onSuccess: (updatedTask) => {
      queryClient.setQueryData(TASKS_QUERY_KEY, (old: Task[] | undefined) => {
        return (old || []).map((task) =>
          task.id === updatedTask.id ? updatedTask : task
        );
      });
    },
    onError: (error: APIError) => {
      console.error('Failed to update task:', error);
    },
  });

  // Complete task
  const completeTask = useMutation({
    mutationFn: async (taskId: string) => {
      return apiClient.patch<Task>(`/tasks/${taskId}/complete`, {});
    },
    onMutate: async (taskId) => {
      // Optimistically remove task from list (it gets archived)
      await queryClient.cancelQueries({ queryKey: TASKS_QUERY_KEY });
      const previousTasks = queryClient.getQueryData<Task[]>(TASKS_QUERY_KEY);
      
      queryClient.setQueryData(TASKS_QUERY_KEY, (old: Task[] | undefined) => {
        return (old || []).filter((task) => task.id !== taskId);
      });

      return { previousTasks };
    },
    onError: (error: APIError, _taskId, context) => {
      // Rollback on error
      if (context?.previousTasks) {
        queryClient.setQueryData(TASKS_QUERY_KEY, context.previousTasks);
      }
      console.error('Failed to complete task:', error);
    },
    onSuccess: () => {
      // Invalidate to get fresh data from server
      queryClient.invalidateQueries({ queryKey: TASKS_QUERY_KEY });
    },
  });

  // Incomplete task
  const incompleteTask = useMutation({
    mutationFn: async (taskId: string) => {
      return apiClient.patch<Task>(`/tasks/${taskId}/incomplete`, {});
    },
    onSuccess: (uncompletedTask) => {
      queryClient.setQueryData(TASKS_QUERY_KEY, (old: Task[] | undefined) => {
        return (old || []).map((task) =>
          task.id === uncompletedTask.id ? uncompletedTask : task
        );
      });
    },
    onError: (error: APIError) => {
      console.error('Failed to mark task incomplete:', error);
    },
  });

  // Delete task
  const deleteTask = useMutation({
    mutationFn: async (taskId: string) => {
      return apiClient.delete(`/tasks/${taskId}`);
    },
    onSuccess: (_, taskId) => {
      queryClient.setQueryData(TASKS_QUERY_KEY, (old: Task[] | undefined) => {
        return (old || []).filter((task) => task.id !== taskId);
      });
    },
    onError: (error: APIError) => {
      console.error('Failed to delete task:', error);
    },
  });

  return {
    // Queries
    tasks: listTasks.data || [],
    isLoadingTasks: listTasks.isLoading,
    isLoadingTask: getTask.isLoading,
    error: listTasks.error || getTask.error,

    // Mutations
    createTask,
    updateTask,
    completeTask,
    incompleteTask,
    deleteTask,

    // Utilities
    refetch: listTasks.refetch,
  };
}
