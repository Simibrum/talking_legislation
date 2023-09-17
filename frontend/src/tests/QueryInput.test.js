import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import QueryInput from '../QueryInput';

test('renders QueryInput with input and button', () => {
  const { getByPlaceholderText, getByRole } = render(<QueryInput />);

  // Check if the input field is displayed
  const inputElement = getByPlaceholderText('Ask your question here...');
  expect(inputElement).toBeInTheDocument();

  // Check if the search button is displayed
  const buttonElement = getByRole('button');
  expect(buttonElement).toBeInTheDocument();
});

test('allows text to be typed into input', () => {
  const { getByPlaceholderText } = render(<QueryInput />);

  // Type text into the input field
  const inputElement = getByPlaceholderText('Ask your question here...');
  fireEvent.change(inputElement, { target: { value: 'What is the meaning of life?' } });

  // Check if the input field value has changed
  expect(inputElement.value).toBe('What is the meaning of life?');
});

// Add any additional tests_logic like button click behavior, etc.


test('calls setUserQuery on submit', () => {
  const mockSetUserQuery = jest.fn();
  render(<QueryInput setUserQuery={mockSetUserQuery} />);

  const inputElement = screen.getByPlaceholderText("Ask your question here...");
  const buttonElement = screen.getByRole("button");

  fireEvent.change(inputElement, { target: { value: 'What is the meaning of life?' } });
  fireEvent.click(buttonElement);

  expect(mockSetUserQuery).toHaveBeenCalledWith('What is the meaning of life?');
});
