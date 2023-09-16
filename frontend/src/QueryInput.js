import React, { useState } from 'react';

const QueryInput = ({ onQuerySubmit }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onQuerySubmit(query);
  };

  return (
    <div className="input-group mb-3">
      <input
        type="text"
        id="query"
        name="query"
        className="form-control form-control-lg"
        placeholder="Ask your question here..."
        aria-label="Ask your question here..."
        aria-describedby="button-addon2"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button className="btn btn-outline-secondary" type="submit" id="button-addon2" onClick={handleSubmit}>
        <i className="fas fa-search"></i>
      </button>
    </div>
  );
};

export default QueryInput;
