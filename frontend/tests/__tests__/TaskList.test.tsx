/**
 * Unit tests for TaskList component (T163).
 * Tests rendering, loading states, error states, and empty states.
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import { TaskList } from '@/components/TaskList';
import { Task } from '@/lib/types';

// Mock TaskItem component
jest.mock('@/components/TaskItem', () => ({
  TaskItem: ({ task, onComplete, onEdit, onDelete }: any) => (
    <div data-testid={`task-item-${task.id}`}>
      <span>{task.title}</span>
      {onComplete && <button onClick={() => onComplete(task.id)}>Complete</button>}
      {onEdit && <button onClick={() => onEdit(task.id, 'New Title')}>Edit</button>}
      {onDelete && <button onClick={() => onDelete(task.id)}>Delete</button>}
    </div>
  ),
}));

describe('TaskList Component', () => {
  const mockTasks: Task[] = [
    {
      id: 'task-1',
      user_id: 'user-1',
      title: 'First Task',
      completed: false,
      is_archived: false,
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2024-01-15T10:00:00Z',
    },
    {
      id: 'task-2',
      user_id: 'user-1',
      title: 'Second Task',
      completed: true,
      is_archived: false,
      created_at: '2024-01-15T11:00:00Z',
      updated_at: '2024-01-15T11:00:00Z',
    },
    {
      id: 'task-3',
      user_id: 'user-1',
      title: 'Third Task',
      completed: false,
      is_archived: false,
      created_at: '2024-01-15T12:00:00Z',
      updated_at: '2024-01-15T12:00:00Z',
    },
  ];

  describe('Loading State', () => {
    it('renders loading skeletons when isLoading is true', () => {
      render(<TaskList tasks={[]} isLoading={true} />);

      const skeletons = screen.getAllByRole('generic').filter((el) =>
        el.className.includes('animate-pulse')
      );

      expect(skeletons.length).toBeGreaterThan(0);
      expect(screen.queryByText(/task/i)).not.toBeInTheDocument();
    });

    it('renders exactly 3 loading skeleton items', () => {
      const { container } = render(<TaskList tasks={[]} isLoading={true} />);

      const skeletons = container.querySelectorAll('.animate-pulse');
      expect(skeletons).toHaveLength(3);
    });

    it('does not render tasks when loading', () => {
      render(<TaskList tasks={mockTasks} isLoading={true} />);

      expect(screen.queryByText('First Task')).not.toBeInTheDocument();
      expect(screen.queryByText('Second Task')).not.toBeInTheDocument();
    });
  });

  describe('Error State', () => {
    it('renders error message when error prop provided', () => {
      const error = new Error('Failed to fetch tasks');
      render(<TaskList tasks={[]} error={error} />);

      expect(screen.getByText('Failed to load tasks')).toBeInTheDocument();
      expect(screen.getByText('Failed to fetch tasks')).toBeInTheDocument();
    });

    it('renders generic error message when error.message is undefined', () => {
      const error = new Error();
      error.message = '';
      render(<TaskList tasks={[]} error={error} />);

      expect(screen.getByText('Failed to load tasks')).toBeInTheDocument();
      expect(
        screen.getByText('An error occurred while fetching your tasks')
      ).toBeInTheDocument();
    });

    it('renders error icon in error state', () => {
      const error = new Error('Network error');
      const { container } = render(<TaskList tasks={[]} error={error} />);

      const errorIcon = container.querySelector('svg.text-red-600');
      expect(errorIcon).toBeInTheDocument();
    });

    it('does not render tasks when error present', () => {
      const error = new Error('Failed');
      render(<TaskList tasks={mockTasks} error={error} />);

      expect(screen.queryByText('First Task')).not.toBeInTheDocument();
    });
  });

  describe('Empty State', () => {
    it('renders empty state when tasks array is empty', () => {
      render(<TaskList tasks={[]} />);

      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
      expect(screen.getByText('Get started by creating your first task.')).toBeInTheDocument();
    });

    it('renders empty state icon', () => {
      const { container } = render(<TaskList tasks={[]} />);

      const emptyIcon = container.querySelector('svg.text-gray-400');
      expect(emptyIcon).toBeInTheDocument();
    });

    it('renders empty state when tasks is undefined', () => {
      render(<TaskList tasks={undefined as any} />);

      expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    });
  });

  describe('Task List Rendering', () => {
    it('renders all tasks when provided', () => {
      render(<TaskList tasks={mockTasks} />);

      expect(screen.getByText('First Task')).toBeInTheDocument();
      expect(screen.getByText('Second Task')).toBeInTheDocument();
      expect(screen.getByText('Third Task')).toBeInTheDocument();
    });

    it('renders correct task count header', () => {
      render(<TaskList tasks={mockTasks} />);

      expect(screen.getByText('3 Tasks')).toBeInTheDocument();
    });

    it('uses singular "Task" for single task', () => {
      const singleTask = [mockTasks[0]];
      render(<TaskList tasks={singleTask} />);

      expect(screen.getByText('1 Task')).toBeInTheDocument();
    });

    it('renders TaskItem components with correct props', () => {
      render(<TaskList tasks={mockTasks} />);

      expect(screen.getByTestId('task-item-task-1')).toBeInTheDocument();
      expect(screen.getByTestId('task-item-task-2')).toBeInTheDocument();
      expect(screen.getByTestId('task-item-task-3')).toBeInTheDocument();
    });

    it('passes unique key to each TaskItem', () => {
      const { container } = render(<TaskList tasks={mockTasks} />);

      const taskItems = container.querySelectorAll('[data-testid^="task-item-"]');
      expect(taskItems).toHaveLength(3);
    });
  });

  describe('Callback Props', () => {
    it('passes onComplete callback to TaskItem components', () => {
      const onComplete = jest.fn();
      render(<TaskList tasks={mockTasks} onComplete={onComplete} />);

      const completeButtons = screen.getAllByText('Complete');
      expect(completeButtons).toHaveLength(3);

      completeButtons[0].click();
      expect(onComplete).toHaveBeenCalledWith('task-1');
    });

    it('passes onEdit callback to TaskItem components', () => {
      const onEdit = jest.fn();
      render(<TaskList tasks={mockTasks} onEdit={onEdit} />);

      const editButtons = screen.getAllByText('Edit');
      expect(editButtons).toHaveLength(3);

      editButtons[1].click();
      expect(onEdit).toHaveBeenCalledWith('task-2', 'New Title');
    });

    it('passes onDelete callback to TaskItem components', () => {
      const onDelete = jest.fn();
      render(<TaskList tasks={mockTasks} onDelete={onDelete} />);

      const deleteButtons = screen.getAllByText('Delete');
      expect(deleteButtons).toHaveLength(3);

      deleteButtons[2].click();
      expect(onDelete).toHaveBeenCalledWith('task-3');
    });

    it('works without any callback props', () => {
      render(<TaskList tasks={mockTasks} />);

      expect(screen.getByText('First Task')).toBeInTheDocument();
      expect(screen.queryByText('Complete')).not.toBeInTheDocument();
      expect(screen.queryByText('Edit')).not.toBeInTheDocument();
      expect(screen.queryByText('Delete')).not.toBeInTheDocument();
    });
  });

  describe('State Priority', () => {
    it('prioritizes loading state over error state', () => {
      const error = new Error('Failed');
      render(<TaskList tasks={[]} isLoading={true} error={error} />);

      expect(screen.queryByText('Failed to load tasks')).not.toBeInTheDocument();
      expect(screen.getAllByRole('generic').some((el) => el.className.includes('animate-pulse'))).toBe(true);
    });

    it('prioritizes error state over empty state', () => {
      const error = new Error('Failed');
      render(<TaskList tasks={[]} error={error} />);

      expect(screen.getByText('Failed to load tasks')).toBeInTheDocument();
      expect(screen.queryByText('No tasks yet')).not.toBeInTheDocument();
    });

    it('prioritizes error state over tasks', () => {
      const error = new Error('Failed');
      render(<TaskList tasks={mockTasks} error={error} />);

      expect(screen.getByText('Failed to load tasks')).toBeInTheDocument();
      expect(screen.queryByText('First Task')).not.toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('renders task count as heading', () => {
      render(<TaskList tasks={mockTasks} />);

      const heading = screen.getByRole('heading', { level: 2 });
      expect(heading).toHaveTextContent('3 Tasks');
    });

    it('provides descriptive error message structure', () => {
      const error = new Error('Network timeout');
      render(<TaskList tasks={[]} error={error} />);

      const errorHeading = screen.getByRole('heading', { level: 3 });
      expect(errorHeading).toHaveTextContent('Failed to load tasks');
    });
  });

  describe('Edge Cases', () => {
    it('handles tasks with special characters in titles', () => {
      const specialTasks: Task[] = [
        {
          ...mockTasks[0],
          title: '<script>alert("XSS")</script>',
        },
      ];

      render(<TaskList tasks={specialTasks} />);
      expect(screen.getByText('<script>alert("XSS")</script>')).toBeInTheDocument();
    });

    it('handles very long task list', () => {
      const manyTasks = Array.from({ length: 100 }, (_, i) => ({
        ...mockTasks[0],
        id: `task-${i}`,
        title: `Task ${i + 1}`,
      }));

      render(<TaskList tasks={manyTasks} />);

      expect(screen.getByText('100 Tasks')).toBeInTheDocument();
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 100')).toBeInTheDocument();
    });
  });
});
