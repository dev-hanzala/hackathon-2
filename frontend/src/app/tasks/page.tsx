'use client';

/**
 * Tasks page - displays user's tasks (protected route).
 * User Story 2: View All Tasks
 */

import { ProtectedRoute } from '@/components/ProtectedRoute';
import { TaskList } from '@/components/TaskList';
import { TaskForm } from '@/components/TaskForm';
import { useAuthContext } from '@/components/AuthProvider';
import { useTasks } from '@/lib/hooks/useTasks';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function TasksPage() {
  const { user, logout } = useAuthContext();
  const router = useRouter();
  const { tasks, isLoadingTasks, error, createTask, completeTask, updateTask, deleteTask } =
    useTasks();
  const [successMessage, setSuccessMessage] = useState('');

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  const handleCreateTask = async (title: string) => {
    try {
      await createTask.mutateAsync(title);
      setSuccessMessage('Task created successfully!');
      setTimeout(() => setSuccessMessage(''), 3000); // Clear after 3 seconds
    } catch (err) {
      console.error('Failed to create task:', err);
    }
  };

  const handleCompleteTask = async (taskId: string) => {
    try {
      await completeTask.mutateAsync(taskId);
      setSuccessMessage('Task marked as complete!');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      console.error('Failed to complete task:', err);
    }
  };

  const handleEditTask = async (taskId: string, newTitle: string) => {
    try {
      await updateTask.mutateAsync({ id: taskId, title: newTitle });
      setSuccessMessage('Task updated successfully!');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await deleteTask.mutateAsync(taskId);
      setSuccessMessage('Task deleted successfully!');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation Bar */}
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div>
                <h1 className="text-xl font-bold text-gray-900">My Tasks</h1>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-600 hidden sm:inline">
                  {user?.email}
                </span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Your Tasks</h2>
              <p className="text-sm text-gray-600 mt-1">
                View and manage your todo list
              </p>
            </div>

            {/* Success Message */}
            {successMessage && (
              <div className="mb-4 bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center">
                  <svg
                    className="w-5 h-5 text-green-600 mr-3"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <p className="text-sm font-medium text-green-800">{successMessage}</p>
                </div>
              </div>
            )}

            {/* Task Form */}
            <TaskForm
              onSubmit={handleCreateTask}
              isSubmitting={createTask.isPending}
            />

            {/* Task List */}
            <TaskList
              tasks={tasks}
              isLoading={isLoadingTasks}
              error={error as Error | null}
              onComplete={handleCompleteTask}
              onEdit={handleEditTask}
              onDelete={handleDeleteTask}
            />
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
