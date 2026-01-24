'use client';

/**
 * TaskForm component - form for creating new tasks.
 * Migrated to shadcn/ui components for consistent styling.
 */

import { useState, FormEvent } from 'react';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface TaskFormProps {
  onSubmit: (title: string) => void;
  isSubmitting?: boolean;
}

export function TaskForm({ onSubmit, isSubmitting }: TaskFormProps) {
  const [title, setTitle] = useState('');
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
    onSubmit(trimmedTitle);
    setTitle(''); // Clear input after submission
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1 space-y-2">
          <Label htmlFor="task-title" className="sr-only">
            Task title
          </Label>
          <Input
            id="task-title"
            type="text"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (error) setError(''); // Clear error on change
            }}
            placeholder="What needs to be done?"
            className={error ? 'border-destructive focus-visible:ring-destructive' : ''}
            disabled={isSubmitting}
            maxLength={500}
          />
          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}
        </div>
        <Button
          type="submit"
          disabled={isSubmitting || !title.trim()}
          className="h-10 px-6"
        >
          {isSubmitting ? (
            <span className="flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              Adding...
            </span>
          ) : (
            'Add Task'
          )}
        </Button>
      </div>
      <p className="mt-2 text-xs text-muted-foreground">
        {title.length}/500 characters
      </p>
    </form>
  );
}
