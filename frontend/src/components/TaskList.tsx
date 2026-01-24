'use client';

/**
 * TaskList component - displays a list of tasks.
 * Migrated to shadcn/ui components for consistent styling.
 */

import { ClipboardList, AlertCircle } from 'lucide-react';
import { Task } from '@/lib/types';
import { TaskItem } from './TaskItem';
import { Card } from '@/components/ui/card';

interface TaskListProps {
  tasks: Task[];
  isLoading?: boolean;
  error?: Error | null;
  onComplete?: (taskId: string) => void;
  onEdit?: (taskId: string, newTitle: string) => void;
  onDelete?: (taskId: string) => void;
}

export function TaskList({
  tasks,
  isLoading,
  error,
  onComplete,
  onEdit,
  onDelete,
}: TaskListProps) {
  // Loading state
  if (isLoading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="animate-pulse">
            <div className="h-20 bg-muted rounded-lg"></div>
          </Card>
        ))}
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <Card className="p-4 bg-destructive/5 border-destructive/20">
        <div className="flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-destructive mt-0.5 flex-shrink-0" />
          <div>
            <h3 className="text-sm font-medium text-destructive">Failed to load tasks</h3>
            <p className="text-sm text-destructive/80 mt-1">
              {error.message || 'An error occurred while fetching your tasks'}
            </p>
          </div>
        </div>
      </Card>
    );
  }

  // Empty state
  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <ClipboardList className="mx-auto h-12 w-12 text-muted-foreground" />
        <h3 className="mt-2 text-sm font-medium text-foreground">No tasks yet</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          Get started by creating your first task.
        </p>
      </div>
    );
  }

  // Task list
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-foreground">
          {tasks.length} {tasks.length === 1 ? 'Task' : 'Tasks'}
        </h2>
      </div>

      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onComplete={onComplete}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
