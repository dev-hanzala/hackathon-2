'use client';

/**
 * TaskEditForm component - inline form for editing task titles.
 * Migrated to shadcn/ui components for consistent styling.
 */

import { useState, FormEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

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
          <Input
            type="text"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (error) setError('');
            }}
            className={`flex-1 ${error ? 'border-destructive focus-visible:ring-destructive' : ''}`}
            disabled={isSubmitting}
            maxLength={500}
            autoFocus
          />
          <Button
            type="submit"
            disabled={isSubmitting || !title.trim() || title.trim() === currentTitle.trim()}
            size="sm"
          >
            {isSubmitting ? 'Saving...' : 'Save'}
          </Button>
          <Button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            variant="outline"
            size="sm"
          >
            Cancel
          </Button>
        </div>
        {error && <p className="text-xs text-destructive">{error}</p>}
        <p className="text-xs text-muted-foreground">{title.length}/500 characters</p>
      </div>
    </form>
  );
}
