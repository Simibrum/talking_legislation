import React from 'react';
import QueryInput from "./QueryInput";
import UserQueryDisplay from './UserQueryDisplay';
import SourceOutputList from './SourceOutputList';

const sourcesData = [
  { text: 'Some legal text 1', citation: 'Section 1.1' },
  { text: 'Some legal text 2', citation: 'Section 1.2' },
  // more sources
];

function App() {
    // Test data
    const title = "Your Query";
    const userQuery = "This is the output of your query";

    // Output
    return (
        <div className="App">
          <header className="App-header">
            <h1>Legislation Query</h1>
          </header>
          <main>
            <QueryInput />
            <hr/>
            <UserQueryDisplay titleName={title} output={userQuery} />
            <hr/>
            <SourceOutputList sources={sourcesData} />
          </main>
        </div>
      );
    }

export default App;
