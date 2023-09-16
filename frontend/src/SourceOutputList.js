import React from 'react';
import SourceOutput from './SourceOutput';

const SourceOutputList = ({ sources }) => {
  return (
    <div>
      {sources.map((source, index) => (
        <SourceOutput
          key={index}
          sourceText={source.text}
          sourceCitation={source.citation}
        />
      ))}
    </div>
  );
};

export default SourceOutputList;
