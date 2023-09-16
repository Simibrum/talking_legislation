import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import SourceOutput from './SourceOutput';

test('renders source text and citation', () => {
  const { getByText } = render(<SourceOutput sourceText="Test Text" sourceCitation="Test Citation" />);

  expect(getByText('Test Text')).toBeInTheDocument();
  expect(getByText('Test Citation')).toBeInTheDocument();
});
