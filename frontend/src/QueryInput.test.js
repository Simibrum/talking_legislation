import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import QueryInput from './QueryInput'; // Adjust this import to your file structure

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

// Add any additional tests like button click behavior, etc.
