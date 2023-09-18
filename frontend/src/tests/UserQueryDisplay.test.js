import React from 'react';
import { render } from '@testing-library/react';
import UserQueryDisplay from '../UserQueryDisplay';  // Adjust this import to your file structure

test('renders UserQueryDisplay with title and output', () => {
  const titleName = 'You asked...';
  const output = 'What is the meaning of life?';

  const { getByText } = render(<UserQueryDisplay titleName={titleName} output={output} />);

  // Check if the title is displayed
  expect(getByText(titleName)).toBeInTheDocument();

  // Check if the output is displayed
  expect(getByText(output)).toBeInTheDocument();
});
