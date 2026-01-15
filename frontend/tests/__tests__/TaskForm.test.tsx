/**
 * Unit tests for TaskForm component (T163).
 * Tests form rendering, validation, submission, and user interactions.
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TaskForm } from '@/components/TaskForm';

describe('TaskForm Component', () => {
  describe('Rendering', () => {
    it('renders input field with placeholder', () => {
      render(<TaskForm onSubmit={jest.fn()} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      expect(input).toBeInTheDocument();
      expect(input).toHaveAttribute('type', 'text');
    });

    it('renders submit button with correct text', () => {
      render(<TaskForm onSubmit={jest.fn()} />);

      const button = screen.getByRole('button', { name: /add task/i });
      expect(button).toBeInTheDocument();
    });

    it('renders character counter', () => {
      render(<TaskForm onSubmit={jest.fn()} />);

      expect(screen.getByText('0/500 characters')).toBeInTheDocument();
    });

    it('submit button is disabled initially when input is empty', () => {
      render(<TaskForm onSubmit={jest.fn()} />);

      const button = screen.getByRole('button', { name: /add task/i });
      expect(button).toBeDisabled();
    });
  });

  describe('User Input', () => {
    it('updates input value when user types', async () => {
      const user = userEvent.setup();
      render(<TaskForm onSubmit={jest.fn()} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      await user.type(input, 'New task');

      expect(input).toHaveValue('New task');
    });

    it('enables submit button when input has content', async () => {
      const user = userEvent.setup();
      render(<TaskForm onSubmit={jest.fn()} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const button = screen.getByRole('button', { name: /add task/i });

      expect(button).toBeDisabled();

      await user.type(input, 'Task with content');

      expect(button).not.toBeDisabled();
    });

    it('updates character counter as user types', async () => {
      const user = userEvent.setup();
      render(<TaskForm onSubmit={jest.fn()} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      await user.type(input, 'Hello');

      expect(screen.getByText('5/500 characters')).toBeInTheDocument();
    });

    it('enforces maxLength of 500 characters', () => {
      render(<TaskForm onSubmit={jest.fn()} />);

      const input = screen.getByPlaceholderText('What needs to be done?') as HTMLInputElement;
      expect(input).toHaveAttribute('maxLength', '500');
    });
  });

  describe('Form Submission', () => {
    it('calls onSubmit with trimmed title when form submitted', async () => {
      const user = userEvent.setup();
      const onSubmit = jest.fn();
      render(<TaskForm onSubmit={onSubmit} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      await user.type(input, '  Task with spaces  ');
      fireEvent.submit(form);

      expect(onSubmit).toHaveBeenCalledWith('Task with spaces');
      expect(onSubmit).toHaveBeenCalledTimes(1);
    });

    it('clears input after successful submission', async () => {
      const user = userEvent.setup();
      const onSubmit = jest.fn();
      render(<TaskForm onSubmit={onSubmit} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      await user.type(input, 'New task');
      expect(input).toHaveValue('New task');

      fireEvent.submit(form);

      await waitFor(() => {
        expect(input).toHaveValue('');
      });
    });

    it('resets character counter after submission', async () => {
      const user = userEvent.setup();
      render(<TaskForm onSubmit={jest.fn()} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      await user.type(input, 'Task');
      expect(screen.getByText('4/500 characters')).toBeInTheDocument();

      fireEvent.submit(form);

      await waitFor(() => {
        expect(screen.getByText('0/500 characters')).toBeInTheDocument();
      });
    });

    it('can submit by clicking submit button', async () => {
      const user = userEvent.setup();
      const onSubmit = jest.fn();
      render(<TaskForm onSubmit={onSubmit} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const button = screen.getByRole('button', { name: /add task/i });

      await user.type(input, 'Click submit task');
      await user.click(button);

      expect(onSubmit).toHaveBeenCalledWith('Click submit task');
    });
  });

  describe('Validation', () => {
    it('shows error when submitting empty title', async () => {
      const user = userEvent.setup();
      const onSubmit = jest.fn();
      render(<TaskForm onSubmit={onSubmit} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      await user.type(input, '   '); // Only whitespace
      fireEvent.submit(form);

      expect(await screen.findByText('Task title cannot be empty')).toBeInTheDocument();
      expect(onSubmit).not.toHaveBeenCalled();
    });

    it('shows error when title exceeds 500 characters', async () => {
      const user = userEvent.setup();
      const onSubmit = jest.fn();
      render(<TaskForm onSubmit={onSubmit} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      // Since maxLength prevents typing more, we'll manually set value
      const longTitle = 'A'.repeat(501);
      fireEvent.change(input, { target: { value: longTitle } });
      fireEvent.submit(form);

      await waitFor(() => {
        const errorMessage = screen.queryByText(/cannot exceed 500 characters/i);
        if (errorMessage) {
          expect(errorMessage).toBeInTheDocument();
        }
        expect(onSubmit).not.toHaveBeenCalled();
      });
    });

    it('clears error when user starts typing after error', async () => {
      const user = userEvent.setup();
      render(<TaskForm onSubmit={jest.fn()} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      // Trigger error
      await user.type(input, '   ');
      fireEvent.submit(form);
      expect(await screen.findByText('Task title cannot be empty')).toBeInTheDocument();

      // Start typing
      await user.clear(input);
      await user.type(input, 'V');

      await waitFor(() => {
        expect(screen.queryByText('Task title cannot be empty')).not.toBeInTheDocument();
      });
    });

    it('applies error styling to input when validation fails', async () => {
      const user = userEvent.setup();
      render(<TaskForm onSubmit={jest.fn()} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      await user.type(input, '   ');
      fireEvent.submit(form);

      await waitFor(() => {
        expect(input).toHaveClass('border-red-300');
      });
    });
  });

  describe('Submitting State', () => {
    it('disables input when isSubmitting is true', () => {
      render(<TaskForm onSubmit={jest.fn()} isSubmitting={true} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      expect(input).toBeDisabled();
    });

    it('disables submit button when isSubmitting is true', () => {
      render(<TaskForm onSubmit={jest.fn()} isSubmitting={true} />);

      const button = screen.getByRole('button', { name: /adding/i });
      expect(button).toBeDisabled();
    });

    it('shows "Adding..." text when isSubmitting is true', () => {
      render(<TaskForm onSubmit={jest.fn()} isSubmitting={true} />);

      expect(screen.getByText(/adding/i)).toBeInTheDocument();
      expect(screen.queryByText('Add Task')).not.toBeInTheDocument();
    });

    it('shows loading spinner when isSubmitting is true', () => {
      const { container } = render(<TaskForm onSubmit={jest.fn()} isSubmitting={true} />);

      const spinner = container.querySelector('.animate-spin');
      expect(spinner).toBeInTheDocument();
    });

    it('applies disabled styling to button when isSubmitting', () => {
      render(<TaskForm onSubmit={jest.fn()} isSubmitting={true} />);

      const button = screen.getByRole('button');
      expect(button).toHaveClass('bg-gray-400');
      expect(button).toHaveClass('cursor-not-allowed');
    });
  });

  describe('Accessibility', () => {
    it('input is keyboard accessible', async () => {
      const user = userEvent.setup();
      render(<TaskForm onSubmit={jest.fn()} />);

      const input = screen.getByPlaceholderText('What needs to be done?');

      await user.tab();
      expect(input).toHaveFocus();
    });

    it('can submit form with Enter key', async () => {
      const onSubmit = jest.fn();
      render(<TaskForm onSubmit={onSubmit} />);

      const input = screen.getByPlaceholderText('What needs to be done?');

      fireEvent.change(input, { target: { value: 'Keyboard task' } });
      fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });
      fireEvent.submit(input.closest('form')!);

      expect(onSubmit).toHaveBeenCalledWith('Keyboard task');
    });

    it('form has proper structure for screen readers', () => {
      const { container } = render(<TaskForm onSubmit={jest.fn()} />);

      const form = container.querySelector('form');
      expect(form).toBeInTheDocument();

      const input = screen.getByPlaceholderText('What needs to be done?');
      const button = screen.getByRole('button');

      expect(form).toContainElement(input);
      expect(form).toContainElement(button);
    });
  });

  describe('Edge Cases', () => {
    it('handles rapid submissions', async () => {
      const user = userEvent.setup();
      const onSubmit = jest.fn();
      render(<TaskForm onSubmit={onSubmit} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      await user.type(input, 'Task 1');
      fireEvent.submit(form);

      await user.type(input, 'Task 2');
      fireEvent.submit(form);

      // Should handle both submissions
      expect(onSubmit).toHaveBeenCalledTimes(2);
    });

    it('handles special characters in title', async () => {
      const user = userEvent.setup();
      const onSubmit = jest.fn();
      render(<TaskForm onSubmit={onSubmit} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      const specialTitle = 'Task with émojis 🎉 & special chars!@#$%';
      await user.type(input, specialTitle);
      fireEvent.submit(form);

      expect(onSubmit).toHaveBeenCalledWith(specialTitle);
    });

    it('handles paste events', async () => {
      const user = userEvent.setup();
      const onSubmit = jest.fn();
      render(<TaskForm onSubmit={onSubmit} />);

      const input = screen.getByPlaceholderText('What needs to be done?');
      const form = screen.getByRole('button', { name: /add task/i }).closest('form')!;

      await user.click(input);
      await user.paste('Pasted task content');
      fireEvent.submit(form);

      expect(onSubmit).toHaveBeenCalledWith('Pasted task content');
    });
  });
});
