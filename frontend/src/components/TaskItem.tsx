'use client';

/**
 * TaskItem component - displays a single task with actions.
 */

import { useState } from 'react';
import { Task } from '@/lib/types';
import { TaskEditForm } from './TaskEditForm';

interface TaskItemProps {
  task: Task;
  onComplete?: (taskId: string) => void;
  onEdit?: (taskId: string, newTitle: string) => void;
  onDelete?: (taskId: string) => void;
  isUpdating?: boolean;
  isDeleting?: boolean;
}

export function TaskItem({
  task,
  onComplete,
  onEdit,
  onDelete,
  isUpdating,
  isDeleting,
}: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleSave = (taskId: string, newTitle: string) => {
    onEdit?.(taskId, newTitle);
    setIsEditing(false);
  };

  const handleDelete = () => {
    onDelete?.(task.id);
    setShowDeleteConfirm(false);
  };

  // Edit mode
  if (isEditing) {
    return (
      <div className="flex items-center gap-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <TaskEditForm
          taskId={task.id}
          currentTitle={task.title}
          onSave={handleSave}
          onCancel={() => setIsEditing(false)}
          isSubmitting={isUpdating}
        />
      </div>
    );
  }

  // Delete confirmation mode
  if (showDeleteConfirm) {
    return (
      <div className="flex items-center gap-4 p-4 bg-red-50 border border-red-200 rounded-lg">
        <div className="flex-1">
          <p className="text-sm font-medium text-red-900">Delete this task?</p>
          <p className="text-xs text-red-700 mt-1">This action cannot be undone.</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
          <button
            onClick={() => setShowDeleteConfirm(false)}
            disabled={isDeleting}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 transition-colors disabled:opacity-50"
          >
            Cancel
          </button>
        </div>
      </div>
    );
  }

  // Normal display mode
  return (
    <div className="flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
      {/* Checkbox for completion */}
      <button
        onClick={() => onComplete?.(task.id)}
        className="flex-shrink-0 w-5 h-5 border-2 border-gray-300 rounded hover:border-blue-500 transition-colors"
        aria-label={task.completed ? 'Mark incomplete' : 'Mark complete'}
      >
        {task.completed && (
          <svg className="w-full h-full text-blue-600" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clipRule="evenodd"
            />
          </svg>
        )}
      </button>

      {/* Task title */}
      <div className="flex-1 min-w-0">
        <h3
          className={`text-sm font-medium truncate ${
            task.completed ? 'line-through text-gray-500' : 'text-gray-900'
          }`}
        >
          {task.title}
        </h3>
        <p className="text-xs text-gray-500 mt-1">
          Created {new Date(task.created_at).toLocaleDateString()}
        </p>
      </div>

      {/* Action buttons */}
      <div className="flex items-center gap-2">
        {onEdit && !task.completed && (
          <button
            onClick={() => setIsEditing(true)}
            className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
            aria-label="Edit task"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
        )}

        {onDelete && (
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            aria-label="Delete task"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}
