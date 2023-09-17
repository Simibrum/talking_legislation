import React, { useState } from "react";

const QueryInput = ({ setUserQuery }) => {
  const [localQuery, setLocalQuery] = useState("");

  const handleInputChange = (e) => {
    setLocalQuery(e.target.value);
  };

  const handleButtonClick = () => {
    setUserQuery(localQuery);
  };

  return (
    <div className="input-group mb-3 py-3">
      <input
        type="text"
        id="query"
        name="query"
        autoComplete="off"
        className="form-control form-control-lg"
        placeholder="Ask your question here..."
        aria-label="Ask your question here..."
        aria-describedby="button-addon2"
        value={localQuery}
        onChange={handleInputChange}
      />
      <button
        className="btn btn-outline-secondary"
        type="submit"
        id="button-addon2"
        onClick={handleButtonClick}
      >
        <i className="fas fa-search"></i>
      </button>
    </div>
  );
};

export default QueryInput;
