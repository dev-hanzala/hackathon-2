'use client';

/**
 * TaskItem component - displays a single task with actions.
 * Migrated to shadcn/ui components for consistent styling.
 */

import { useState } from 'react';
import { Pencil, Trash2 } from 'lucide-react';
import { Task } from '@/lib/types';
import { TaskEditForm } from './TaskEditForm';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';

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
      <Card className="p-4 bg-primary/5 border-primary/20">
        <TaskEditForm
          taskId={task.id}
          currentTitle={task.title}
          onSave={handleSave}
          onCancel={() => setIsEditing(false)}
          isSubmitting={isUpdating}
        />
      </Card>
    );
  }

  // Delete confirmation mode
  if (showDeleteConfirm) {
    return (
      <Card className="p-4 bg-destructive/5 border-destructive/20">
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <p className="text-sm font-medium text-destructive">Delete this task?</p>
            <p className="text-xs text-destructive/80 mt-1">This action cannot be undone.</p>
          </div>
          <div className="flex items-center gap-2">
            <Button
              onClick={handleDelete}
              disabled={isDeleting}
              variant="destructive"
              size="sm"
            >
              {isDeleting ? 'Deleting...' : 'Delete'}
            </Button>
            <Button
              onClick={() => setShowDeleteConfirm(false)}
              disabled={isDeleting}
              variant="outline"
              size="sm"
            >
              Cancel
            </Button>
          </div>
        </div>
      </Card>
    );
  }

  // Normal display mode
  return (
    <Card className="p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center gap-4">
        {/* Checkbox for completion */}
        <Checkbox
          checked={task.completed}
          onCheckedChange={() => onComplete?.(task.id)}
          aria-label={task.completed ? 'Mark incomplete' : 'Mark complete'}
          className="h-5 w-5"
        />

        {/* Task title */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-sm font-medium truncate ${
              task.completed ? 'line-through text-muted-foreground' : 'text-foreground'
            }`}
          >
            {task.title}
          </h3>
          <p className="text-xs text-muted-foreground mt-1">
            Created {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-1">
          {onEdit && !task.completed && (
            <Button
              onClick={() => setIsEditing(true)}
              variant="ghost"
              size="icon"
              className="h-8 w-8 text-muted-foreground hover:text-primary"
              aria-label="Edit task"
            >
              <Pencil className="h-4 w-4" />
            </Button>
          )}

          {onDelete && (
            <Button
              onClick={() => setShowDeleteConfirm(true)}
              variant="ghost"
              size="icon"
              className="h-8 w-8 text-muted-foreground hover:text-destructive"
              aria-label="Delete task"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
}
