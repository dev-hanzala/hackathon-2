/**
 * Unit tests for TaskItem component (T163).
 * Tests rendering, user interactions, and state management.
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TaskItem } from '@/components/TaskItem';
import { Task } from '@/lib/types';

// Mock TaskEditForm component
jest.mock('@/components/TaskEditForm', () => ({
  TaskEditForm: ({ taskId, currentTitle, onSave, onCancel, isSubmitting }: any) => (
    <div data-testid="task-edit-form">
      <input
        data-testid="edit-input"
        defaultValue={currentTitle}
        onChange={(e) => {
          // Store value for testing
          (e.target as any).editValue = e.target.value;
        }}
      />
      <button
        data-testid="save-button"
        onClick={() => {
          const input = document.querySelector('[data-testid="edit-input"]') as HTMLInputElement;
          onSave(taskId, input?.editValue || currentTitle);
        }}
        disabled={isSubmitting}
      >
        Save
      </button>
      <button data-testid="cancel-button" onClick={onCancel}>
        Cancel
      </button>
    </div>
  ),
}));

describe('TaskItem Component', () => {
  const mockTask: Task = {
    id: 'task-123',
    user_id: 'user-456',
    title: 'Test Task',
    completed: false,
    is_archived: false,
    created_at: '2024-01-15T12:00:00Z',
    updated_at: '2024-01-15T12:00:00Z',
  };

  describe('Rendering', () => {
    it('renders task title correctly', () => {
      render(<TaskItem task={mockTask} />);
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    it('renders creation date', () => {
      render(<TaskItem task={mockTask} />);
      const dateElement = screen.getByText(/Created/);
      expect(dateElement).toBeInTheDocument();
    });

    it('renders unchecked checkbox for incomplete task', () => {
      render(<TaskItem task={mockTask} onComplete={jest.fn()} />);
      const checkbox = screen.getByLabelText('Mark complete');
      expect(checkbox).toBeInTheDocument();
      expect(checkbox.querySelector('svg')).not.toBeInTheDocument();
    });

    it('renders checked checkbox for completed task', () => {
      const completedTask = { ...mockTask, completed: true };
      render(<TaskItem task={completedTask} onComplete={jest.fn()} />);
      const checkbox = screen.getByLabelText('Mark incomplete');
      expect(checkbox).toBeInTheDocument();
      expect(checkbox.querySelector('svg')).toBeInTheDocument();
    });

    it('applies strikethrough styling to completed task title', () => {
      const completedTask = { ...mockTask, completed: true };
      render(<TaskItem task={completedTask} />);
      const titleElement = screen.getByText('Test Task');
      expect(titleElement).toHaveClass('line-through');
    });

    it('renders edit button when onEdit prop provided and task not completed', () => {
      render(<TaskItem task={mockTask} onEdit={jest.fn()} />);
      const editButton = screen.getByLabelText('Edit task');
      expect(editButton).toBeInTheDocument();
    });

    it('does not render edit button for completed tasks', () => {
      const completedTask = { ...mockTask, completed: true };
      render(<TaskItem task={completedTask} onEdit={jest.fn()} />);
      expect(screen.queryByLabelText('Edit task')).not.toBeInTheDocument();
    });

    it('renders delete button when onDelete prop provided', () => {
      render(<TaskItem task={mockTask} onDelete={jest.fn()} />);
      const deleteButton = screen.getByLabelText('Delete task');
      expect(deleteButton).toBeInTheDocument();
    });
  });

  describe('Completion Toggle', () => {
    it('calls onComplete with task ID when checkbox clicked', async () => {
      const onComplete = jest.fn();
      render(<TaskItem task={mockTask} onComplete={onComplete} />);

      const checkbox = screen.getByLabelText('Mark complete');
      await userEvent.click(checkbox);

      expect(onComplete).toHaveBeenCalledWith('task-123');
      expect(onComplete).toHaveBeenCalledTimes(1);
    });

    it('calls onComplete for completed tasks to mark incomplete', async () => {
      const onComplete = jest.fn();
      const completedTask = { ...mockTask, completed: true };
      render(<TaskItem task={completedTask} onComplete={onComplete} />);

      const checkbox = screen.getByLabelText('Mark incomplete');
      await userEvent.click(checkbox);

      expect(onComplete).toHaveBeenCalledWith('task-123');
    });
  });

  describe('Edit Mode', () => {
    it('shows edit form when edit button clicked', async () => {
      render(<TaskItem task={mockTask} onEdit={jest.fn()} />);

      const editButton = screen.getByLabelText('Edit task');
      await userEvent.click(editButton);

      expect(screen.getByTestId('task-edit-form')).toBeInTheDocument();
      expect(screen.queryByText('Test Task')).not.toBeInTheDocument(); // Original view hidden
    });

    it('calls onEdit with task ID and new title when saved', async () => {
      const onEdit = jest.fn();
      render(<TaskItem task={mockTask} onEdit={onEdit} />);

      // Enter edit mode
      const editButton = screen.getByLabelText('Edit task');
      await userEvent.click(editButton);

      // Edit and save
      const editInput = screen.getByTestId('edit-input');
      fireEvent.change(editInput, { target: { value: 'Updated Title' } });
      (editInput as any).editValue = 'Updated Title';

      const saveButton = screen.getByTestId('save-button');
      await userEvent.click(saveButton);

      expect(onEdit).toHaveBeenCalledWith('task-123', 'Updated Title');
    });

    it('exits edit mode when cancel button clicked', async () => {
      render(<TaskItem task={mockTask} onEdit={jest.fn()} />);

      // Enter edit mode
      await userEvent.click(screen.getByLabelText('Edit task'));
      expect(screen.getByTestId('task-edit-form')).toBeInTheDocument();

      // Cancel editing
      await userEvent.click(screen.getByTestId('cancel-button'));

      // Back to normal view
      await waitFor(() => {
        expect(screen.queryByTestId('task-edit-form')).not.toBeInTheDocument();
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });
    });

    it('passes isSubmitting prop to edit form', () => {
      render(<TaskItem task={mockTask} onEdit={jest.fn()} isUpdating={true} />);

      // Enter edit mode
      fireEvent.click(screen.getByLabelText('Edit task'));

      const saveButton = screen.getByTestId('save-button');
      expect(saveButton).toBeDisabled();
    });
  });

  describe('Delete Confirmation', () => {
    it('shows delete confirmation when delete button clicked', async () => {
      render(<TaskItem task={mockTask} onDelete={jest.fn()} />);

      const deleteButton = screen.getByLabelText('Delete task');
      await userEvent.click(deleteButton);

      expect(screen.getByText('Delete this task?')).toBeInTheDocument();
      expect(screen.getByText('This action cannot be undone.')).toBeInTheDocument();
    });

    it('calls onDelete with task ID when delete confirmed', async () => {
      const onDelete = jest.fn();
      render(<TaskItem task={mockTask} onDelete={onDelete} />);

      // Show confirmation
      await userEvent.click(screen.getByLabelText('Delete task'));

      // Confirm deletion
      const confirmButton = screen.getByText('Delete');
      await userEvent.click(confirmButton);

      expect(onDelete).toHaveBeenCalledWith('task-123');
      expect(onDelete).toHaveBeenCalledTimes(1);
    });

    it('cancels delete confirmation and returns to normal view', async () => {
      render(<TaskItem task={mockTask} onDelete={jest.fn()} />);

      // Show confirmation
      await userEvent.click(screen.getByLabelText('Delete task'));
      expect(screen.getByText('Delete this task?')).toBeInTheDocument();

      // Cancel
      await userEvent.click(screen.getByText('Cancel'));

      // Back to normal view
      await waitFor(() => {
        expect(screen.queryByText('Delete this task?')).not.toBeInTheDocument();
        expect(screen.getByText('Test Task')).toBeInTheDocument();
      });
    });

    it('disables delete buttons when isDeleting is true', async () => {
      render(<TaskItem task={mockTask} onDelete={jest.fn()} isDeleting={true} />);

      await userEvent.click(screen.getByLabelText('Delete task'));

      const deleteButton = screen.getByText('Deleting...');
      const cancelButton = screen.getByText('Cancel');

      expect(deleteButton).toBeDisabled();
      expect(cancelButton).toBeDisabled();
    });
  });

  describe('Props Handling', () => {
    it('does not render action buttons when callbacks not provided', () => {
      render(<TaskItem task={mockTask} />);

      expect(screen.queryByLabelText('Edit task')).not.toBeInTheDocument();
      expect(screen.queryByLabelText('Delete task')).not.toBeInTheDocument();
    });

    it('renders correctly with all optional props', () => {
      const { container } = render(
        <TaskItem
          task={mockTask}
          onComplete={jest.fn()}
          onEdit={jest.fn()}
          onDelete={jest.fn()}
          isUpdating={false}
          isDeleting={false}
        />
      );

      expect(container).toMatchSnapshot();
    });
  });
});
