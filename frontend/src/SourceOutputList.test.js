import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import SourceOutputList from './SourceOutputList';

test('renders a list of sources', () => {
  const sources = [
    { text: 'Text 1', citation: 'Citation 1' },
    { text: 'Text 2', citation: 'Citation 2' }
  ];

  const { getAllByText } = render(<SourceOutputList sources={sources} />);

  expect(getAllByText(/Text/).length).toBe(2);
  expect(getAllByText(/Citation/).length).toBe(2);
});
