import React from 'react';

const SourceOutput = ({ sourceText, sourceCitation }) => {
  return (
    <figure>
      <blockquote className="blockquote">
        <p className="mb-0">{sourceText}</p>
      </blockquote>
      <figcaption className="blockquote-footer">
        <cite title={sourceCitation}>{sourceCitation}</cite>
      </figcaption>
    </figure>
  );
};

export default SourceOutput;