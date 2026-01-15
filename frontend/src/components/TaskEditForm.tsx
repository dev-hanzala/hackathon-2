'use client';

/**
 * TaskEditForm component - inline form for editing task titles.
 * User Story 5: Update Task
 */

import { useState, FormEvent } from 'react';

interface TaskEditFormProps {
  taskId: string;
  currentTitle: string;
  onSave: (taskId: string, newTitle: string) => void;
  onCancel: () => void;
  isSubmitting?: boolean;
}

export function TaskEditForm({
  taskId,
  currentTitle,
  onSave,
  onCancel,
  isSubmitting,
}: TaskEditFormProps) {
  const [title, setTitle] = useState(currentTitle);
  const [error, setError] = useState('');

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Validate title
    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      setError('Task title cannot be empty');
      return;
    }

    if (trimmedTitle.length > 500) {
      setError('Task title cannot exceed 500 characters');
      return;
    }

    // Clear error and submit
    setError('');
    onSave(taskId, trimmedTitle);
  };

  return (
    <form onSubmit={handleSubmit} className="flex-1">
      <div className="flex flex-col gap-2">
        <div className="flex gap-2">
          <input
            type="text"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (error) setError('');
            }}
            className={`flex-1 px-3 py-2 text-sm border rounded focus:outline-none focus:ring-2 transition-colors ${
              error
                ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
            }`}
            disabled={isSubmitting}
            maxLength={500}
            autoFocus
          />
          <button
            type="submit"
            disabled={isSubmitting || !title.trim() || title.trim() === currentTitle.trim()}
            className={`px-4 py-2 text-sm font-medium text-white rounded transition-colors ${
              isSubmitting || !title.trim() || title.trim() === currentTitle.trim()
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {isSubmitting ? 'Saving...' : 'Save'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 transition-colors disabled:opacity-50"
          >
            Cancel
          </button>
        </div>
        {error && <p className="text-xs text-red-600">{error}</p>}
        <p className="text-xs text-gray-500">{title.length}/500 characters</p>
      </div>
    </form>
  );
}
