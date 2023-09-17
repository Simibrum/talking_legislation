import React, {useState} from "react";

const QueryInput = ({setUserQuery, resetApp}) => {
    const [localQuery, setLocalQuery] = useState("");

    const handleInputChange = (e) => {
        setLocalQuery(e.target.value);
    };

    const handleButtonClick = () => {
        setUserQuery(localQuery);
    };

    const handleResetClick = () => {
        setLocalQuery(""); // Reset the local input
        setUserQuery(""); // Reset the query in the main App state
        resetApp(); // Call the global reset function from App.js
    };

    return (
        <div className="input-group mb-3 py-3">
            <button type="button" className={"btn btn-light"} onClick={handleResetClick}>
                <i className="fas fa-undo"></i>
            </button>
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
