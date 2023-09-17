import React from 'react';

const SourceOutput = ({sourceText, sourceCitation}) => {
    const citationParts = sourceCitation.split(" - ");
    const citationTitle = citationParts[0];
    const citationURL = citationParts[1];
    return (
        <figure>
            <blockquote className="blockquote fs-6">
                <p className="mb-0" style={{whiteSpace: "pre-line"}}>{sourceText}</p>
            </blockquote>
            <figcaption className="blockquote-footer">
                <cite title={citationTitle}>{citationTitle}{citationURL && " - "}
                {citationURL && <a href={citationURL} target="_blank" rel="noopener noreferrer">{citationURL}</a>}
                </cite>
            </figcaption>
            <div className="centered-line"></div>
        </figure>
    );
};

export default SourceOutput;