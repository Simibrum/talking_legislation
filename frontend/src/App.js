import React, {useEffect, useState} from 'react';
import QueryInput from "./QueryInput";
import UserQueryDisplay from './UserQueryDisplay';
import SourceOutputList from './SourceOutputList';

const sourcesData = [
    {text: 'Some legal text 1', citation: 'Section 1.1'},
    {text: 'Some legal text 2', citation: 'Section 1.2'},
    // more sources
];

function App() {
    // Test data

    const [userQuery, setUserQuery] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState(null);

    useEffect(() => {
        if (!userQuery) return; // Don't open a WebSocket if there's no query

        const ws = new WebSocket('ws://localhost:8000/ws');

        ws.onopen = () => {
            console.log('WebSocket is connected.');
            ws.send(JSON.stringify({"query": userQuery}));
            setIsLoading(true);
        };

        ws.onmessage = (event) => {
            console.log(`Server says: ${event.data}`);
            setResponse(event.data);
            setIsLoading(false);
        };

        ws.onerror = (error) => {
            console.log(`WebSocket error: ${error}`);
            setIsLoading(false);
        };

        return () => {
            ws.close();
        };
    }, [userQuery]);

    // Output
    return (
        <div className="App">
            <header className="App-header">
                <h1>Legislation Query</h1>
            </header>
            <main>
                <QueryInput setUserQuery={setUserQuery} />
                <hr/>
                <UserQueryDisplay titleName="You asked..." output={userQuery}/>
                <hr/>
                <SourceOutputList sources={sourcesData}/>
            </main>
        </div>
    );
}

export default App;
